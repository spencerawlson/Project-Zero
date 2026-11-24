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

	t.test("buying wings spends credits, adds them and equips them on the back", function()
		local p = fresh(150)
		expect.truthy((Cat.buy(p, "wings_basic")))
		expect.equal(p.wallet.credits, 50)
		expect.truthy(p.items.wings_basic)
		expect.equal(p.equipped.back, "wings_basic")
	end)

	t.test("cannot buy without enough credits, twice, or an unknown item", function()
		local p = fresh(99)
		local ok, why = Cat.buy(p, "wings_basic")
		expect.falsy(ok); expect.equal(why, "credits"); expect.equal(p.wallet.credits, 99)
		p.wallet.credits = 500
		Cat.buy(p, "wings_basic")
		ok, why = Cat.buy(p, "wings_basic")
		expect.falsy(ok); expect.equal(why, "owned"); expect.equal(p.wallet.credits, 400)
		ok, why = Cat.buy(p, "rocket_boots")
		expect.falsy(ok); expect.equal(why, "unknown")
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

	t.test("one-time rewards pay once; finishing M01 affords wings", function()
		local p = fresh(0)
		expect.equal(Cat.award(p, "mission:M01"), 150)
		expect.equal(Cat.award(p, "mission:M01"), 0)
		expect.equal(Cat.award(p, "mission:unknown"), 0)
		expect.equal(p.wallet.credits, 150)
		expect.truthy((Cat.canBuy(p, "wings_basic")))
	end)

	t.test("older profiles gain wallet, items and equipped on load", function()
		local old = ProfileSchema.default(5, 0)
		old.wallet, old.items, old.equipped = nil, nil, nil
		local m = ProfileSchema.migrate(old, 5, 1)
		expect.equal(m.wallet.credits, 0)
		expect.truthy(type(m.items) == "table" and type(m.equipped) == "table")
	end)
end
