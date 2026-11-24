-- Tests for ReplicatedStorage.Shared.EnergyRules (docs/NEXUS_01_CITY.md §2).
return function(t)
	local E = require(game:GetService("ReplicatedStorage").Shared.EnergyRules)
	local expect = t.expect

	t.test("full energy lasts about 25 minutes of play", function()
		local e = E.MAX
		for _ = 1, 24 * 60 do e = E.drain(e, 1) end
		expect.truthy(e > 0)
		for _ = 1, 2 * 60 do e = E.drain(e, 1) end
		expect.equal(e, 0)
	end)

	t.test("charging and cells never exceed the maximum", function()
		expect.equal(E.charge(90, 5), E.MAX)
		expect.equal(E.addCell(80), E.MAX)
		expect.equal(E.addCell(10), 60)
		expect.equal(E.charge(0, 1), E.CHARGE_PER_SECOND)
	end)

	t.test("empty only slows the robot; low triggers the warning", function()
		expect.equal(E.speedFactor(50), 1)
		expect.equal(E.speedFactor(0), E.EMPTY_SPEED)
		expect.truthy(E.isLow(19.9))
		expect.falsy(E.isLow(20))
	end)

	t.test("negative time is rejected", function()
		expect.throws(function() E.drain(50, -1) end)
		expect.throws(function() E.charge(50, -1) end)
	end)
end
