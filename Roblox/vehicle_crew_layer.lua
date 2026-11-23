-- Vehicle crew layer builder (Roblox Studio command bar or MCP execute_luau, Edit mode).
-- Adds the inner layer that lets robots get into a supplied (Meshy) vehicle hull:
--   seats sized for the largest robot (crew standard, 4.8 wide), a Board prompt, and a server script that seats
--   the boarding robot in the first free seat (server decides; the client only presses the prompt).
-- Seat positions come from Blender/scripts/pz_vehicle_prep.py (report JSON, "chosen" layout): each seat's
-- seated envelope for the largest robot (Patch 4.4 wide, Sentinel 7.5 tall) was tested clear of the hull.
--
-- Usage: set CONFIG below, run. Prep space is centred, length along X, Z up; Studio = (X, Z, -Y) after the model
-- is placed with its bounding-box centre at CONFIG.centre (Y of the centre = half the model height).

local CONFIG = {
	model = "PZ_TitanRover",                  -- Workspace child
	centre = Vector3.new(-32, 0, 36),         -- where the bounding-box centre sits (Y filled in from the model)
	face = 1,                                  -- +1: occupants look toward +X, -1: toward -X (front of the vehicle)
	seats = {},                                -- { {x, y, floor_z, "Name"}, ... } from the prep report, front first
	board = {x = -20, y = 0, z = 0},           -- boarding point in prep space (z above ground)
	label = "Vehicle",
}

local function build(cfg)
	local CHS = game:GetService("ChangeHistoryService")
	local CS = game:GetService("CollectionService")
	local m = workspace:FindFirstChild(cfg.model)
	assert(m, "model not found: " .. cfg.model)
	local cf, size = m:GetBoundingBox()
	local c = Vector3.new(cfg.centre.X, size.Y / 2, cfg.centre.Z)
	local function W(x, y, z) return Vector3.new(c.X + x, z, c.Z - y) end
	local old = m:FindFirstChild("CrewLayer"); if old then old:Destroy() end
	local layer = Instance.new("Model"); layer.Name = "CrewLayer"
	layer:SetAttribute("Standard", "crew standard: seat 4.8 wide, largest robot 4.4 x 7.5 (seated entry via prompt)")
	local look = Vector3.xAxis * cfg.face
	for i, s in ipairs(cfg.seats) do
		local seat = Instance.new("Seat"); seat.Name = "Seat_" .. (s[4] or i); seat.Anchored = true
		seat.Size = Vector3.new(2.4, 1.6, 4.8)
		local p = W(s[1], s[2], s[3] + 0.8)
		seat.CFrame = CFrame.lookAt(p, p + look)
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
	local sc = Instance.new("Script"); sc.Name = "BoardServer"
	sc.Source = [[
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
	sc.Parent = layer
	layer.Parent = m
	CHS:SetWaypoint("Add crew layer to " .. cfg.model)
	return string.format("%s: %d seats, board point %s", cfg.model, #cfg.seats, tostring(entry.Position))
end

return build(CONFIG)
