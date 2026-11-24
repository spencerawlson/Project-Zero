--!strict
-- CitizenService: robot citizens of the Founders' Quarter (docs/NEXUS_01_CITY.md §2). They have real names (owner:
-- NEXUS citizens are people; only HECF machines have serial designations), walk a loop along the sidewalks and
-- through the plaza, and pause now and then. Each one starts at a different point of the loop and walks at its own
-- pace, so the street looks lived in. Bodies: ServerStorage.Citizens (R15 rigs from the owner's models, via Avatar
-- Auto Setup); if a body is missing, that citizen is skipped (logged).
-- Greetings are shown by the client (CitizenClient) when a player walks close: attribute "Greetings" holds the lines.

local ReplicatedStorage = game:GetService("ReplicatedStorage")
local ServerStorage = game:GetService("ServerStorage")

local CityLayout = require(ReplicatedStorage.Shared.CityLayout)
local CityService = require(script.Parent.CityService)
local NpcService = require(script.Parent.NpcService)

local CitizenService = {}

-- name, body (ServerStorage.Citizens child), start index on the route, speed, greeting lines
local CITIZENS = {
	{ "Vela", "UtilityRobot", 1, 9, { "Morning, sleeper. The Quarter's quiet today.", "Charge Bay's free, if you're running low." } },
	{ "Brass", "CargoRobot", 5, 7, { "Coming through, cargo for the market.", "Patch pays fair. Tell them Brass sent you." } },
	{ "Orin", "ResearchRobot", 9, 8, { "Fascinating. Another founder awake.", "The archives say the first of us came here asleep, like you." } },
	{ "Tamsin", "UtilityRobot", 12, 10, { "Lights went out again on the west side.", "Have you been to the plaza yet?" } },
}
local PAUSE_CHANCE = 0.25

local function walk(name: string, hum: Humanoid, root: BasePart, startIndex: number)
	local route = CityLayout.CITIZEN_ROUTE
	local i = startIndex
	local rng = Random.new()
	while root.Parent do
		i = i % #route + 1
		local p = route[i]
		local goal = CityLayout.at(p.x + rng:NextNumber(-2, 2), p.z, 0.5)
		hum:MoveTo(goal)
		local t0 = os.clock()
		while root.Parent and os.clock() - t0 < 30 and (Vector3.new(root.Position.X, 0, root.Position.Z) - Vector3.new(goal.X, 0, goal.Z)).Magnitude > 2.5 do
			task.wait(0.25)
			if os.clock() - t0 > 8 and root.AssemblyLinearVelocity.Magnitude < 0.5 then
				hum:MoveTo(goal) -- nudge (MoveTo times out after 8 s)
			end
		end
		if rng:NextNumber() < PAUSE_CHANCE then
			task.wait(rng:NextNumber(2, 6))
		end
	end
end

function CitizenService.Start()
	if not CityService.Ready() then return end
	local bodies = ServerStorage:FindFirstChild("Citizens")
	for _, c in ipairs(CITIZENS) do
		local name, body, startIndex, speed, lines = c[1], c[2], c[3], c[4], c[5]
		if not (bodies and bodies:FindFirstChild(body)) then
			warn(("[Citizens] body %s missing; %s skipped"):format(body, name))
			continue
		end
		local p = CityLayout.CITIZEN_ROUTE[startIndex]
		local model, hum = NpcService.SpawnAt("Citizen_" .. name, body, CFrame.new(CityLayout.at(p.x, p.z, 0.5)), nil)
		if model and hum then
			hum.WalkSpeed = speed
			model:SetAttribute("CitizenName", name)
			model:SetAttribute("Greetings", table.concat(lines, "|"))
			task.spawn(walk, name, hum, model:FindFirstChild("HumanoidRootPart") :: BasePart, startIndex)
		end
	end
end

return CitizenService
