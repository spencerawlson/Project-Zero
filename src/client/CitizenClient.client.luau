--!strict
-- CitizenClient (client): citizens greet this player (CitizenService, docs/NEXUS_01_CITY.md §2). When the player
-- walks within GREET_RANGE of a citizen, a small speech line appears over the citizen's head for a few seconds:
-- the citizen's name and one of its lines (attribute "Greetings", "|"-separated). Each citizen greets the same
-- player at most once every REPEAT seconds. Local only: other players see their own greetings.

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer
local GREET_RANGE = 10
local SHOW = 4
local REPEAT = 45

local lastGreet: { [Model]: number } = {}
local lineIndex: { [Model]: number } = {}

local function bubble(model: Model, name: string, text: string)
	local head = model:FindFirstChild("Head") :: BasePart?
	if not head then return end
	local old = head:FindFirstChild("PZ_Greeting")
	if old then old:Destroy() end
	local g = Instance.new("BillboardGui")
	g.Name = "PZ_Greeting"; g.Size = UDim2.fromOffset(240, 46); g.StudsOffset = Vector3.new(0, 2.6, 0)
	g.LightInfluence = 0; g.MaxDistance = 40; g.Adornee = head
	local f = Instance.new("TextLabel")
	f.Size = UDim2.fromScale(1, 1); f.BackgroundColor3 = Color3.fromRGB(12, 16, 22); f.BackgroundTransparency = 0.2
	f.Font = Enum.Font.Gotham; f.TextSize = 13; f.TextWrapped = true; f.TextColor3 = Color3.fromRGB(235, 240, 245)
	f.RichText = true
	f.Text = ("<b><font color=\"#22D3EE\">%s</font></b>  %s"):format(string.upper(name), text)
	f.Parent = g
	local c = Instance.new("UICorner"); c.CornerRadius = UDim.new(0, 6); c.Parent = f
	g.Parent = head
	task.delay(SHOW, function() g:Destroy() end)
end

local acc = 0
RunService.Heartbeat:Connect(function(dt)
	acc += dt
	if acc < 0.3 then return end
	acc = 0
	local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
	if not root then return end
	local now = os.clock()
	for _, m in ipairs(workspace:GetChildren()) do
		local name = m:GetAttribute("CitizenName")
		local lines = m:GetAttribute("Greetings")
		local head = m:FindFirstChild("Head") :: BasePart?
		if type(name) == "string" and type(lines) == "string" and head and m:IsA("Model") then
			if (head.Position - root.Position).Magnitude <= GREET_RANGE and now - (lastGreet[m] or -math.huge) > REPEAT then
				lastGreet[m] = now
				local list = string.split(lines, "|")
				local i = (lineIndex[m] or 0) % #list + 1
				lineIndex[m] = i
				bubble(m, name, list[i])
			end
		end
	end
end)
