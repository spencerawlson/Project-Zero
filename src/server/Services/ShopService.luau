--!strict
-- ShopService: NEXUS Credits wallet, purchases and equipping (server authoritative). Rules: Shared.ItemCatalog.
--
-- Credits are only changed here (Award, purchases) through PlayerDataService.Update, which mirrors the balance to
-- the player attribute PZ_Credits for the HUD.
-- Vendor: the Circuit Market kiosk in the Founders' Quarter (CityService registers it with SetVendor and opens the
-- window with Open). Wings are never sold (the Reception wing vendor was removed 2026-11-24; see WingPlatformService).
-- ReplicatedStorage.PZ_Remotes.Shop (RemoteEvent):
--   client -> server: ("buy", itemId) | ("equip", itemId) | ("unequip", slot)     (rate limited)
--   server -> client: ("open", state) | ("state", state) | ("result", { ok, reason, itemId, action })
--   state = { credits, items = { id = true }, equipped = { slot = id }, inventory = { id = count }, catalog = ItemCatalog.ITEMS }

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local ItemCatalog = require(ReplicatedStorage.Shared.ItemCatalog)
local PlayerDataService = require(script.Parent.PlayerDataService)
local EquipmentService = require(script.Parent.EquipmentService)

local ShopService = {}

local COOLDOWN = 0.4
local VENDOR_RANGE = 14 -- purchases only while standing at a vendor terminal
local remote: RemoteEvent
local vendor: BasePart? = nil
local last: { [Player]: number } = {}

local function stateOf(player: Player)
	local p = PlayerDataService.GetProfile(player)
	if not p then return nil end
	return { credits = p.wallet.credits, items = p.items, equipped = p.equipped, inventory = p.inventory, catalog = ItemCatalog.ITEMS }
end

-- One-time reward (e.g. "mission:M01"). Returns the credits added.
function ShopService.Award(player: Player, key: string): number
	local added = 0
	PlayerDataService.Update(player, function(p)
		added = ItemCatalog.award(p, key)
	end)
	if added > 0 then
		remote:FireClient(player, "state", stateOf(player))
	end
	return added
end

local function handle(player: Player, action: string, arg: any)
	local ok, reason = false, "bad_request"
	if action == "buy" and type(arg) == "string" then
		local root = player.Character and player.Character:FindFirstChild("HumanoidRootPart") :: BasePart?
		if not vendor or not root or (root.Position - vendor.Position).Magnitude > VENDOR_RANGE then
			ok, reason = false, "too_far"
		else
			PlayerDataService.Update(player, function(p) ok, reason = ItemCatalog.buy(p, arg) end)
		end
	elseif action == "equip" and type(arg) == "string" then
		PlayerDataService.Update(player, function(p) ok, reason = ItemCatalog.equip(p, arg) end)
	elseif action == "unequip" and type(arg) == "string" then
		PlayerDataService.Update(player, function(p) ItemCatalog.unequip(p, arg) end)
		ok, reason = true, nil
	end
	if ok then
		EquipmentService.Refresh(player)
	end
	remote:FireClient(player, "result", { ok = ok, reason = reason, itemId = arg, action = action })
	remote:FireClient(player, "state", stateOf(player))
end

function ShopService.SetVendor(part: BasePart?)
	vendor = part
end

function ShopService.Open(player: Player)
	remote:FireClient(player, "open", stateOf(player))
end

function ShopService.Start()
	local folder = ReplicatedStorage:WaitForChild("PZ_Remotes")
	remote = Instance.new("RemoteEvent")
	remote.Name = "Shop"
	remote.Parent = folder
	remote.OnServerEvent:Connect(function(player, action, arg)
		local now = os.clock()
		if last[player] and now - last[player] < COOLDOWN then return end
		last[player] = now
		handle(player, action, arg)
	end)
	Players.PlayerRemoving:Connect(function(p) last[p] = nil end)
end

return ShopService
