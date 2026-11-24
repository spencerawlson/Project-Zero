--!strict
-- AppearanceService: robot body colours (owner request 2026-11-24). Server authoritative.
--   * Each player's character is tinted with profile.chassis.colour (ChassisColors) whenever it spawns.
--   * Players change colour through ReplicatedStorage.PZ_Remotes.Appearance:
--       client -> server: ("setColour", id)       only palette ids (ChassisColors.isChoosable), at most once per
--                                                  COOLDOWN seconds; saved to the profile and applied at once
--       server -> client: ("colour", id)          the colour now in effect (after a change, and on spawn)
--   * AppearanceService.Paint(model, id) tints any robot model (used for NPCs and dormant robots too).

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local ChassisColors = require(ReplicatedStorage.Shared.ChassisColors)
local PlayerDataService = require(script.Parent.PlayerDataService)

local AppearanceService = {}

local COOLDOWN = 0.5
local remote: RemoteEvent
local lastChange: { [Player]: number } = {}

function AppearanceService.Paint(model: Instance, id: string?)
	local colour = ChassisColors.color3(id)
	for _, d in ipairs(model:GetDescendants()) do
		if d:IsA("SurfaceAppearance") then
			d.Color = colour
		end
	end
	if model:IsA("Model") then
		model:SetAttribute("ChassisColour", id)
	end
end

local function colourOf(player: Player): string?
	local profile = PlayerDataService.GetProfile(player)
	return profile and profile.chassis.colour or nil
end

local function onCharacter(player: Player, character: Model)
	local deadline = os.clock() + 15
	while not PlayerDataService.GetProfile(player) and os.clock() < deadline and player.Parent do
		task.wait(0.2)
	end
	character:WaitForChild("HumanoidRootPart", 10)
	local id = colourOf(player)
	AppearanceService.Paint(character, id)
	if id then
		remote:FireClient(player, "colour", id)
	end
end

function AppearanceService.Start()
	local folder = ReplicatedStorage:WaitForChild("PZ_Remotes")
	remote = Instance.new("RemoteEvent")
	remote.Name = "Appearance"
	remote.Parent = folder
	remote.OnServerEvent:Connect(function(player, action, id)
		if action ~= "setColour" or not ChassisColors.isChoosable(id) then
			return
		end
		local now = os.clock()
		if lastChange[player] and now - lastChange[player] < COOLDOWN then
			return
		end
		lastChange[player] = now
		local ok = PlayerDataService.Update(player, function(p)
			p.chassis.colour = id
		end)
		if ok then
			if player.Character then
				AppearanceService.Paint(player.Character, id)
			end
			remote:FireClient(player, "colour", id)
		end
	end)
	local function onPlayer(player: Player)
		player.CharacterAdded:Connect(function(c)
			onCharacter(player, c)
		end)
		if player.Character then
			task.spawn(onCharacter, player, player.Character)
		end
	end
	Players.PlayerAdded:Connect(onPlayer)
	for _, p in ipairs(Players:GetPlayers()) do
		onPlayer(p)
	end
	Players.PlayerRemoving:Connect(function(p)
		lastChange[p] = nil
	end)
end

return AppearanceService
