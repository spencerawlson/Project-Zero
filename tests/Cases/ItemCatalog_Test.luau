-- Tests for ReplicatedStorage.Shared.ItemCatalog and the wallet / items fields of ProfileSchema.
return function(t)
	local Shared = game:GetService("ReplicatedStorage").Shared
	local Cat = require(Shared.ItemCatalog)
	local ProfileSchema = require(Shared.ProfileSchema)
	local expect = t.expect

	local function fresh(creditsAmount)
		local p = ProfileSchema.default(5, 0)
		p.wallet.credits = creditsAmount or 0
		return p
	end

	t.test("new profiles start with an empty wallet, no items, nothing equipped", function()
		local p = ProfileSchema.default(5, 0)
		expect.equal(p.wallet.credits, 0)
		expect.equal(next(p.items), nil)
		expect.equal(next(p.equipped), nil)
	end)

	-- A priced item for the vendor rules (nothing is sold yet: wings are found, not bought).
	local TEST_ITEM = { id = "test_visor", name = "Test visor", price = 100, slot = "head", description = "" }
	local function withTestItem(fn)
		Cat.ITEMS.test_visor = TEST_ITEM
		local ok, err = pcall(fn)
		Cat.ITEMS.test_visor = nil
		if not ok then error(err, 0) end
	end

	t.test("wings are found, not sold, and no robot starts with them", function()
		local p = fresh(1000)
		local ok, why = Cat.buy(p, "wings_basic")
		expect.falsy(ok); expect.equal(why, "not_for_sale"); expect.equal(p.wallet.credits, 1000)
		expect.equal(p.items.wings_basic, nil)
		expect.equal(Cat.ITEMS.wings_basic.source, "wing_platform")
	end)

	t.test("granting wings adds and equips them once, for free", function()
		local p = fresh(0)
		expect.truthy((Cat.grant(p, "wings_basic")))
		expect.truthy(p.items.wings_basic)
		expect.equal(p.equipped.back, "wings_basic")
		local ok, why = Cat.grant(p, "wings_basic")
		expect.falsy(ok); expect.equal(why, "owned")
		ok, why = Cat.grant(p, "rocket_boots")
		expect.falsy(ok); expect.equal(why, "unknown")
		expect.equal(p.wallet.credits, 0)
	end)

	t.test("buying a priced item spends credits, adds it and equips it", function()
		withTestItem(function()
			local p = fresh(150)
			expect.truthy((Cat.buy(p, "test_visor")))
			expect.equal(p.wallet.credits, 50)
			expect.truthy(p.items.test_visor)
			expect.equal(p.equipped.head, "test_visor")
		end)
	end)

	t.test("cannot buy without enough credits, twice, or an unknown item", function()
		withTestItem(function()
			local p = fresh(99)
			local ok, why = Cat.buy(p, "test_visor")
			expect.falsy(ok); expect.equal(why, "credits"); expect.equal(p.wallet.credits, 99)
			p.wallet.credits = 500
			Cat.buy(p, "test_visor")
			ok, why = Cat.buy(p, "test_visor")
			expect.falsy(ok); expect.equal(why, "owned"); expect.equal(p.wallet.credits, 400)
			ok, why = Cat.buy(p, "rocket_boots")
			expect.falsy(ok); expect.equal(why, "unknown")
		end)
	end)

	t.test("equip needs ownership; unequip clears the slot", function()
		local p = fresh(0)
		local ok, why = Cat.equip(p, "wings_basic")
		expect.falsy(ok); expect.equal(why, "not_owned")
		p.items.wings_basic = true
		expect.truthy((Cat.equip(p, "wings_basic")))
		expect.equal(p.equipped.back, "wings_basic")
		Cat.unequip(p, "back")
		expect.equal(p.equipped.back, nil)
	end)

	t.test("one-time rewards pay once", function()
		local p = fresh(0)
		expect.equal(Cat.award(p, "mission:M01"), 150)
		expect.equal(Cat.award(p, "mission:M01"), 0)
		expect.equal(Cat.award(p, "mission:unknown"), 0)
		expect.equal(p.wallet.credits, 150)
	end)

	t.test("older profiles gain wallet, items and equipped on load", function()
		local old = ProfileSchema.default(5, 0)
		old.wallet, old.items, old.equipped = nil, nil, nil
		local m = ProfileSchema.migrate(old, 5, 1)
		expect.equal(m.wallet.credits, 0)
		expect.truthy(type(m.items) == "table" and type(m.equipped) == "table")
	end)

	t.test("market: energy cells stack up to 5 and are used one at a time", function()
		local p = fresh(1000)
		for _ = 1, 5 do expect.truthy((Cat.buy(p, "energy_cell"))) end
		expect.equal(Cat.count(p, "energy_cell"), 5)
		expect.equal(p.wallet.credits, 1000 - 5 * 30)
		local ok, why = Cat.buy(p, "energy_cell")
		expect.falsy(ok); expect.equal(why, "full")
		expect.truthy((Cat.useOne(p, "energy_cell")))
		expect.equal(Cat.count(p, "energy_cell"), 4)
		expect.equal(p.items.energy_cell, nil)
	end)

	t.test("market: the toolkit is owned once and has no slot", function()
		local p = fresh(250)
		expect.truthy((Cat.buy(p, "toolkit_engineering")))
		expect.truthy(p.items.toolkit_engineering)
		expect.equal(next(p.equipped), nil)
		local ok, why = Cat.buy(p, "toolkit_engineering")
		expect.falsy(ok); expect.equal(why, "owned")
		ok, why = Cat.useOne(p, "toolkit_engineering")
		expect.falsy(ok); expect.equal(why, "unknown")
		expect.equal(p.wallet.credits, 50)
	end)

	t.test("using a cell you don't have fails", function()
		local p = fresh(0)
		local ok, why = Cat.useOne(p, "energy_cell")
		expect.falsy(ok); expect.equal(why, "none")
	end)
end
