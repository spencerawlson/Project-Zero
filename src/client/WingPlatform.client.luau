--!strict
-- WingPlatform (client): draws the wing platform in R03 for this player (WingPlatformService decides everything).
--   Hologram: turns slowly and bobs above the platform while it has power; hidden without power.
--   Ring: SEGMENTS lights around the centre disc fill up while this player charges, then flash when the wings are
--         acquired. Local only: each player sees their own progress.
--   Label: a small floating line (NO POWER / STAND IN THE CENTRE / INSTALLING 60% / INSTALLED: [F] TO FLY).
--   Banner: "NIGHTWING ACQUIRED" when the server grants the wings.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("WingPlatform") :: RemoteEvent
local facility = workspace:WaitForChild("PZ_StasisFacility")
local platform = facility:WaitForChild("WingPlatform") :: Model
local ringFolder = platform:WaitForChild("Ring")
local info = platform:WaitForChild("Info") :: BasePart

local CYAN = Color3.fromHex("#22D3EE")
local DIM = 0.75

local segments: { BasePart } = {}
for _, s in ipairs(ringFolder:GetChildren()) do
	if s:IsA("BasePart") then table.insert(segments, s) end
end
table.sort(segments, function(a, b) return a.Name < b.Name end)

-- label ----------------------------------------------------------------------------------------------------
local bb = Instance.new("BillboardGui")
bb.Name = "PZ_WingPlatformLabel"; bb.Adornee = info; bb.Size = UDim2.fromOffset(240, 26); bb.LightInfluence = 0
bb.MaxDistance = 45; bb.AlwaysOnTop = false
local text = Instance.new("TextLabel")
text.Size = UDim2.fromScale(1, 1); text.BackgroundTransparency = 1; text.Font = Enum.Font.GothamBold; text.TextSize = 14
text.TextColor3 = CYAN; text.TextStrokeTransparency = 0.4; text.Text = ""; text.Parent = bb
bb.Parent = player:WaitForChild("PlayerGui")

-- banner ---------------------------------------------------------------------------------------------------
local gui = Instance.new("ScreenGui")
gui.Name = "PZ_WingPlatform"; gui.ResetOnSpawn = false; gui.DisplayOrder = 11; gui.Parent = player.PlayerGui
local function banner()
	local f = Instance.new("TextLabel")
	f.AnchorPoint = Vector2.new(0.5, 0.5); f.Position = UDim2.fromScale(0.5, 0.3); f.Size = UDim2.fromOffset(560, 64)
	f.BackgroundColor3 = Color3.fromRGB(12, 16, 22); f.BackgroundTransparency = 0.15; f.Font = Enum.Font.GothamBold
	f.TextSize = 24; f.TextColor3 = CYAN; f.TextTransparency = 1; f.Text = "NIGHTWING ACQUIRED  ·  PRESS F TO FLY"
	Instance.new("UICorner", f).CornerRadius = UDim.new(0, 6)
	f.Parent = gui
	TweenService:Create(f, TweenInfo.new(0.5), { TextTransparency = 0 }):Play()
	task.delay(4.5, function()
		TweenService:Create(f, TweenInfo.new(1.2), { TextTransparency = 1, BackgroundTransparency = 1 }):Play()
		task.delay(1.3, function() f:Destroy() end)
	end)
end

-- state ----------------------------------------------------------------------------------------------------
local chargeStart: number? = nil
local chargeSeconds = 5
local flashUntil = 0

local function powered(): boolean
	return platform:GetAttribute("Powered") == true
end

local function owned(): boolean
	local c = player.Character
	return c ~= nil and c:GetAttribute("PZ_CanFly") == true
end

remote.OnClientEvent:Connect(function(kind, data)
	if kind ~= "status" or type(data) ~= "table" then return end
	if data.state == "charging" then
		chargeStart = os.clock(); chargeSeconds = tonumber(data.seconds) or 5
	elseif data.state == "cancel" then
		chargeStart = nil
	elseif data.state == "granted" then
		chargeStart = nil; flashUntil = os.clock() + 1.2
		banner()
	end
end)

-- hologram motion: local only, from its server pose
local holo = platform:FindFirstChild("Hologram") :: Model?
local holoBase = if holo then holo:GetPivot() else nil
local holoParts: { BasePart } = {}
if holo then
	for _, d in ipairs(holo:GetDescendants()) do
		if d:IsA("BasePart") and d.Transparency < 1 then table.insert(holoParts, d) end
	end
end
local holoVisible: boolean? = nil

RunService.RenderStepped:Connect(function()
	local now = os.clock()
	local on = powered()
	if holo and holoBase then
		if on ~= holoVisible then
			holoVisible = on
			for _, p in ipairs(holoParts) do p.Transparency = if on then 0 else 1 end
		end
		if on then
			holo:PivotTo(holoBase * CFrame.new(0, math.sin(now * 1.3) * 0.25, 0) * CFrame.Angles(0, now * 0.6, 0))
		end
	end
	-- ring
	local lit = 0
	if now < flashUntil then
		lit = #segments
	elseif chargeStart then
		lit = math.floor(math.clamp((now - chargeStart) / chargeSeconds, 0, 1) * #segments)
	end
	for i, s in ipairs(segments) do
		s.Transparency = if not on then 1 elseif i <= lit then 0 else DIM
		s.Color = if now < flashUntil then Color3.new(1, 1, 1) else CYAN
	end
	-- label
	if not on then
		text.Text = "WING PLATFORM  ·  NO POWER"
		text.TextColor3 = Color3.fromRGB(150, 160, 170)
	elseif chargeStart then
		text.Text = ("INSTALLING NIGHTWING  %d%%"):format(math.floor(math.clamp((now - chargeStart) / chargeSeconds, 0, 1) * 100))
		text.TextColor3 = CYAN
	elseif owned() then
		text.Text = "NIGHTWING INSTALLED  ·  [F] TO FLY"
		text.TextColor3 = CYAN
	else
		text.Text = "NIGHTWING  ·  STAND IN THE CENTRE"
		text.TextColor3 = CYAN
	end
end)
