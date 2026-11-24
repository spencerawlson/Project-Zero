--!strict
-- MissionHUD (client): shows what MissionService sends on ReplicatedStorage.PZ_Remotes.Mission. Display only.
--   ("objective", info | nil)  objective panel (top left) + waypoint markers (cyan: objective, amber: optional)
--   ("dialogue", beats)        non-blocking subtitles at the bottom, queued (same beat kinds as ActivationScript)
--   ("complete", info)         "mission complete" banner
-- Sits under the activation cinematic (lower DisplayOrder), so it never covers that scene.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("Mission") :: RemoteEvent

local CYAN = Color3.fromRGB(0, 230, 220)
local AMBER = Color3.fromRGB(255, 196, 120)
local RED = Color3.fromRGB(255, 60, 70)
local WHITE = Color3.fromRGB(235, 240, 245)
local PANEL = Color3.fromRGB(12, 16, 22)

local function make(className: string, props: { [string]: any }, parent: Instance?): any
	local inst = Instance.new(className)
	for k, v in pairs(props) do (inst :: any)[k] = v end
	if parent then inst.Parent = parent end
	return inst
end

local gui = make("ScreenGui", { Name = "PZ_Mission", ResetOnSpawn = false, DisplayOrder = 10, IgnoreGuiInset = false },
	player:WaitForChild("PlayerGui"))

-- objective panel ------------------------------------------------------------------------------------------
local panel = make("Frame", { Name = "Objective", Position = UDim2.fromOffset(16, 16), Size = UDim2.fromOffset(330, 0),
	AutomaticSize = Enum.AutomaticSize.Y, BackgroundColor3 = PANEL, BackgroundTransparency = 0.25, Visible = false }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, panel)
make("UIPadding", { PaddingTop = UDim.new(0, 10), PaddingBottom = UDim.new(0, 10), PaddingLeft = UDim.new(0, 12), PaddingRight = UDim.new(0, 12) }, panel)
make("UIListLayout", { Padding = UDim.new(0, 4), SortOrder = Enum.SortOrder.LayoutOrder }, panel)
make("UIStroke", { Color = CYAN, Transparency = 0.6, Thickness = 1 }, panel)
local function label(order: number, font: Enum.Font, size: number, colour: Color3): TextLabel
	return make("TextLabel", { LayoutOrder = order, Size = UDim2.new(1, 0, 0, 0), AutomaticSize = Enum.AutomaticSize.Y,
		BackgroundTransparency = 1, Font = font, TextSize = size, TextColor3 = colour, TextWrapped = true,
		TextXAlignment = Enum.TextXAlignment.Left, Text = "" }, panel)
end
local heading = label(1, Enum.Font.GothamBold, 12, CYAN); heading.Text = "MISSION  ·  THE AWAKENING"
local title = label(2, Enum.Font.GothamBold, 20, WHITE)
local hint = label(3, Enum.Font.Gotham, 14, Color3.fromRGB(190, 200, 210))
local optTitle = label(4, Enum.Font.GothamBold, 14, AMBER)
local optHint = label(5, Enum.Font.Gotham, 13, Color3.fromRGB(210, 190, 160))

-- waypoint markers ----------------------------------------------------------------------------------------
local function marker(colour: Color3)
	local bb = make("BillboardGui", { Name = "PZ_Waypoint", Size = UDim2.fromOffset(60, 52), AlwaysOnTop = true,
		LightInfluence = 0, StudsOffset = Vector3.new(0, 7, 0), Enabled = false }, gui)
	local diamond = make("Frame", { AnchorPoint = Vector2.new(0.5, 0), Position = UDim2.new(0.5, 0, 0, 2), Size = UDim2.fromOffset(18, 18),
		Rotation = 45, BackgroundColor3 = colour, BorderSizePixel = 0 }, bb)
	make("UIStroke", { Color = Color3.new(0, 0, 0), Thickness = 1.5, Transparency = 0.3 }, diamond)
	local dist = make("TextLabel", { Position = UDim2.new(0, 0, 0, 26), Size = UDim2.new(1, 0, 0, 22), BackgroundTransparency = 1,
		Font = Enum.Font.GothamBold, TextSize = 14, TextColor3 = colour, TextStrokeTransparency = 0.3, Text = "" }, bb)
	return { gui = bb, dist = dist }
end
local main, opt = marker(CYAN), marker(AMBER)
RunService.RenderStepped:Connect(function()
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	for _, m in ipairs({ main, opt }) do
		local a = m.gui.Adornee :: BasePart?
		if m.gui.Enabled and root and a then
			m.dist.Text = tostring(math.floor((a.Position - root.Position).Magnitude)) .. " studs"
		end
	end
end)

