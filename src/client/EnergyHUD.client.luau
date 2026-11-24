--!strict
-- EnergyHUD (client): the robot's energy (EnergyService, docs/NEXUS_01_CITY.md §2). Display and requests only.
--   * Energy bar on the right edge, above the credits: cyan, amber when low, pulsing green while charging.
--   * Energy cells: a "CELL ×n" button (or R / gamepad X) asks the server to use one (PZ_Remotes.Energy "useCell").
--   * Low energy (< 20): a short warning line and a marker over the Charge Bay.
-- Reads player attributes PZ_Energy, PZ_Charging, PZ_EnergyCells (set by the server).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")

local EnergyRules = require(ReplicatedStorage.Shared.EnergyRules)

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("Energy") :: RemoteEvent

local PANEL = Color3.fromRGB(12, 16, 22)
local CYAN = Color3.fromHex("#22D3EE")
local AMBER = Color3.fromRGB(255, 170, 70)
local GREEN = Color3.fromRGB(90, 230, 140)
local WHITE = Color3.fromRGB(235, 240, 245)

local function make(className: string, props: { [string]: any }, parent: Instance?): any
	local inst = Instance.new(className)
	for k, v in pairs(props) do (inst :: any)[k] = v end
	if parent then inst.Parent = parent end
	return inst
end

local gui = make("ScreenGui", { Name = "PZ_Energy", ResetOnSpawn = false, DisplayOrder = 12 }, player:WaitForChild("PlayerGui"))
local bar = make("Frame", { Name = "Energy", AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -16, 0.4, -82),
	Size = UDim2.fromOffset(150, 32), BackgroundColor3 = PANEL, BackgroundTransparency = 0.2 }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, bar)
local fill = make("Frame", { Position = UDim2.fromOffset(4, 4), Size = UDim2.new(1, -8, 1, -8), BackgroundColor3 = CYAN,
	BackgroundTransparency = 0.55, BorderSizePixel = 0 }, bar)
make("UICorner", { CornerRadius = UDim.new(0, 4) }, fill)
local label = make("TextLabel", { Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, Font = Enum.Font.GothamBold, TextSize = 14,
	TextColor3 = WHITE, Text = "", ZIndex = 2 }, bar)
local cellBtn = make("TextButton", { Name = "Cell", AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -172, 0.4, -82),
	Size = UDim2.fromOffset(100, 32), BackgroundColor3 = PANEL, BackgroundTransparency = 0.2, Font = Enum.Font.GothamBold,
	TextSize = 13, TextColor3 = AMBER, Text = "", Visible = false }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, cellBtn)
local warnLine = make("TextLabel", { AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -16, 0.4, -104), Size = UDim2.fromOffset(240, 18),
	BackgroundTransparency = 1, Font = Enum.Font.GothamBold, TextSize = 13, TextColor3 = AMBER, TextXAlignment = Enum.TextXAlignment.Right,
	TextStrokeTransparency = 0.4, Text = "LOW ENERGY  ·  CHARGE BAY MARKED", Visible = false }, gui)

-- marker over the Charge Bay when low
local marker = make("BillboardGui", { Name = "PZ_ChargeMarker", Size = UDim2.fromOffset(120, 40), AlwaysOnTop = true, LightInfluence = 0,
	StudsOffset = Vector3.new(0, 9, 0), Enabled = false }, gui)
make("TextLabel", { Size = UDim2.fromScale(1, 1), BackgroundTransparency = 1, Font = Enum.Font.GothamBold, TextSize = 14, TextColor3 = GREEN,
	TextStrokeTransparency = 0.3, Text = "⚡ CHARGE BAY" }, marker)
task.spawn(function()
	local city = workspace:WaitForChild("PZ_FoundersQuarter", 60)
	local pad = city and city:WaitForChild("Anchors"):WaitForChild("ChargePad", 30)
	if pad then marker.Adornee = pad end
end)

local function useCell()
	remote:FireServer("useCell")
end
cellBtn.MouseButton1Click:Connect(useCell)
UserInputService.InputBegan:Connect(function(input, processed)
	if processed then return end
	if input.KeyCode == Enum.KeyCode.R or input.KeyCode == Enum.KeyCode.ButtonX then useCell() end
end)

RunService.RenderStepped:Connect(function()
	local e = player:GetAttribute("PZ_Energy")
	if type(e) ~= "number" then bar.Visible = false return end
	bar.Visible = true
	local charging = player:GetAttribute("PZ_Charging") == true
	local low = EnergyRules.isLow(e)
	fill.Size = UDim2.new(e / EnergyRules.MAX, -8 * e / EnergyRules.MAX, 1, -8)
	fill.BackgroundColor3 = if charging then GREEN elseif low then AMBER else CYAN
	fill.BackgroundTransparency = if charging then 0.35 + 0.2 * math.sin(os.clock() * 6) else 0.55
	label.Text = (if charging then "CHARGING  " else "ENERGY  ") .. tostring(e) .. "%"
	local cells = player:GetAttribute("PZ_EnergyCells")
	cellBtn.Visible = type(cells) == "number" and cells > 0
	cellBtn.Text = ("CELL ×%s [R]"):format(tostring(cells))
	warnLine.Visible = low and not charging
	marker.Enabled = low and not charging
end)
