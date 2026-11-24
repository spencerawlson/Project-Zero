-- Tests for ReplicatedStorage.Shared.PodRoster (contract in the module header).
return function(t)
	local PodRoster = require(game:GetService("ReplicatedStorage").Shared.PodRoster)
	local expect = t.expect
	local PODS = { "P02", "P03", "P04", "P06" }

	t.test("a party fills pods in order", function()
		local r = PodRoster.new(PODS)
		expect.equal(r:claim(101), "P02")
		expect.equal(r:claim(102), "P03")
		expect.equal(r:claim(103), "P04")
		expect.equal(r:claim(104), "P06")
		expect.equal(r:freeCount(), 0)
	end)

	t.test("a fifth player gets no pod", function()
		local r = PodRoster.new(PODS)
		for id = 1, 4 do r:claim(id) end
		expect.equal(r:claim(5), nil)
		expect.equal(r:podOf(5), nil)
	end)

	t.test("claim is idempotent for a player who already holds a pod", function()
		local r = PodRoster.new(PODS)
		expect.equal(r:claim(7), "P02")
		r:claim(8)
		expect.equal(r:claim(7), "P02")
		expect.equal(r:freeCount(), 2)
	end)

	t.test("release frees the pod for the next player", function()
		local r = PodRoster.new(PODS)
		r:claim(1); r:claim(2)
		expect.equal(r:release(1), "P02")
		expect.equal(r:holderOf("P02"), nil)
		expect.equal(r:claim(3), "P02")
		expect.equal(r:holderOf("P02"), 3)
	end)

	t.test("release of a player without a pod is a no-op", function()
		local r = PodRoster.new(PODS)
		r:claim(1)
		expect.equal(r:release(99), nil)
		expect.equal(r:freeCount(), 3)
	end)

	t.test("podOf and holderOf agree", function()
		local r = PodRoster.new(PODS)
		r:claim(10); r:claim(20)
		expect.equal(r:podOf(20), "P03")
		expect.equal(r:holderOf("P03"), 20)
	end)

	t.test("bad input is rejected", function()
		expect.throws(function() PodRoster.new({}) end)
		expect.throws(function() PodRoster.new({ "P02", "P02" }) end)
		local r = PodRoster.new(PODS)
		expect.throws(function() r:claim("not a number" :: any) end)
	end)
end
