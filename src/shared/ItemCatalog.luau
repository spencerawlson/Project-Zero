--!strict
-- ItemCatalog: things robots can buy with NEXUS Credits, and the rules for buying and equipping them.
-- Pure data and functions on a profile table (no Roblox services), unit tested; ShopService applies them.
-- Owner decisions 2026-11-24: any basic robot can buy wings with NEXUS Credits and fly freely; wings mount on
-- the robot's back (Cypher-style and Sentinel bodies alike).
--
-- Profile fields used (ProfileSchema): wallet.credits (number), items { [itemId] = true }, equipped { [slot] = itemId }
--
-- Contract:
--   ItemCatalog.ITEMS[id] = { id, name, price, slot, description }
--   ItemCatalog.REWARDS[key] = credits for one-time rewards (e.g. "mission:M01")
--   ItemCatalog.canBuy(profile, id)   -> ok: boolean, reason: string?  ("unknown", "owned", "credits")
--   ItemCatalog.buy(profile, id)      -> ok, reason   (spends credits, adds the item, equips it in its slot)
--   ItemCatalog.equip(profile, id)    -> ok, reason   ("unknown", "not_owned")
--   ItemCatalog.unequip(profile, slot)
--   ItemCatalog.award(profile, key)   -> credits added (0 if this reward was already given or is unknown)

local ItemCatalog = {}

ItemCatalog.ITEMS = {
	wings_basic = {
		id = "wings_basic", name = "Flight Wings", price = 100, slot = "back",
		description = "Back-mounted wings for any standard frame. Free flight on wing energy.",
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
	if profile.items[id] then return false, "owned" end
	if credits(profile) < item.price then return false, "credits" end
	return true, nil
end

function ItemCatalog.buy(profile: any, id: string): (boolean, string?)
	local ok, reason = ItemCatalog.canBuy(profile, id)
	if not ok then return false, reason end
	local item = ItemCatalog.ITEMS[id]
	profile.wallet.credits -= item.price
	profile.items[id] = true
	profile.equipped[item.slot] = id
	return true, nil
end

function ItemCatalog.equip(profile: any, id: string): (boolean, string?)
	local item = ItemCatalog.ITEMS[id]
	if not item then return false, "unknown" end
	if not profile.items[id] then return false, "not_owned" end
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
