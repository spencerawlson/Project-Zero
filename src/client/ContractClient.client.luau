--!strict
-- ContractClient (client): this player's side of a contract (ContractService, docs/NEXUS_01_CITY.md §2).
-- Each player has their own job, so the prompts are made here, locally, only for this player's targets:
--   * "Take power cell" on Patch's crate while the contract wants a cell,
--   * "Install cell" (hold) on each dark target light while carrying one,
--   * "Calibrate arm" (hold) on each Charge Bay arm for C02.
-- The target lights look dark (and their socket glows red) on this player's screen until fixed; other players
-- see the street as it is for them. The server checks every request (distance and rules) before anything changes.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("Contract") :: RemoteEvent
local city = workspace:WaitForChild("PZ_FoundersQuarter")
local anchors = city:WaitForChild("Anchors")
local lights = city:WaitForChild("Lights")

local CYAN = Color3.fromHex("#22D3EE")
local DARK = Color3.fromRGB(40, 44, 50)
local RED = Color3.fromRGB(255, 70, 70)

local prompts: { ProximityPrompt } = {}
local darkened: { [string]: boolean } = {}

local function clearPrompts()
	for _, p in ipairs(prompts) do p:Destroy() end
	table.clear(prompts)
end

local function prompt(parent: Instance, action: string, object: string, hold: number, request: string, arg: string?)
	local p = Instance.new("ProximityPrompt")
	p.ActionText = action; p.ObjectText = object; p.HoldDuration = hold
	p.MaxActivationDistance = 8; p.RequiresLineOfSight = false
	p.Parent = parent
	p.Triggered:Connect(function()
		remote:FireServer(request, arg)
	end)
	table.insert(prompts, p)
end

local function setDark(id: string, dark: boolean)
	local m = lights:FindFirstChild(id)
	if not m then return end
	local head = m:FindFirstChild("Head") :: BasePart?
	local socketLight = m:FindFirstChild("SocketLight") :: BasePart?
	if head then
		head.Color = if dark then DARK else CYAN
		head.Material = if dark then Enum.Material.Metal else Enum.Material.Neon
		local pl = head:FindFirstChildOfClass("PointLight")
		if pl then pl.Enabled = not dark end
	end
	if socketLight then socketLight.Color = if dark then RED else CYAN end
	darkened[id] = if dark then true else nil
end

-- a dark target light flickers now and then, so it reads as broken
RunService.Heartbeat:Connect(function()
	for id in pairs(darkened) do
		local head = lights:FindFirstChild(id) and (lights :: any)[id]:FindFirstChild("Head") :: BasePart?
		if head then
			head.Color = if math.random() < 0.015 then CYAN else DARK
		end
	end
end)

remote.OnClientEvent:Connect(function(kind, s)
	if kind ~= "state" then return end
	clearPrompts()
	local done: { [string]: boolean } = {}
	if s then
		for _, d in ipairs(s.done) do done[d] = true end
	end
	-- lights: dark while they're this player's unfinished C01 targets
	for id in pairs(darkened) do
		if not (s and s.id == "C01" and not done[id] and table.find(s.targets, id)) then setDark(id, false) end
	end
	if not s then return end
	if s.id == "C01" then
		for _, id in ipairs(s.targets) do
			if not done[id] then setDark(id, true) end
		end
	end
	if s.step == "collect" then
		local crate = anchors:FindFirstChild("WorkshopCrate")
		if crate then prompt(crate, "Take power cell", "Patch's crate", 0, "take_cell") end
	elseif s.step == "install" and s.carrying then
		for _, id in ipairs(s.targets) do
			local m = lights:FindFirstChild(id)
			local socket = m and m:FindFirstChild("Socket")
			if socket and not done[id] then prompt(socket, "Install cell", "Dark street light " .. id, 2, "install", id) end
		end
	elseif s.step == "calibrate" then
		for i, id in ipairs(s.targets) do
			local arm = anchors:FindFirstChild(id)
			if arm and not done[id] then prompt(arm, "Calibrate", "Charge Bay arm " .. i, 2.5, "calibrate", id) end
		end
	end
end)
