-- Tests for ReplicatedStorage.Shared.ContractRules (docs/NEXUS_01_CITY.md §2).
return function(t)
	local Shared = game:GetService("ReplicatedStorage").Shared
	local C = require(Shared.ContractRules)
	local ProfileSchema = require(Shared.ProfileSchema)
	local expect = t.expect
	local LIGHTS = { "L2", "L5", "L7" }

	local function has(effects, name)
		for _, e in ipairs(effects) do
			if e == name or (type(e) == "table" and e[1] == name) then return true end
		end
		return false
	end

	t.test("C01: one cell at a time, three lights, then report", function()
		local s = C.new("C01", LIGHTS)
		expect.equal(s.step, "collect")
		expect.deepEqual(C.apply(s, "install", "L2"), {})       -- no cell yet
		expect.truthy(has(C.apply(s, "take_cell"), "carrying"))
		expect.deepEqual(C.apply(s, "take_cell"), {})            -- already carrying
		expect.deepEqual(C.apply(s, "install", "L9"), {})       -- not a target
		expect.truthy(has(C.apply(s, "install", "L2"), "done"))
		expect.equal(s.step, "collect")
		C.apply(s, "take_cell"); expect.deepEqual(C.apply(s, "install", "L2"), {}) -- already fixed
		C.apply(s, "install", "L5")
		C.apply(s, "take_cell"); C.apply(s, "install", "L7")
		expect.equal(s.step, "report")
		expect.truthy(has(C.apply(s, "report"), "complete"))
		expect.equal(s.step, "complete")
	end)

	t.test("C01 objective counts fixed lights and lists the remaining ones", function()
		local s = C.new("C01", LIGHTS)
		local o = C.objective(s)
		expect.truthy(o.pickup and #o.targets == 3)
		C.apply(s, "take_cell"); C.apply(s, "install", "L5")
		o = C.objective(s)
		expect.truthy(o.hint:find("1/3", 1, true) ~= nil)
		expect.deepEqual(o.targets, { "L2", "L7" })
	end)

	t.test("first completion pays more; repeats pay less and wait for the cooldown", function()
		local p = ProfileSchema.default(5, 0)
		local r = C.reward(p, "C01", 1000)
		expect.truthy(r.first); expect.equal(r.credits, 120)
		expect.equal(p.wallet.credits, 120); expect.equal(p.careers.engineering.xp, 50)
		local ok, why = C.canStart(p, "C01", 1000 + 10)
		expect.falsy(ok); expect.equal(why, "cooldown")
		expect.truthy((C.canStart(p, "C01", 1000 + C.CONTRACTS.C01.cooldown)))
		r = C.reward(p, "C01", 2000)
		expect.falsy(r.first); expect.equal(r.credits, 40)
		expect.equal(p.contracts.C01.completions, 2)
		expect.equal(p.careers.engineering.xp, 70)
	end)

	t.test("C02 needs the toolkit and C01 done once", function()
		local p = ProfileSchema.default(5, 0)
		local ok, why = C.canStart(p, "C02", 0)
		expect.falsy(ok); expect.equal(why, "needs_item")
		p.items.toolkit_engineering = true
		ok, why = C.canStart(p, "C02", 0)
		expect.falsy(ok); expect.equal(why, "needs_contract")
		C.reward(p, "C01", 0)
		expect.truthy((C.canStart(p, "C02", 0)))
		local s = C.new("C02", { "A1", "A2", "A3" })
		expect.equal(s.step, "calibrate")
		C.apply(s, "calibrate", "A1"); C.apply(s, "calibrate", "A3"); C.apply(s, "calibrate", "A2")
		expect.equal(s.step, "report")
	end)

	t.test("unknown contracts and wrong target counts are refused", function()
		local ok, why = C.canStart(ProfileSchema.default(5, 0), "C99", 0)
		expect.falsy(ok); expect.equal(why, "unknown")
		expect.throws(function() C.new("C01", { "L1" }) end)
	end)
end
