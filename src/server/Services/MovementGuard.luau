--!strict
-- MovementGuard: server checks on client-owned movement (audit remediation step 4, P0). Rules: Shared.MovementRules.
--
-- Flight energy (server authoritative): the server keeps each robot's wing energy. It drains while the wings are out
-- (character attribute PZ_WingsOut, which only the server sets) and recharges on the ground with the wings stowed.
-- Take-off needs MovementRules.Flight.MIN_TAKEOFF (EquipmentService asks CanTakeOff); at 0 the server folds the wings
-- and the client's FlightController lands. Published as the player attribute PZ_WingEnergy for the HUD.
--
-- Robots: every SAMPLE seconds each character's root is compared with the previous sample:
--   * speed / climb / teleport beyond MovementRules limits (walking or flying, whichever the server says it is);
--   * hovering without wings: off the ground for HOVER_TIME and not falling, with the wings stowed;
--   * flying above FLIGHT_CEILING, or leaving the WORLD box.
-- STRIKES bad samples in a row (a teleport or leaving the bounds at once) put the robot back at its last valid
-- position, fold its wings and log a warning. Server moves (pods, doors) set the character attribute
-- PZ_MoveGraceUntil (workspace:GetServerTimeNow() + seconds) via MovementGuard.Grace, so they're never flagged.
-- Seated robots are skipped (the vehicle is checked instead); anchored ones just reset their baseline.
--
-- Vehicles (VehicleService registers each DriveBody): while a player drives, the body's samples are checked the same
-- way (vehicle limits, turn rate, VEHICLE_ZONE). A correction takes network ownership back for OWNER_HOLD seconds,
-- puts the vehicle at its last valid place and stops it; EJECT_AFTER corrections within EJECT_WINDOW unseat the driver.
-- Overturned / abandoned vehicle recovery is NOT here: that is owner decision D16 (open).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local MovementRules = require(ReplicatedStorage.Shared.MovementRules)

local MovementGuard = {}

local HOVER_TIME = 2.0
local GROUND_RAY = 9          -- studs below the root that count as "on the ground" (hip height + root + margin)
local STANDING = 4             -- sphere-cast distance of a standing robot: 2.46 measured (Cypher frame), ~3 for Sentinel
local OWNER_HOLD = 1.5
local EJECT_AFTER, EJECT_WINDOW = 3, 30

-- prev = the previous sample (each check compares one sample interval); valid = where a correction puts it back
-- ground = last valid position on the ground (where a hover correction puts it back)
type CharState = { prev: Vector3?, valid: Vector3?, ground: Vector3?, strikes: number, airTime: number }
type VehState = { body: BasePart, seat: VehicleSeat, prev: CFrame?, valid: CFrame?, strikes: number, corrections: { number }, holdUntil: number }

local chars: { [Player]: CharState } = {}
local wing: { [Player]: number } = {}
local vehicles: { VehState } = {}

MovementGuard.Log = {} :: { { kind: string, who: string, reason: string, t: number } } -- recent corrections (tests, QA)

local function note(kind: string, who: string, reason: string)
	table.insert(MovementGuard.Log, { kind = kind, who = who, reason = reason, t = os.clock() })
	if #MovementGuard.Log > 50 then table.remove(MovementGuard.Log, 1) end
	warn(string.format("[MovementGuard] %s %s corrected: %s", kind, who, reason))
end

-- Ground under the robot: the server's own sphere cast, so ledges and thin rails count. Humanoid.FloorMaterial is not
-- used: the robot's owner computes it (with it in the check, a hovering robot went unflagged in the first playtest).
-- Returns the distance to it, or nil when nothing is within GROUND_RAY.
local function groundBelow(c: Model, root: BasePart): number?
	local params = RaycastParams.new()
	params.FilterType = Enum.RaycastFilterType.Exclude
	params.FilterDescendantsInstances = { c }
	local hit = workspace:Spherecast(root.Position, 1.2, Vector3.new(0, -GROUND_RAY, 0), params)
	return hit and hit.Distance
end

function MovementGuard.Grace(character: Model, seconds: number)
	character:SetAttribute("PZ_MoveGraceUntil", workspace:GetServerTimeNow() + seconds)
end

function MovementGuard.WingEnergy(player: Player): number
	return wing[player] or MovementRules.Flight.MAX_ENERGY
end

function MovementGuard.CanTakeOff(player: Player): boolean
	return MovementRules.canTakeOff(MovementGuard.WingEnergy(player))
end

