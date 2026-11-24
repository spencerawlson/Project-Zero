--!strict
-- ActivationCinematic (client): plays the first-activation scene when the server says so.
-- Server contract (StasisService): PZ_Remotes.Activation fires ("play", { podId, designation }) to this client
-- only; this script answers ("done") when the scene ends or is skipped. The server holds the pod closed until
-- then (with a timeout), and records the activation, MF-001 and the designation. Nothing here changes game state.
--
-- Presentation: letterbox bars, camera on the robot through the pod glass with a slow push-in, subtitles with a
-- typewriter reveal. Beat styles from ActivationScript: source (cyan), censored (ZERO: red glitch, flicker,
-- shake), memory (white flash, warm desaturated grade), system (monospace HUD line at the top).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local StarterGui = game:GetService("StarterGui")
local TweenService = game:GetService("TweenService")

local ActivationScript = require(ReplicatedStorage:WaitForChild("Shared"):WaitForChild("ActivationScript"))

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("Activation") :: RemoteEvent

local CYAN = Color3.fromRGB(0, 230, 220)
local RED = Color3.fromRGB(255, 60, 70)
local AMBER = Color3.fromRGB(255, 196, 120)
local WHITE = Color3.fromRGB(235, 240, 245)
local GLITCH_CHARS = "#$%&@!?/\\|<>01=+*" -- ASCII only: string.sub slices bytes, so multi-byte letters break

local playing = false

local function make(className: string, props: { [string]: any }, parent: Instance?): any
	local inst = Instance.new(className)
	for k, v in pairs(props) do
		(inst :: any)[k] = v
	end
	if parent then
		inst.Parent = parent
	end
	return inst
end

local function tween(inst: Instance, seconds: number, goal: { [string]: any }, style: Enum.EasingStyle?)
	local tw = TweenService:Create(inst, TweenInfo.new(seconds, style or Enum.EasingStyle.Sine), goal)
	tw:Play()
	return tw
end

local function buildGui()
	local gui = make("ScreenGui", { Name = "PZ_Activation", IgnoreGuiInset = true, ResetOnSpawn = false, DisplayOrder = 50 })
	local black = make("Frame", { Name = "Black", Size = UDim2.fromScale(1, 1), BackgroundColor3 = Color3.new(0, 0, 0), BorderSizePixel = 0, ZIndex = 10 }, gui)
	local flash = make("Frame", { Name = "Flash", Size = UDim2.fromScale(1, 1), BackgroundColor3 = Color3.new(1, 1, 1), BackgroundTransparency = 1, BorderSizePixel = 0, ZIndex = 9 }, gui)
	local top = make("Frame", { Name = "BarTop", Size = UDim2.fromScale(1, 0.11), BackgroundColor3 = Color3.new(0, 0, 0), BorderSizePixel = 0, ZIndex = 5 }, gui)
	local bottom = make("Frame", { Name = "BarBottom", AnchorPoint = Vector2.new(0, 1), Position = UDim2.fromScale(0, 1), Size = UDim2.fromScale(1, 0.2), BackgroundColor3 = Color3.new(0, 0, 0), BorderSizePixel = 0, ZIndex = 5 }, gui)
	local hud = make("TextLabel", {
		Name = "Hud", AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5), Size = UDim2.fromScale(0.94, 0.6),
		BackgroundTransparency = 1, Font = Enum.Font.Code, TextColor3 = CYAN, TextScaled = true, Text = "", ZIndex = 6,
	}, top)
	make("UITextSizeConstraint", { MaxTextSize = 20 }, hud)
	local speaker = make("TextLabel", {
		Name = "Speaker", Position = UDim2.fromScale(0.08, 0.1), Size = UDim2.fromScale(0.84, 0.22),
		BackgroundTransparency = 1, Font = Enum.Font.GothamBold, TextColor3 = CYAN, TextScaled = true,
		TextXAlignment = Enum.TextXAlignment.Left, Text = "", ZIndex = 6,
	}, bottom)
	make("UITextSizeConstraint", { MaxTextSize = 18 }, speaker)
	local line = make("TextLabel", {
		Name = "Line", Position = UDim2.fromScale(0.08, 0.34), Size = UDim2.fromScale(0.84, 0.5),
		BackgroundTransparency = 1, Font = Enum.Font.Gotham, TextColor3 = WHITE, TextScaled = true, TextWrapped = true,
		TextXAlignment = Enum.TextXAlignment.Left, TextYAlignment = Enum.TextYAlignment.Top, Text = "", ZIndex = 6,
	}, bottom)
	make("UITextSizeConstraint", { MaxTextSize = 26 }, line)
	local skip = make("TextButton", {
		Name = "Skip", AnchorPoint = Vector2.new(1, 1), Position = UDim2.new(1, -24, 1, -18), Size = UDim2.fromOffset(110, 34),
		BackgroundColor3 = Color3.fromRGB(20, 26, 32), BackgroundTransparency = 0.2, Font = Enum.Font.GothamBold,
		TextColor3 = WHITE, TextSize = 16, Text = "Skip  >>", AutoButtonColor = true, ZIndex = 8,
	}, gui)
	make("UICorner", { CornerRadius = UDim.new(0, 6) }, skip)
	gui.Parent = player:WaitForChild("PlayerGui")
	return { gui = gui, black = black, flash = flash, top = top, bottom = bottom, hud = hud, speaker = speaker, line = line, skip = skip }
