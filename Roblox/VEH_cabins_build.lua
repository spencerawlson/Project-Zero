-- Vehicle cabins (edit time). Run in Studio's Edit mode. Owner feedback 2026-11-24: inside a vehicle "it's only a
-- couple of blocks" and the hull was see-through from inside (Meshy hulls are a one-sided outer skin).
-- For every crewed vehicle (a Model in workspace with a CrewLayer, see Roblox/vehicles_in_studio.md):
--   * hull MeshParts render DoubleSided (no more see-through walls),
--   * each crew Seat keeps working but turns invisible, and the owner's Command Chair (ServerStorage.Props.PZ_CabinChair,
--     INT-15) is welded in its place, on a small mounting plate,
--   * the driver's seat (Order 1) gets the owner's Command Console (ServerStorage.Props.PZ_CabinConsole, INT-14) in front
--     of it, pulled back if the hull is close (ray check), skipped if there is no room,
--   * one soft cabin light.
-- Output: <vehicle>.Cabin (replaced on re-run). Chair/console parts are welded to the seat (unanchored, massless,
-- non-colliding), so they follow the vehicle when vehicles drive later.
-- CHAIR_YAW / CONSOLE_YAW: rotation that turns each model's front to face along the seat's look direction; set by eye.

local ServerStorage = game:GetService("ServerStorage")
local props = ServerStorage:WaitForChild("Props")
local CHAIR = props:FindFirstChild("PZ_CabinChair")
local CONSOLE = props:FindFirstChild("PZ_CabinConsole")
local CHAIR_YAW = 90  -- the chair model faces +X in its own frame (checked in Studio; a camera looking +Z has -X on its right)
local CONSOLE_YAW = 0  -- the console faces -Z in its own frame (checked in Studio)
local CUSHION = 1.9         -- chair cushion height above its base (studs, chair 4.2 tall)
local CONSOLE_AHEAD = 3.8   -- console distance in front of the driver's seat

local function weldTo(base: BasePart, model: Instance)
	local all = model:GetDescendants()
	table.insert(all, model) -- a single Part (plate, light) is welded too
	for _, d in ipairs(all) do
		if d:IsA("BasePart") then
			d.Anchored = false; d.Massless = true; d.CanCollide = false; d.CanQuery = false; d.CanTouch = false
			local w = Instance.new("Weld"); w.Part0 = base; w.Part1 = d; w.C0 = base.CFrame:ToObjectSpace(d.CFrame); w.Parent = d
		end
	end
end

local report = {}
for _, v in ipairs(workspace:GetChildren()) do
	local crew = v:IsA("Model") and v:FindFirstChild("CrewLayer")
	if crew then
		local old = v:FindFirstChild("Cabin"); if old then old:Destroy() end
		local cabin = Instance.new("Folder"); cabin.Name = "Cabin"; cabin.Parent = v
		for _, d in ipairs(v:GetDescendants()) do
			if d:IsA("MeshPart") and not d:IsDescendantOf(crew) then d.DoubleSided = true end
		end
		local hull = {}
		for _, d in ipairs(v:GetDescendants()) do if d:IsA("MeshPart") and not d:IsDescendantOf(cabin) then table.insert(hull, d) end end
		local params = RaycastParams.new(); params.FilterType = Enum.RaycastFilterType.Include; params.FilterDescendantsInstances = hull
		local sum, n, chairs, consoles = Vector3.zero, 0, 0, 0
		for _, seat in ipairs(crew:GetChildren()) do
			if seat:IsA("Seat") then
				seat.Transparency = 1
				local look = seat.CFrame.LookVector * Vector3.new(1, 0, 1)
				local top = seat.Position.Y + seat.Size.Y / 2
				local baseCf = CFrame.lookAt(Vector3.new(seat.Position.X, top - CUSHION, seat.Position.Z), Vector3.new(seat.Position.X, top - CUSHION, seat.Position.Z) + look)
				if CHAIR then
					local c = CHAIR:Clone(); c.Name = "Chair_" .. seat.Name
					c:PivotTo(baseCf * CFrame.Angles(0, math.rad(CHAIR_YAW), 0))
					c.Parent = cabin; weldTo(seat, c); chairs += 1
				end
				local plate = Instance.new("Part"); plate.Name = "MountPlate_" .. seat.Name
				plate.Size = Vector3.new(3.2, 0.3, 3.2); plate.CFrame = baseCf * CFrame.new(0, -0.15, 0)
				plate.Color = Color3.fromHex("#2B2F36"); plate.Material = Enum.Material.DiamondPlate
				plate.Parent = cabin; weldTo(seat, plate)
				if seat:GetAttribute("Order") == 1 and CONSOLE then
					-- room in front of the driver: ray at console height
					local origin = baseCf.Position + Vector3.new(0, 2.5, 0)
					local hit = workspace:Raycast(origin, look.Unit * (CONSOLE_AHEAD + 3), params)
					local dist = if hit then math.min(CONSOLE_AHEAD, (hit.Position - origin).Magnitude - 2.2) else CONSOLE_AHEAD
					if dist >= 2.4 then
						local k = CONSOLE:Clone(); k.Name = "DriverConsole"
						k:PivotTo(baseCf * CFrame.new(0, 0, -dist) * CFrame.Angles(0, math.rad(180 + CONSOLE_YAW), 0))
						k.Parent = cabin; weldTo(seat, k); consoles += 1
					end
				end
				sum += seat.Position; n += 1
			end
		end
		if n > 0 then
			local lp = Instance.new("Part"); lp.Name = "CabinLight"; lp.Size = Vector3.new(0.4, 0.4, 0.4); lp.Transparency = 1
			lp.CFrame = CFrame.new(sum / n + Vector3.new(0, 4.5, 0)); lp.Parent = cabin
			local l = Instance.new("PointLight"); l.Range = 16; l.Brightness = 0.9; l.Color = Color3.fromRGB(215, 232, 255); l.Shadows = false; l.Parent = lp
			local first = crew:FindFirstChildWhichIsA("Seat")
			if first then weldTo(first, lp) end
		end
		table.insert(report, ("%s: %d chairs, %d console"):format(v.Name, chairs, consoles))
	end
end
return table.concat(report, "\n")