local function setObjective(info: any)
	if not info then
		panel.Visible = false; main.gui.Enabled = false; opt.gui.Enabled = false
		return
	end
	panel.Visible = true
	title.Text = info.title; hint.Text = info.hint
	main.gui.Adornee = info.target; main.gui.Enabled = info.target ~= nil
	if info.optional then
		optTitle.Visible, optHint.Visible = true, true
		optTitle.Text = info.optional.title; optHint.Text = info.optional.hint
		opt.gui.Adornee = info.optional.target; opt.gui.Enabled = info.optional.target ~= nil
	else
		optTitle.Visible, optHint.Visible = false, false
		opt.gui.Enabled = false
	end
	panel.BackgroundTransparency = 0
	TweenService:Create(panel, TweenInfo.new(0.8), { BackgroundTransparency = 0.25 }):Play()
end

-- dialogue -------------------------------------------------------------------------------------------------
local box = make("Frame", { Name = "Dialogue", AnchorPoint = Vector2.new(0.5, 1), Position = UDim2.new(0.5, 0, 1, -24),
	Size = UDim2.new(0.6, 0, 0, 86), BackgroundColor3 = PANEL, BackgroundTransparency = 0.2, Visible = false }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, box)
make("UISizeConstraint", { MaxSize = Vector2.new(820, 120) }, box)
local speaker = make("TextLabel", { Position = UDim2.fromOffset(16, 8), Size = UDim2.new(1, -32, 0, 20), BackgroundTransparency = 1,
	Font = Enum.Font.GothamBold, TextSize = 15, TextColor3 = CYAN, TextXAlignment = Enum.TextXAlignment.Left, Text = "" }, box)
local line = make("TextLabel", { Position = UDim2.fromOffset(16, 30), Size = UDim2.new(1, -32, 1, -38), BackgroundTransparency = 1,
	Font = Enum.Font.Gotham, TextSize = 18, TextColor3 = WHITE, TextWrapped = true, TextXAlignment = Enum.TextXAlignment.Left,
	TextYAlignment = Enum.TextYAlignment.Top, Text = "" }, box)
local queue: { any } = {}
local talking = false
local function playQueue()
	if talking then return end
	talking = true
	while #queue > 0 do
		local b = table.remove(queue, 1)
		box.Visible = true
		local colour = if b.kind == "censored" then RED elseif b.kind == "memory" then AMBER elseif b.kind == "system" then CYAN else WHITE
		speaker.Text = b.speaker or ""
		speaker.TextColor3 = if b.kind == "censored" then RED elseif b.kind == "memory" then AMBER else CYAN
		line.TextColor3 = colour
		line.Font = if b.kind == "system" or b.kind == "censored" then Enum.Font.Code else Enum.Font.Gotham
		line.Text = b.text
		line.MaxVisibleGraphemes = 0
		local n = utf8.len(b.text) or #b.text
		local t0 = os.clock()
		while os.clock() - t0 < b.seconds do
			line.MaxVisibleGraphemes = math.min(n, math.floor((os.clock() - t0) / (b.seconds * 0.5) * n))
			RunService.RenderStepped:Wait()
		end
		line.MaxVisibleGraphemes = -1
	end
	box.Visible = false
	talking = false
end

-- completion banner ----------------------------------------------------------------------------------------
local function banner()
	local f = make("TextLabel", { AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.3), Size = UDim2.fromOffset(640, 70),
		BackgroundColor3 = PANEL, BackgroundTransparency = 0.15, Font = Enum.Font.GothamBold, TextSize = 30, TextColor3 = CYAN,
		Text = "MISSION COMPLETE  ·  THE AWAKENING", TextTransparency = 1 }, gui)
	make("UICorner", { CornerRadius = UDim.new(0, 6) }, f)
	TweenService:Create(f, TweenInfo.new(0.8), { TextTransparency = 0 }):Play()
	task.delay(6, function()
		TweenService:Create(f, TweenInfo.new(1.5), { TextTransparency = 1, BackgroundTransparency = 1 }):Play()
		task.delay(1.6, function() f:Destroy() end)
	end)
end

remote.OnClientEvent:Connect(function(kind, info)
	if kind == "objective" then
		setObjective(info)
	elseif kind == "dialogue" and type(info) == "table" then
		for _, b in ipairs(info) do table.insert(queue, b) end
		task.spawn(playQueue)
	elseif kind == "complete" then
		banner()
	end
end)