end

-- Reveal text a character at a time over `seconds` (stops early when `cancelled()` turns true).
local function typewrite(label: TextLabel, text: string, seconds: number, cancelled: () -> boolean)
	label.Text = text
	label.MaxVisibleGraphemes = 0
	local n = utf8.len(text) or #text
	local t0 = os.clock()
	while not cancelled() do
		local k = math.floor((os.clock() - t0) / seconds * n)
		label.MaxVisibleGraphemes = math.min(k, n)
		if k >= n then
			break
		end
		RunService.RenderStepped:Wait()
	end
	label.MaxVisibleGraphemes = -1
end

local function glitch(label: TextLabel, text: string, seconds: number, cancelled: () -> boolean)
	local t0 = os.clock()
	while os.clock() - t0 < seconds and not cancelled() do
		local chars = {}
		for _, code in utf8.codes(text) do
			local c = utf8.char(code)
			if c ~= " " and math.random() < 0.45 then
				local i = math.random(1, #GLITCH_CHARS)
				c = GLITCH_CHARS:sub(i, i)
			end
			table.insert(chars, c)
		end
		label.Text = table.concat(chars)
		task.wait(0.05)
	end
	label.Text = text
end

local function play(info: { podId: string, designation: string })
	if playing then
		return
	end
	playing = true
	local character = player.Character
	local head = character and character:FindFirstChild("Head") :: BasePart?
	local root = character and character:FindFirstChild("HumanoidRootPart") :: BasePart?
	local camera = workspace.CurrentCamera
	local ui = buildGui()
	local skipped = false
	local function cancelled()
		return skipped
	end
	ui.skip.MouseButton1Click:Connect(function()
		skipped = true
	end)
	pcall(function()
		StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.All, false)
	end)
	local grade = make("ColorCorrectionEffect", { Name = "PZ_ActivationGrade" }, camera)

	-- Camera: in front of the robot, through the glass, slowly pushing in.
	local camTween: Tween? = nil
	if head and root then
		local facing = root.CFrame.LookVector
		local target = head.Position + Vector3.new(0, -0.4, 0)
		camera.CameraType = Enum.CameraType.Scriptable
		camera.CFrame = CFrame.lookAt(target + facing * 9 + Vector3.new(0, 0.6, 0), target)
		local total = ActivationScript.totalSeconds(ActivationScript.build(info.designation))
		camTween = tween(camera, total, { CFrame = CFrame.lookAt(target + facing * 4.8 + Vector3.new(0, 0.2, 0), target) }, Enum.EasingStyle.Linear)
	end

	tween(ui.black, 2.5, { BackgroundTransparency = 1 })
	for _, beat in ipairs(ActivationScript.build(info.designation)) do
		if skipped then
			break
		end
		local t0 = os.clock()
		ui.speaker.Text = beat.speaker or ""
		if beat.kind == "system" then
			ui.speaker.Text = ""
			ui.line.Text = ""
			ui.hud.TextColor3 = CYAN
			typewrite(ui.hud, beat.text, math.min(1.5, beat.seconds * 0.5), cancelled)
		elseif beat.kind == "source" then
			ui.speaker.TextColor3 = CYAN
			ui.line.TextColor3 = WHITE
			ui.line.Font = Enum.Font.Gotham
			typewrite(ui.line, beat.text, beat.seconds * 0.55, cancelled)
		elseif beat.kind == "censored" then
			ui.speaker.TextColor3 = RED
			ui.line.TextColor3 = RED
			ui.line.Font = Enum.Font.Code
			ui.flash.BackgroundColor3 = RED
			ui.flash.BackgroundTransparency = 0.6
			tween(ui.flash, 0.6, { BackgroundTransparency = 1 })
			grade.Saturation = -0.4
			grade.TintColor = Color3.fromRGB(255, 190, 190)
			local shakeUntil = os.clock() + 0.6
			local conn = RunService.RenderStepped:Connect(function()
				if os.clock() < shakeUntil and camera.CameraType == Enum.CameraType.Scriptable then
					camera.CFrame *= CFrame.new(math.random(-10, 10) / 100, math.random(-10, 10) / 100, 0)
				end
			end)
			glitch(ui.line, beat.text, 0.8, cancelled)
			conn:Disconnect()
			tween(grade, 0.8, { Saturation = 0, TintColor = Color3.new(1, 1, 1) })
		elseif beat.kind == "memory" then
			ui.speaker.TextColor3 = AMBER
			ui.line.TextColor3 = AMBER
			ui.line.Font = Enum.Font.GothamMedium
			ui.flash.BackgroundColor3 = Color3.new(1, 1, 1)
			ui.flash.BackgroundTransparency = 0
			tween(ui.flash, 1.2, { BackgroundTransparency = 1 })
			grade.Saturation = -0.7
			grade.TintColor = Color3.fromRGB(255, 225, 190)
			grade.Contrast = 0.15
			typewrite(ui.line, beat.text, beat.seconds * 0.6, cancelled)
		end
		while os.clock() - t0 < beat.seconds and not skipped do
			task.wait(0.05)
		end
		if beat.kind == "memory" then
			tween(grade, 1.0, { Saturation = 0, TintColor = Color3.new(1, 1, 1), Contrast = 0 })
		end
	end

	-- Out: fade through black, hand the camera back, tell the server.
	tween(ui.black, 0.6, { BackgroundTransparency = 0 }).Completed:Wait()
	if camTween then
		camTween:Cancel()
	end
	camera.CameraType = Enum.CameraType.Custom
	grade:Destroy()
	ui.speaker.Text, ui.line.Text, ui.hud.Text = "", "", ""
	ui.skip.Visible = false
	remote:FireServer("done")
	tween(ui.top, 1.2, { Position = UDim2.fromScale(0, -0.11) })
	tween(ui.bottom, 1.2, { Position = UDim2.fromScale(0, 1.2) })
	tween(ui.black, 1.5, { BackgroundTransparency = 1 }).Completed:Wait()
	pcall(function()
		StarterGui:SetCoreGuiEnabled(Enum.CoreGuiType.All, true)
	end)
	ui.gui:Destroy()
	playing = false
end

remote.OnClientEvent:Connect(function(message, info)
	if message == "play" and type(info) == "table" then
		play(info)
	end
end)
