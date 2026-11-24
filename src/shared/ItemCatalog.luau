--!strict
-- ItemCatalog: items robots can own, how they get them (bought with NEXUS Credits, or found in the world), and
-- the rules for equipping them. Pure data and functions on a profile table (no Roblox services), unit tested;
-- ShopService and WingPlatformService apply them.
-- Owner decisions 2026-11-24: any basic robot can get wings and fly freely; wings mount on the robot's back
-- (Cypher-style and Sentinel bodies alike). Later the same day: no robot starts with wings, and wings are not
-- sold: players find the wing platform (R03) and stand on it until its ring completes (source "wing_platform").
--
-- Profile fields used (ProfileSchema): wallet.credits (number), items { [itemId] = true }, equipped { [slot] = itemId },
--   inventory { [itemId] = count } for consumables (v2)
-- Founders' Quarter market (2026-11-24, docs/NEXUS_01_CITY.md §2): energy cells (consumable) and the engineering
-- toolkit (a tool: owned, no slot; it unlocks contract C02).
--
-- Contract:
--   ItemCatalog.ITEMS[id] = { id, name, price?, source?, slot?, kind?, max?, description }
--       price = NEXUS Credits (sold by a vendor); source = where it is found instead (not for sale)
--       kind = "consumable" (counted in inventory, up to max) | nil (owned once; equipped in slot if it has one)
--   ItemCatalog.REWARDS[key] = credits for one-time rewards (e.g. "mission:M01")
--   ItemCatalog.canBuy(profile, id)   -> ok: boolean, reason: string?  ("unknown", "not_for_sale", "owned", "full", "credits")
--   ItemCatalog.buy(profile, id)      -> ok, reason   (spends credits; adds the item and equips it in its slot, or
--                                                       adds one to the inventory count for a consumable)
--   ItemCatalog.count(profile, id)    -> consumables held
--   ItemCatalog.useOne(profile, id)   -> ok, reason   ("unknown", "none"): removes one consumable
--   ItemCatalog.grant(profile, id)    -> ok, reason   ("unknown", "owned"): adds a found item and equips it
--   ItemCatalog.equip(profile, id)    -> ok, reason   ("unknown", "not_owned")
--   ItemCatalog.unequip(profile, slot)
--   ItemCatalog.award(profile, key)   -> credits added (0 if this reward was already given or is unknown)

local ItemCatalog = {}

ItemCatalog.ITEMS = {
	wings_basic = {
		id = "wings_basic", name = "Nightwing", source = "wing_platform", slot = "back",
		description = "Segmented flight wings with cyan power lines. Fold out of a back module on any standard frame; free flight on wing energy.",
	},
	energy_cell = {
		id = "energy_cell", name = "Energy cell", price = 30, kind = "consumable", max = 5,
		description = "A charged cell: +50 energy anywhere. Carry up to 5.",
	},
	toolkit_engineering = {
		id = "toolkit_engineering", name = "Engineering toolkit", price = 200,
		description = "Calibrators and fine tools. Patch will trust you with real repairs (contract: Bay Calibration).",
	},
}

ItemCatalog.REWARDS = {
	["mission:M01"] = 150,
}

local function credits(profile: any): number
	return profile.wallet and profile.wallet.credits or 0
end

function ItemCatalog.canBuy(profile: any, id: string): (boolean, string?)
	local item = ItemCatalog.ITEMS[id]
	if not item then return false, "unknown" end
	if not item.price then return false, "not_for_sale" end
	if item.kind == "consumable" then
		if ItemCatalog.count(profile, id) >= (item.max or math.huge) then return false, "full" end
	elseif profile.items[id] then
		return false, "owned"
	end
	if credits(profile) < item.price then return false, "credits" end
	return true, nil
end

function ItemCatalog.buy(profile: any, id: string): (boolean, string?)
	local ok, reason = ItemCatalog.canBuy(profile, id)
	if not ok then return false, reason end
	local item = ItemCatalog.ITEMS[id]
	profile.wallet.credits -= item.price
	if item.kind == "consumable" then
		profile.inventory = profile.inventory or {}
		profile.inventory[id] = ItemCatalog.count(profile, id) + 1
	else
		profile.items[id] = true
		if item.slot then profile.equipped[item.slot] = id end
	end
	return true, nil
end

function ItemCatalog.count(profile: any, id: string): number
	return profile.inventory and profile.inventory[id] or 0
end

function ItemCatalog.useOne(profile: any, id: string): (boolean, string?)
	local item = ItemCatalog.ITEMS[id]
	if not item or item.kind ~= "consumable" then return false, "unknown" end
	local n = ItemCatalog.count(profile, id)
	if n <= 0 then return false, "none" end
	profile.inventory[id] = n - 1
	return true, nil
end

function ItemCatalog.grant(profile: any, id: string): (boolean, string?)
	local item = ItemCatalog.ITEMS[id]
	if not item then return false, "unknown" end
	if profile.items[id] then return false, "owned" end
	profile.items[id] = true
	if item.slot then profile.equipped[item.slot] = id end
	return true, nil
end

function ItemCatalog.equip(profile: any, id: string): (boolean, string?)
	local item = ItemCatalog.ITEMS[id]
	if not item then return false, "unknown" end
	if not profile.items[id] then return false, "not_owned" end
	if not item.slot then return false, "no_slot" end
	profile.equipped[item.slot] = id
	return true, nil
end

function ItemCatalog.unequip(profile: any, slot: string)
	profile.equipped[slot] = nil
end

function ItemCatalog.award(profile: any, key: string): number
	local amount = ItemCatalog.REWARDS[key]
	profile.wallet.rewards = profile.wallet.rewards or {}
	if not amount or profile.wallet.rewards[key] then
		return 0
	end
	profile.wallet.rewards[key] = true
	profile.wallet.credits += amount
	return amount
end

return ItemCatalog
