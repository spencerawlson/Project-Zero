--!strict
-- ColourPicker (client): the "PAINT" button (right edge, 40 % down; the top-right corner is under Roblox's
-- player list, which swallowed clicks in the playtest) opens the robot colour palette (ChassisColors.PALETTE).
-- Choosing a swatch asks the server ("setColour", id) on PZ_Remotes.Appearance; the server validates, saves and
-- paints the robot, then confirms with ("colour", id), which moves the selection ring. Display and input only.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local ChassisColors = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("ChassisColors"))

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("Appearance") :: RemoteEvent

local PANEL = Color3.fromRGB(12, 16, 22)
local CYAN = Color3.fromRGB(0, 230, 220)
local WHITE = Color3.fromRGB(235, 240, 245)

local function make(className: string, props: { [string]: any }, parent: Instance?): any
	local inst = Instance.new(className)
	for k, v in pairs(props) do (inst :: any)[k] = v end
	if parent then inst.Parent = parent end
	return inst
end

local gui = make("ScreenGui", { Name = "PZ_ColourPicker", ResetOnSpawn = false, DisplayOrder = 11 }, player:WaitForChild("PlayerGui"))

local button = make("TextButton", { Name = "Paint", AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -16, 0.4, 0),
	Size = UDim2.fromOffset(112, 36), BackgroundColor3 = PANEL, BackgroundTransparency = 0.2, Font = Enum.Font.GothamBold,
	TextSize = 15, TextColor3 = WHITE, Text = "PAINT", AutoButtonColor = true }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, button)
local chip = make("Frame", { AnchorPoint = Vector2.new(0, 0.5), Position = UDim2.new(0, 10, 0.5, 0), Size = UDim2.fromOffset(16, 16),
	BackgroundColor3 = WHITE }, button)
make("UICorner", { CornerRadius = UDim.new(1, 0) }, chip)
make("UIStroke", { Color = Color3.new(0, 0, 0), Thickness = 1 }, chip)

local panel = make("Frame", { Name = "Palette", AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -16, 0.4, 44),
	Size = UDim2.fromOffset(272, 0), AutomaticSize = Enum.AutomaticSize.Y, BackgroundColor3 = PANEL, BackgroundTransparency = 0.15,
	Visible = false }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, panel)
make("UIStroke", { Color = CYAN, Transparency = 0.6 }, panel)
make("UIPadding", { PaddingTop = UDim.new(0, 10), PaddingBottom = UDim.new(0, 10), PaddingLeft = UDim.new(0, 10), PaddingRight = UDim.new(0, 10) }, panel)
make("UIListLayout", { Padding = UDim.new(0, 8), SortOrder = Enum.SortOrder.LayoutOrder }, panel)
make("TextLabel", { LayoutOrder = 1, Size = UDim2.new(1, 0, 0, 18), BackgroundTransparency = 1, Font = Enum.Font.GothamBold,
	TextSize = 13, TextColor3 = CYAN, TextXAlignment = Enum.TextXAlignment.Left, Text = "ROBOT COLOUR" }, panel)
local grid = make("Frame", { LayoutOrder = 2, Size = UDim2.new(1, 0, 0, 0), AutomaticSize = Enum.AutomaticSize.Y, BackgroundTransparency = 1 }, panel)
make("UIGridLayout", { CellSize = UDim2.fromOffset(44, 44), CellPadding = UDim2.fromOffset(6, 6), SortOrder = Enum.SortOrder.LayoutOrder }, grid)
local nameLabel = make("TextLabel", { LayoutOrder = 3, Size = UDim2.new(1, 0, 0, 18), BackgroundTransparency = 1, Font = Enum.Font.Gotham,
	TextSize = 14, TextColor3 = WHITE, TextXAlignment = Enum.TextXAlignment.Left, Text = "" }, panel)

local rings: { [string]: UIStroke } = {}
local current: string? = nil

local function select(id: string)
	current = id
	for k, ring in pairs(rings) do
		ring.Color = if k == id then CYAN else Color3.new(0, 0, 0)
		ring.Thickness = if k == id then 3 else 1
	end
	local e = ChassisColors.get(id)
	nameLabel.Text = e and e.name or ""
	chip.BackgroundColor3 = ChassisColors.color3(id)
	button.Text = "     PAINT"
end

for i, e in ipairs(ChassisColors.PALETTE) do
	local sw = make("TextButton", { Name = e.id, LayoutOrder = i, BackgroundColor3 = Color3.fromHex(e.hex), Text = "", AutoButtonColor = true }, grid)
	make("UICorner", { CornerRadius = UDim.new(0, 8) }, sw)
	rings[e.id] = make("UIStroke", { Color = Color3.new(0, 0, 0), Thickness = 1, ApplyStrokeMode = Enum.ApplyStrokeMode.Border }, sw)
	sw.MouseButton1Click:Connect(function()
		if e.id ~= current then
			remote:FireServer("setColour", e.id)
		end
	end)
	sw.MouseEnter:Connect(function() nameLabel.Text = e.name end)
	sw.MouseLeave:Connect(function()
		local c = current and ChassisColors.get(current)
		nameLabel.Text = c and c.name or ""
	end)
end

button.MouseButton1Click:Connect(function()
	panel.Visible = not panel.Visible
end)

remote.OnClientEvent:Connect(function(kind, id)
	if kind == "colour" and type(id) == "string" then
		select(id)
	end
end)

-- hide while the activation cinematic is on screen
local pg = player:WaitForChild("PlayerGui")
local function refresh()
	local busy = pg:FindFirstChild("PZ_Activation") ~= nil
	button.Visible = not busy
	if busy then panel.Visible = false end
end
pg.ChildAdded:Connect(refresh)
pg.ChildRemoved:Connect(refresh)
refresh()
