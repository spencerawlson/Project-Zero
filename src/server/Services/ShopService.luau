--!strict
-- ShopService: NEXUS Credits wallet, purchases and equipping (server authoritative). Rules: Shared.ItemCatalog.
--
-- Credits are only changed here (Award, purchases) through PlayerDataService.Update, which mirrors the balance to
-- the player attribute PZ_Credits for the HUD.
-- Vendor: a "Wing vendor" terminal in Reception (R01, facility frame x 22, y 12). Its prompt opens the shop on
-- that player's screen.
-- ReplicatedStorage.PZ_Remotes.Shop (RemoteEvent):
--   client -> server: ("buy", itemId) | ("equip", itemId) | ("unequip", slot)     (rate limited)
--   server -> client: ("open", state) | ("state", state) | ("result", { ok, reason, itemId, action })
--   state = { credits, items = { id = true }, equipped = { slot = id }, catalog = ItemCatalog.ITEMS }

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")

local ItemCatalog = require(ReplicatedStorage.Shared.ItemCatalog)
local PlayerDataService = require(script.Parent.PlayerDataService)
local EquipmentService = require(script.Parent.EquipmentService)

local ShopService = {}

local COOLDOWN = 0.4
local VENDOR_RANGE = 14 -- purchases only while standing at the vendor terminal
local remote: RemoteEvent
local vendor: BasePart? = nil
local last: { [Player]: number } = {}

local function stateOf(player: Player)
	local p = PlayerDataService.GetProfile(player)
	if not p then return nil end
	return { credits = p.wallet.credits, items = p.items, equipped = p.equipped, catalog = ItemCatalog.ITEMS }
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

local function buildVendor()
	local facility = workspace:WaitForChild("PZ_StasisFacility", 30)
	local old = facility and facility:FindFirstChild("WingVendor")
	if old then old:Destroy() end
	local p = Instance.new("Part")
	p.Name = "WingVendor"; p.Anchored = true; p.Size = Vector3.new(1, 5, 3.5)
	p.CFrame = CFrame.new(22, 2.7, -12); p.Color = Color3.fromHex("#2B2F36"); p.Material = Enum.Material.Metal
	local g = Instance.new("SurfaceGui"); g.Face = Enum.NormalId.Left; g.LightInfluence = 0
	g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; g.PixelsPerStud = 40
	local t = Instance.new("TextLabel"); t.Size = UDim2.fromScale(1, 1); t.BackgroundColor3 = Color3.fromRGB(10, 14, 18)
	t.TextColor3 = Color3.fromHex("#22D3EE"); t.Font = Enum.Font.GothamBold; t.TextScaled = true
	t.Text = "WING\nVENDOR\n\nNEXUS\nCREDITS"; t.Parent = g
	g.Parent = p
	local pr = Instance.new("ProximityPrompt")
	pr.ActionText = "Browse"; pr.ObjectText = "Wing vendor"; pr.HoldDuration = 0.2
	pr.MaxActivationDistance = 8; pr.RequiresLineOfSight = false; pr.Parent = p
	pr.Triggered:Connect(function(player)
		remote:FireClient(player, "open", stateOf(player))
	end)
	p.Parent = facility
	vendor = p
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
	buildVendor()
end

return ShopService
