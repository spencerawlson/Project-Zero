--!strict
-- ProfileSchema: the shape of a player's saved profile, its defaults, and upgrades between schema versions.
-- Pure functions only (no Roblox services), so it is unit testable and safe to share with clients.
--
-- Contract:
--   ProfileSchema.VERSION                 current schema version (integer)
--   ProfileSchema.default(userId, now)    a complete new profile for userId, timestamps = now
--   ProfileSchema.migrate(data, userId, now)
--       returns a complete profile at VERSION built from any older or partial saved table:
--       missing fields are filled from defaults, existing values are kept, unknown fields are kept,
--       and a profile from a NEWER version than this server understands raises an error (never downgrade data).
--   ProfileSchema.STARTER_CHASSIS         id of the standard starter body (owner decision D2: Cypher-style frame)

local ProfileSchema = {}
local ChassisColors = require(script.Parent.ChassisColors)

ProfileSchema.VERSION = 2
ProfileSchema.STARTER_CHASSIS = "CypherFrame"

export type Profile = {
	schemaVersion: number,
	userId: number,
	createdAt: number,
	lastSeenAt: number,
	identity: { designation: string? },
	chassis: { current: string, owned: { string }, colour: string }, -- colour: ChassisColors id
	progress: {
		activated: boolean,
		missions: { [string]: string },        -- missionId -> "active" | "complete"
		memoryFragments: { [string]: boolean }, -- fragmentId -> recovered
	},
	stats: { sessions: number },
	wallet: { credits: number, rewards: { [string]: boolean }? }, -- NEXUS Credits (server-authoritative)
	items: { [string]: boolean },     -- owned ItemCatalog ids
	equipped: { [string]: string },   -- slot -> ItemCatalog id (e.g. back = "wings_basic")
	-- v2 (2026-11-24, Phase 2 city slice; docs/NEXUS_01_CITY.md §2):
	status: { energy: number },                        -- 0..100, drains while playing, charged at Charge Bays
	careers: { engineering: { xp: number } },          -- experience per career (Phase 3 adds more careers)
	contracts: { [string]: { completions: number, lastCompletedAt: number } }, -- ContractRules ids
	inventory: { [string]: number },                   -- consumable ItemCatalog ids -> count (e.g. energy_cell)
}

local function deepCopy<T>(value: T): T
	if type(value) ~= "table" then
		return value
	end
	local out = {}
	for k, v in pairs(value :: any) do
		out[k] = deepCopy(v)
	end
	return out :: any
end

function ProfileSchema.default(userId: number, now: number): Profile
	assert(type(userId) == "number", "userId must be a number")
	assert(type(now) == "number", "now must be a number")
	return {
		schemaVersion = ProfileSchema.VERSION,
		userId = userId,
		createdAt = now,
		lastSeenAt = now,
		identity = { designation = nil },
		chassis = { current = ProfileSchema.STARTER_CHASSIS, owned = { ProfileSchema.STARTER_CHASSIS },
			colour = ChassisColors.defaultFor(userId).id }, -- players start in different colours (owner, 2026-11-24)
		progress = { activated = false, missions = {}, memoryFragments = {} },
		stats = { sessions = 0 },
		wallet = { credits = 0 },
		items = {},
		equipped = {},
		status = { energy = 100 },
		careers = { engineering = { xp = 0 } },
		contracts = {},
		inventory = {},
	}
end

-- Fill every missing key of `target` from `defaults`, recursively for nested tables. Existing values win.
local function fillMissing(target: { [any]: any }, defaults: { [any]: any })
	for k, dv in pairs(defaults) do
		local tv = target[k]
		if tv == nil then
			target[k] = deepCopy(dv)
		elseif type(tv) == "table" and type(dv) == "table" and next(dv) ~= nil and #dv == 0 then
			fillMissing(tv, dv) -- recurse into record-like tables, not into arrays or empty maps
		end
	end
end

function ProfileSchema.migrate(data: any, userId: number, now: number): Profile
	if data == nil then
		return ProfileSchema.default(userId, now)
	end
	assert(type(data) == "table", "saved profile must be a table")
	local version = data.schemaVersion
	if type(version) == "number" and version > ProfileSchema.VERSION then
		error(string.format("profile schema %d is newer than this server (%d)", version, ProfileSchema.VERSION))
	end
	local profile = deepCopy(data)
	-- Version 0 (or missing version) -> 1: no renamed fields yet; defaults fill the gaps below.
	-- 1 -> 2: new sections only (status, careers, contracts, inventory); defaults fill them below.
	fillMissing(profile, ProfileSchema.default(userId, now) :: any)
	profile.schemaVersion = ProfileSchema.VERSION
	profile.userId = userId
	return profile :: any
end

return ProfileSchema
