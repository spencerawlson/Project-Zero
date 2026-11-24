--!strict
-- VehicleService: basic driving (master plan Phase 2, "basic transportation"; owner order 2026-11-24).
-- A crewed vehicle (Model in workspace with a CrewLayer, see Roblox/vehicles_in_studio.md) with the attribute
-- PZ_Drivable = true becomes a car you can drive, arcade style:
--   * Body: an invisible box under the hull ("DriveBody") carries the physics; every other part of the vehicle is
--     welded to it, unanchored, massless and non-colliding. Low friction; walls and buildings stop it.
--   * Driver: a VehicleSeat ("PZ_DriverSeat") replaces crew seat Order 1 (that Seat is disabled and its chair re-welded).
--     The vehicle's Board prompt now seats the first robot as driver and the next ones as passengers (the vehicle's
--     own BoardServer script is disabled for drivable vehicles).
--   * Motion: a LinearVelocity (horizontal only, gravity untouched) and an AngularVelocity (yaw) on DriveBody. The
--     driver's client owns the physics and sets them from W/A/S/D (VehicleClient); with no driver the server brakes.
-- Forward is the driver seat's facing. Speeds: Shared.MovementRules.Vehicle; the server checks them (MovementGuard).

local Players = game:GetService("Players")

local MovementGuard = require(script.Parent.MovementGuard)

local VehicleService = {}

local function cabinOf(v: Model): Instance?
	return v:FindFirstChild("Cabin")
end

local function weldAll(model: Model, body: BasePart)
	for _, d in ipairs(model:GetDescendants()) do
		if d:IsA("BasePart") and d ~= body then
			-- parts already welded to a seat (cabin chairs, plates) only need to be unanchored; the seat itself is welded below
			local hasJoint = false
			for _, j in ipairs(d:GetChildren()) do if j:IsA("Weld") or j:IsA("WeldConstraint") then hasJoint = true end end
			d.Anchored = false; d.Massless = true
			if not (d:IsA("Seat") or d:IsA("VehicleSeat")) then d.CanCollide = false end
			if not hasJoint then
				local w = Instance.new("WeldConstraint"); w.Part0 = body; w.Part1 = d; w.Parent = d
			end
		end
	end
end

