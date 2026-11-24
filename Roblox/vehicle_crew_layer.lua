-- Vehicle crew layer builder (Roblox Studio command bar or MCP execute_luau, Edit mode).
-- Places a supplied (Meshy) vehicle hull and adds the inner layer that lets robots get in:
--   seats sized for the largest robot (crew standard, 4.8 wide), a Board prompt, and a server script that seats
--   the boarding robot in the first free seat (server decides; the client only presses the prompt).
-- Seat positions come from Blender/scripts/pz_vehicle_prep.py (report JSON, "chosen" layout): each seat's
-- seated envelope for the largest robot (Patch 4.4 wide, Sentinel 7.5 tall) was tested clear of the hull.
--
-- IMPORTANT (found 2026-11-23): Roblox inserts each imported model with an arbitrary yaw. The imported content maps
-- prep space as local (-x, z, +y) rotated by the MeshParts' yaw, so align() first turns the model until the parts'
-- yaw is 180 degrees. Only then does prep (x, y, z) land at world (centre.X + x, z, centre.Z - y).
-- Every Meshy vehicle checked so far faces prep -X (face = -1); confirm by eye before building seats.
-- After building, run the enclosure check (rays from each seat must hit the hull in all six directions).

local CONFIG = {
	model = "PZ_TitanRover",                  -- Workspace child (inserted package)
	centre = Vector3.new(-32, 0, 36),         -- target X/Z of the world bounding-box centre; the model rests on Y = 0
	face = -1,                                 -- -1: occupants look toward -X (front), +1 toward +X
	seats = {},                                -- { {x, y, floor_z, "Name"}, ... } from the prep report, front first
	board = {x = 17.5, y = 0, z = 3},          -- boarding point in prep space (z above ground)
	label = "Vehicle",
}

local function worldAABB(m)
	local mn, mx = Vector3.new(math.huge, math.huge, math.huge), Vector3.new(-math.huge, -math.huge, -math.huge)
	for _, d in ipairs(m:GetDescendants()) do
		if d:IsA("MeshPart") then
			local h = d.Size / 2
			for _, sx in ipairs({-1, 1}) do for _, sy in ipairs({-1, 1}) do for _, sz in ipairs({-1, 1}) do
				local w = d.CFrame:PointToWorldSpace(Vector3.new(h.X * sx, h.Y * sy, h.Z * sz)); mn = mn:Min(w); mx = mx:Max(w)
			end end end
		end
	end
	return mn, mx
end

local function align(m, centre)
	for _, d in ipairs(m:GetDescendants()) do if d:IsA("BasePart") then d.Anchored = true end end
	local _, yaw = m:FindFirstChildWhichIsA("MeshPart", true).CFrame:ToOrientation()
	local mn, mx = worldAABB(m); local c = (mn + mx) / 2
	m:PivotTo(CFrame.new(c) * CFrame.Angles(0, math.rad(180) - yaw, 0) * CFrame.new(-c) * m:GetPivot())
	mn, mx = worldAABB(m); local c2 = (mn + mx) / 2
	m:PivotTo(m:GetPivot() + Vector3.new(centre.X - c2.X, -mn.Y, centre.Z - c2.Z))
end

local SERVER = [[
local layer = script.Parent
local prompt = layer.BoardPoint.BoardPrompt
local seats = {}
for _, s in ipairs(layer:GetChildren()) do if s:IsA("Seat") then table.insert(seats, s) end end
table.sort(seats, function(a, b) return a:GetAttribute("Order") < b:GetAttribute("Order") end)
prompt.Triggered:Connect(function(player)
	local char = player.Character
	local hum = char and char:FindFirstChildOfClass("Humanoid")
	local root = char and char:FindFirstChild("HumanoidRootPart")
	if not hum or not root or hum.Health <= 0 or hum.SeatPart then return end
	if (root.Position - prompt.Parent.Position).Magnitude > prompt.MaxActivationDistance + 2 then return end
	for _, seat in ipairs(seats) do
		if not seat.Occupant then seat:Sit(hum) return end
	end
end)
]]

local function build(cfg)
	local CS = game:GetService("CollectionService")
	local m = workspace:FindFirstChild(cfg.model)
	assert(m, "model not found: " .. cfg.model)
	align(m, cfg.centre)
	local c = cfg.centre
	local function W(x, y, z) return Vector3.new(c.X + x, z, c.Z - y) end
	local old = m:FindFirstChild("CrewLayer"); if old then old:Destroy() end
	local layer = Instance.new("Model"); layer.Name = "CrewLayer"
	layer:SetAttribute("Standard", "crew standard: seat 4.8 wide, largest robot 4.4 x 7.5 (seated entry via prompt)")
	for i, s in ipairs(cfg.seats) do
		local seat = Instance.new("Seat"); seat.Name = "Seat_" .. (s[4] or i); seat.Anchored = true
		seat.Size = Vector3.new(2.4, 1.6, 4.8)
		local p = W(s[1], s[2], s[3] + 0.8)
		seat.CFrame = CFrame.lookAt(p, p + Vector3.xAxis * cfg.face)
		seat.Color = Color3.fromHex("#E8731A"); seat.Material = Enum.Material.Fabric
		seat:SetAttribute("Order", i); seat.Parent = layer
	end
	local entry = Instance.new("Part"); entry.Name = "BoardPoint"; entry.Anchored = true; entry.CanCollide = false
	entry.Transparency = 1; entry.Size = Vector3.one; entry.Position = W(cfg.board.x, cfg.board.y, cfg.board.z)
	local prompt = Instance.new("ProximityPrompt"); prompt.Name = "BoardPrompt"
	prompt.ActionText = "Board"; prompt.ObjectText = cfg.label; prompt.MaxActivationDistance = 10
	prompt.RequiresLineOfSight = false; prompt.Parent = entry
	CS:AddTag(entry, "PZ_Prompt_Board")
	entry.Parent = layer
	local sc = Instance.new("Script"); sc.Name = "BoardServer"; sc.Source = SERVER; sc.Parent = layer
	layer.Parent = m
	-- enclosure check: from each seat, rays in all six directions must hit the hull
	local hull = {}
	for _, d in ipairs(m:GetDescendants()) do if d:IsA("MeshPart") then table.insert(hull, d) end end
	local params = RaycastParams.new(); params.FilterType = Enum.RaycastFilterType.Include; params.FilterDescendantsInstances = hull
	local open = {}
	for _, s in ipairs(layer:GetChildren()) do
		if s:IsA("Seat") then
			local o = s.Position + Vector3.new(0, 1.5, 0); local miss = 0
			for _, dir in ipairs({Vector3.xAxis, -Vector3.xAxis, Vector3.zAxis, -Vector3.zAxis, Vector3.yAxis, -Vector3.yAxis}) do
				if not workspace:Raycast(o, dir * 60, params) then miss += 1 end
			end
			if miss > 0 then table.insert(open, s.Name) end
		end
	end
	game:GetService("ChangeHistoryService"):SetWaypoint("Add crew layer to " .. cfg.model)
	return string.format("%s: %d seats, board point %s, %s", cfg.model, #cfg.seats, tostring(entry.Position),
		#open == 0 and "all seats enclosed" or ("NOT ENCLOSED: " .. table.concat(open, ", ")))
end

return build(CONFIG)