-- robots ----------------------------------------------------------------------------------------------------------
local function stepCharacter(player: Player, dt: number)
	local c = player.Character
	local root = c and c:FindFirstChild("HumanoidRootPart") :: BasePart?
	local hum = c and c:FindFirstChildOfClass("Humanoid")
	local st = chars[player]
	if not st then st = { strikes = 0, airTime = 0 }; chars[player] = st end
	if not c or not root or not hum or hum.Health <= 0 then st.prev, st.valid, st.ground = nil, nil, nil; return end

	local flying = c:GetAttribute("PZ_WingsOut") == true
	local below = groundBelow(c, root)
	local grounded = below ~= nil
	local standing = below ~= nil and below <= STANDING -- a place a correction can safely put it back

	-- wing energy
	local e = MovementRules.wingEnergy(MovementGuard.WingEnergy(player), dt, flying, grounded and not flying)
	wing[player] = e
	player:SetAttribute("PZ_WingEnergy", math.floor(e + 0.5))
	if flying and e <= 0 then c:SetAttribute("PZ_WingsOut", false) end

	local pos = root.Position
	local grace = (c:GetAttribute("PZ_MoveGraceUntil") or 0) :: number
	if root.Anchored or hum.SeatPart or workspace:GetServerTimeNow() < grace or not st.prev then
		st.prev, st.valid, st.strikes, st.airTime = pos, pos, 0, 0
		if standing then st.ground = pos end
		return
	end
	local prev = st.prev :: Vector3
	st.prev = pos

	local ok, reason = MovementRules.checkStep(prev, pos, dt, MovementRules.characterLimits(hum.WalkSpeed, flying))
	local hard = reason == "teleport"
	if ok and not MovementRules.inBox(pos, MovementRules.WORLD) then ok, reason, hard = false, "out of bounds", true end
	if ok and flying and pos.Y > MovementRules.FLIGHT_CEILING then ok, reason, hard = false, "above flight ceiling", true end
	-- hovering without wings: airborne and not coming down
	if not flying and not grounded and pos.Y >= prev.Y - 0.5 then st.airTime += dt else st.airTime = 0 end
	if ok and st.airTime >= HOVER_TIME then ok, reason, hard = false, "hovering without wings", true end

	if ok then
		st.valid, st.strikes = pos, 0
		if standing then st.ground = pos end
		return
	end
	st.strikes += 1
	if hard or st.strikes >= MovementRules.STRIKES then
		c:SetAttribute("PZ_WingsOut", false)
		root.AssemblyLinearVelocity = Vector3.zero
		local back = (if reason == "hovering without wings" or flying then (st.ground or st.valid or prev) else (st.valid or prev)) :: Vector3
		root.CFrame = CFrame.new(back) * (root.CFrame - root.Position)
		st.prev, st.strikes, st.airTime = back, 0, 0
		note("robot", player.Name, reason or "?")
	end
end

-- vehicles --------------------------------------------------------------------------------------------------------
function MovementGuard.RegisterVehicle(body: BasePart, seat: VehicleSeat)
	table.insert(vehicles, { body = body, seat = seat, strikes = 0, corrections = {}, holdUntil = 0 })
end

local function yaw(cf: CFrame): number
	local look = cf.LookVector
	return math.atan2(-look.X, -look.Z)
end

local function stepVehicle(v: VehState, dt: number)
	local body, seat = v.body, v.seat
	if not body.Parent then return end
	local hum = seat.Occupant
	local driver = hum and Players:GetPlayerFromCharacter(hum.Parent)
	local now = os.clock()
	if v.holdUntil > 0 and now >= v.holdUntil then
		v.holdUntil = 0
		if driver then pcall(function() body:SetNetworkOwner(driver) end) end
	end
	local cf = body.CFrame
	if not driver or v.holdUntil > 0 or not v.prev then
		v.prev, v.valid, v.strikes = cf, cf, 0
		return
	end
	local last = v.prev :: CFrame
	v.prev = cf
	local ok, reason = MovementRules.checkStep(last.Position, cf.Position, dt, MovementRules.vehicleLimits())
	local hard = reason == "teleport"
	if ok and not MovementRules.yawOk(yaw(last), yaw(cf), dt) then ok, reason = false, "turn rate" end
	if ok and not MovementRules.inBox(cf.Position, MovementRules.VEHICLE_ZONE) then ok, reason, hard = false, "out of zone", true end
	if ok then
		v.valid, v.strikes = cf, 0
		return
	end
	v.strikes += 1
	if not (hard or v.strikes >= MovementRules.STRIKES) then return end
	-- correction: server takes the physics, puts the vehicle back and stops it
	pcall(function() body:SetNetworkOwner(nil) end)
	local lv = body:FindFirstChild("DriveVelocity") :: LinearVelocity?
	local av = body:FindFirstChild("DriveTurn") :: AngularVelocity?
	if lv then lv.VectorVelocity = Vector3.zero end
	if av then av.AngularVelocity = Vector3.zero end
	body.AssemblyLinearVelocity = Vector3.zero
	body.AssemblyAngularVelocity = Vector3.zero
	local back = (v.valid or last) :: CFrame
	body.CFrame = back
	v.prev, v.strikes, v.holdUntil = back, 0, now + OWNER_HOLD
	note("vehicle", (driver :: Player).Name, reason or "?")
	table.insert(v.corrections, now)
	while v.corrections[1] and now - v.corrections[1] > EJECT_WINDOW do table.remove(v.corrections, 1) end
	if #v.corrections >= EJECT_AFTER then
		v.corrections = {}
		v.holdUntil = 0
		local weld = seat:FindFirstChild("SeatWeld")
		if weld then weld:Destroy() end
		note("vehicle", (driver :: Player).Name, "driver unseated after repeated corrections")
	end
end

function MovementGuard.Start()
	Players.PlayerRemoving:Connect(function(p) chars[p] = nil; wing[p] = nil end)
	local function onPlayer(p: Player)
		p:SetAttribute("PZ_WingEnergy", MovementRules.Flight.MAX_ENERGY)
		p.CharacterAdded:Connect(function()
			chars[p] = nil
			wing[p] = MovementRules.Flight.MAX_ENERGY
		end)
	end
	Players.PlayerAdded:Connect(onPlayer)
	for _, p in ipairs(Players:GetPlayers()) do onPlayer(p) end
	task.spawn(function()
		local t0 = os.clock()
		while true do
			task.wait(MovementRules.SAMPLE)
			local t1 = os.clock()
			local dt = t1 - t0 -- the real interval (server frames can stretch it)
			t0 = t1
			for _, p in ipairs(Players:GetPlayers()) do
				local ok, err = pcall(stepCharacter, p, dt)
				if not ok then warn("[MovementGuard] " .. tostring(err)) end
			end
			for _, v in ipairs(vehicles) do
				local ok, err = pcall(stepVehicle, v, dt)
				if not ok then warn("[MovementGuard] " .. tostring(err)) end
			end
		end
	end)
end

return MovementGuard
