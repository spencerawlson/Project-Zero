--!strict
-- ChassisColors: paint colours for robot bodies (owner request 2026-11-24: robots must not all look alike;
-- players pick their own colour, and players start with different colours).
-- A colour tints the body's SurfaceAppearance (SurfaceAppearance.Color multiplies the colour map): light panels
-- take the colour, dark parts and the face screen keep their look. Pure data and functions, unit tested.
--
-- Contract:
--   ChassisColors.PALETTE              ordered list of { id, name, hex } that players can choose from
--   ChassisColors.CYPHER               { id = "arctic", ... }: reserved for the story NPC Cypher (not choosable),
--                                      so Cypher is the only white robot
--   ChassisColors.get(id)              -> entry or nil (palette or Cypher)
--   ChassisColors.isChoosable(id)      -> true only for palette ids
--   ChassisColors.defaultFor(userId)   -> palette entry, stable per player, spread across the palette
--   ChassisColors.color3(id)           -> Color3 (white for an unknown id)

local ChassisColors = {}

export type Entry = { id: string, name: string, hex: string }

ChassisColors.PALETTE = {
	{ id = "obsidian", name = "Obsidian Black", hex = "#464A54" },
	{ id = "bronze", name = "Bronze Brown", hex = "#8B5A3C" },
	{ id = "violet", name = "Royal Purple", hex = "#8E5CD9" },
	{ id = "rose", name = "Rose Pink", hex = "#F28DB8" },
	{ id = "ember", name = "Ember Orange", hex = "#F08A3C" },
	{ id = "jade", name = "Jade Green", hex = "#4FBF8A" },
	{ id = "ocean", name = "Ocean Blue", hex = "#4A8FE0" },
	{ id = "crimson", name = "Crimson Red", hex = "#D9434E" },
	{ id = "gold", name = "Gold", hex = "#E6BE4A" },
	{ id = "slate", name = "Slate Grey", hex = "#7C8794" },
} :: { Entry }

ChassisColors.CYPHER = { id = "arctic", name = "Arctic White (Cypher)", hex = "#FFFFFF" } :: Entry

function ChassisColors.get(id: string?): Entry?
	if id == ChassisColors.CYPHER.id then
		return ChassisColors.CYPHER
	end
	for _, e in ipairs(ChassisColors.PALETTE) do
		if e.id == id then
			return e
		end
	end
	return nil
end

function ChassisColors.isChoosable(id: any): boolean
	if type(id) ~= "string" then
		return false
	end
	for _, e in ipairs(ChassisColors.PALETTE) do
		if e.id == id then
			return true
		end
	end
	return false
end

function ChassisColors.defaultFor(userId: number): Entry
	assert(type(userId) == "number", "userId must be a number")
	local n = #ChassisColors.PALETTE
	return ChassisColors.PALETTE[(math.floor(math.abs(userId)) % n) + 1]
end

function ChassisColors.color3(id: string?): Color3
	local e = ChassisColors.get(id)
	return if e then Color3.fromHex(e.hex) else Color3.new(1, 1, 1)
end

return ChassisColors