local function setup(v: Model)
	local crew = v:FindFirstChild("CrewLayer")
	if not crew or v:FindFirstChild("DriveBody") then return end
	local seats: { Seat } = {}
	for _, s in ipairs(crew:GetChildren()) do if s:IsA("Seat") then table.insert(seats, s) end end
	table.sort(seats, function(a, b) return (a:GetAttribute("Order") or 0) < (b:GetAttribute("Order") or 0) end)
	local first = seats[1]
	if not first then return end
	-- the vehicle's own boarding script stays off: this service boards drivable vehicles
	local board = crew:FindFirstChild("BoardServer")
	if board and board:IsA("Script") then board.Enabled = false end

	-- body: an invisible box over the hull's footprint (world-axis extents of the hull meshes), resting on the ground
	local mn, mx = Vector3.new(math.huge, math.huge, math.huge), Vector3.new(-math.huge, -math.huge, -math.huge)
	for _, d in ipairs(v:GetDescendants()) do
		if d:IsA("MeshPart") and not d:IsDescendantOf(crew) and not (cabinOf(v) and d:IsDescendantOf(cabinOf(v) :: Instance)) then
			for _, sx in ipairs({ -0.5, 0.5 }) do for _, sy in ipairs({ -0.5, 0.5 }) do for _, sz in ipairs({ -0.5, 0.5 }) do
				local p = d.CFrame:PointToWorldSpace(d.Size * Vector3.new(sx, sy, sz))
				mn = Vector3.new(math.min(mn.X, p.X), math.min(mn.Y, p.Y), math.min(mn.Z, p.Z))
				mx = Vector3.new(math.max(mx.X, p.X), math.max(mx.Y, p.Y), math.max(mx.Z, p.Z))
			end end end
		end
	end
	local centre, ext = (mn + mx) / 2, mx - mn
	local look = (first.CFrame.LookVector * Vector3.new(1, 0, 1)).Unit
	local bottom = mn.Y + 1.05
	local bodyCf = CFrame.lookAt(Vector3.new(centre.X, bottom, centre.Z), Vector3.new(centre.X, bottom, centre.Z) + look)
	local along = math.abs(look.X) > 0.7 -- the vehicle's length runs along world X
	local body = Instance.new("Part")
	body.Name = "DriveBody"; body.Transparency = 1; body.CanCollide = true; body.CanQuery = false
	-- body frame: X = right (width), Z = forward (length)
	body.Size = if along then Vector3.new(ext.Z * 0.9, 2, ext.X * 0.92) else Vector3.new(ext.X * 0.9, 2, ext.Z * 0.92)
	body.CFrame = bodyCf
	body.CustomPhysicalProperties = PhysicalProperties.new(2, 0.05, 0, 100, 1)
	body.Parent = v

	-- driver seat: a VehicleSeat on crew seat 1 (the old Seat is disabled; its chair moves to the new seat)
	local driver = Instance.new("VehicleSeat")
	driver.Name = "PZ_DriverSeat"; driver.Size = first.Size; driver.CFrame = first.CFrame; driver.Transparency = 1
	driver.MaxSpeed = 0; driver.Torque = 0; driver.TurnSpeed = 0; driver.HeadsUpDisplay = false
	driver.Parent = crew
	first.Disabled = true
	local cabin = v:FindFirstChild("Cabin")
	if cabin then
		for _, d in ipairs(cabin:GetDescendants()) do
			if d:IsA("Weld") and d.Part0 == first then
				local p1 = d.Part1 :: BasePart
				d.Part0 = driver; d.C0 = driver.CFrame:ToObjectSpace(p1.CFrame)
			end
		end
	end

	weldAll(v, body)
	body.Anchored = false

	-- motion constraints, driven by the driver's client
	local att = Instance.new("Attachment"); att.Name = "DriveAttachment"; att.Parent = body
	local lv = Instance.new("LinearVelocity")
	lv.Name = "DriveVelocity"; lv.Attachment0 = att; lv.RelativeTo = Enum.ActuatorRelativeTo.World
	lv.ForceLimitMode = Enum.ForceLimitMode.PerAxis; lv.MaxAxesForce = Vector3.new(1e6, 0, 1e6) -- gravity stays free
	lv.VectorVelocity = Vector3.zero; lv.Parent = body
	local av = Instance.new("AngularVelocity")
	av.Name = "DriveTurn"; av.Attachment0 = att; av.RelativeTo = Enum.ActuatorRelativeTo.World
	av.MaxTorque = 1e7; av.AngularVelocity = Vector3.zero; av.Parent = body
	v:SetAttribute("PZ_DriveReady", true)
	MovementGuard.RegisterVehicle(body, driver) -- server checks on the driver's motion (audit step 4)

	local function brake()
		lv.VectorVelocity = Vector3.zero; av.AngularVelocity = Vector3.zero
	end
	driver:GetPropertyChangedSignal("Occupant"):Connect(function()
		local hum = driver.Occupant
		local player = hum and Players:GetPlayerFromCharacter(hum.Parent)
		if player then
			pcall(function() body:SetNetworkOwner(player) end)
		else
			brake()
			pcall(function() body:SetNetworkOwner(nil) end)
		end
	end)
	pcall(function() body:SetNetworkOwner(nil) end)

	-- boarding: driver first, then passengers
	local point = crew:FindFirstChild("BoardPoint")
	local prompt = point and point:FindFirstChildOfClass("ProximityPrompt")
	if prompt then
		prompt.ActionText = "Board"
		prompt.Triggered:Connect(function(player)
			local char = player.Character
			local hum = char and char:FindFirstChildOfClass("Humanoid")
			local root = char and char:FindFirstChild("HumanoidRootPart") :: BasePart?
			if not hum or not root or hum.Health <= 0 or hum.SeatPart then return end
			if (root.Position - (point :: BasePart).Position).Magnitude > prompt.MaxActivationDistance + 4 then return end
			if not driver.Occupant then driver:Sit(hum) return end
			for i = 2, #seats do
				if not seats[i].Occupant then seats[i]:Sit(hum) return end
			end
		end)
	end
end

function VehicleService.Start()
	for _, v in ipairs(workspace:GetChildren()) do
		if v:IsA("Model") and v:GetAttribute("PZ_Drivable") == true then
			local ok, err = pcall(setup, v)
			if not ok then warn("[Vehicle] " .. v.Name .. ": " .. tostring(err)) end
		end
	end
end

return VehicleService
