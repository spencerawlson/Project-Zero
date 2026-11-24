-- Tests for ReplicatedStorage.Shared.ChassisColors and the colour field of ProfileSchema.
return function(t)
	local Shared = game:GetService("ReplicatedStorage").Shared
	local C = require(Shared.ChassisColors)
	local ProfileSchema = require(Shared.ProfileSchema)
	local expect = t.expect

	t.test("palette ids are unique and valid hex colours", function()
		local seen = {}
		for _, e in ipairs(C.PALETTE) do
			expect.falsy(seen[e.id]); seen[e.id] = true
			expect.truthy(e.hex:match("^#%x%x%x%x%x%x$"))
			expect.truthy(#e.name > 0)
		end
		expect.truthy(#C.PALETTE >= 8)
	end)

	t.test("Cypher's white is reserved: not in the palette and not choosable", function()
		expect.falsy(C.isChoosable(C.CYPHER.id))
		for _, e in ipairs(C.PALETTE) do
			expect.truthy(e.id ~= C.CYPHER.id and e.hex:upper() ~= "#FFFFFF")
		end
		expect.equal(C.get("arctic"), C.CYPHER)
	end)

	t.test("only palette ids are choosable; bad input is rejected", function()
		expect.truthy(C.isChoosable("violet"))
		expect.falsy(C.isChoosable("hotpink-hack"))
		expect.falsy(C.isChoosable(nil))
		expect.falsy(C.isChoosable(42))
	end)

	t.test("default colour is stable per player and spread across the palette", function()
		expect.equal(C.defaultFor(12019996170).id, C.defaultFor(12019996170).id)
		local used = {}
		for uid = 1, #C.PALETTE do used[C.defaultFor(uid).id] = true end
		local n = 0; for _ in pairs(used) do n += 1 end
		expect.equal(n, #C.PALETTE)
	end)

	t.test("color3 falls back to white for unknown ids", function()
		expect.equal(C.color3("nope"), Color3.new(1, 1, 1))
		expect.equal(C.color3("ocean"), Color3.fromHex("#4A8FE0"))
	end)

	t.test("new profiles get their default colour; old profiles gain it on load", function()
		local p = ProfileSchema.default(7, 0)
		expect.equal(p.chassis.colour, C.defaultFor(7).id)
		local old = ProfileSchema.default(9, 0)
		old.chassis.colour = nil
		local migrated = ProfileSchema.migrate(old, 9, 1)
		expect.equal(migrated.chassis.colour, C.defaultFor(9).id)
		old.chassis.colour = "rose"
		expect.equal(ProfileSchema.migrate(old, 9, 1).chassis.colour, "rose")
	end)
end
