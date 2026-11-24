-- Tests for ReplicatedStorage.Shared.MissionM01 (contract in the module header).
return function(t)
	local M = require(game:GetService("ReplicatedStorage").Shared.MissionM01)
	local expect = t.expect

	local function names(effects)
		local out = {}
		for _, e in ipairs(effects) do
			table.insert(out, type(e) == "table" and (e[1] .. ":" .. tostring(e[2])) or e)
		end
		return table.concat(out, ",")
	end

	t.test("full playthrough reaches escape and completes", function()
		local s = M.new(nil, { "B2", "B3", "B1" })
		expect.equal(s.step, "find_cypher")
		expect.equal(names(M.apply(s, "reached_cypher")), "wake_cypher,dialogue:cypher_wake,objective")
		expect.equal(s.step, "restore_power")
		expect.equal(names(M.apply(s, "breaker", "B2")), "breaker_ok:B2")
		expect.equal(names(M.apply(s, "breaker", "B3")), "breaker_ok:B3")
		expect.equal(names(M.apply(s, "breaker", "B1")), "breaker_ok:B1,power_on,dialogue:power_on,objective")
		expect.equal(s.step, "free_sentinel")
		expect.equal(names(M.apply(s, "freed_sentinel")), "wake_sentinel,dialogue:sentinel_wake,lockdown,dialogue:lockdown,objective")
		expect.equal(s.step, "escape")
		expect.equal(names(M.apply(s, "exited")), "complete_player,dialogue:complete")
	end)

	t.test("a wrong breaker resets the sequence", function()
		local s = M.new("restore_power", { "B1", "B2", "B3" })
		M.apply(s, "breaker", "B1")
		expect.equal(names(M.apply(s, "breaker", "B3")), "breaker_reset,dialogue:wrong_order")
		expect.equal(#s.pressed, 0)
		expect.equal(s.step, "restore_power")
		-- starting over works
		M.apply(s, "breaker", "B1"); M.apply(s, "breaker", "B2")
		M.apply(s, "breaker", "B3")
		expect.equal(s.step, "free_sentinel")
	end)

	t.test("pressing an already-thrown or unknown breaker does nothing", function()
		local s = M.new("restore_power", { "B1", "B2", "B3" })
		M.apply(s, "breaker", "B1")
		expect.equal(#M.apply(s, "breaker", "B1"), 0)
		expect.equal(#M.apply(s, "breaker", "B9"), 0)
		expect.equal(#s.pressed, 1)
	end)

	t.test("events out of order change nothing", function()
		local s = M.new()
		expect.equal(#M.apply(s, "freed_sentinel"), 0)
		expect.equal(#M.apply(s, "breaker", "B2"), 0)
		expect.equal(#M.apply(s, "exited"), 0)
		expect.equal(s.step, "find_cypher")
	end)

	t.test("shuffled sequences are permutations of the breakers", function()
		local seed = 0
		local function rnd(n) seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n + 1 end
		for _ = 1, 20 do
			local seq = M.shuffledSequence(rnd)
			table.sort(seq)
			expect.equal(table.concat(seq, ","), "B1,B2,B3")
		end
	end)

	t.test("world effects rebuild each checkpoint", function()
		expect.equal(table.concat(M.worldEffectsFor("find_cypher"), ","), "")
		expect.equal(table.concat(M.worldEffectsFor("restore_power"), ","), "wake_cypher")
		expect.equal(table.concat(M.worldEffectsFor("free_sentinel"), ","), "wake_cypher,power_on")
		expect.equal(table.concat(M.worldEffectsFor("escape"), ","), "wake_cypher,power_on,wake_sentinel,lockdown")
		expect.equal(table.concat(M.worldEffectsFor("complete"), ","), "wake_cypher,power_on,wake_sentinel")
		expect.throws(function() M.worldEffectsFor("nope") end)
	end)

	t.test("the optional records open once Cypher is found", function()
		expect.falsy(M.optionalAvailable("find_cypher"))
		expect.truthy(M.optionalAvailable("restore_power"))
		expect.truthy(M.optionalAvailable("complete"))
	end)

	t.test("every step has an objective and every dialogue key is well formed", function()
		for _, step in ipairs(M.STEPS) do
			expect.truthy(M.OBJECTIVES[step] and #M.OBJECTIVES[step].title > 0)
		end
		for _, key in ipairs({ "cypher_wake", "wrong_order", "power_on", "sentinel_wake", "lockdown", "mf002", "complete" }) do
			local beats = M.DIALOGUE[key]
			expect.truthy(beats and #beats > 0)
			for _, b in ipairs(beats) do
				expect.truthy(b.seconds >= 1.5 and b.seconds <= 6 and #b.text > 0)
			end
		end
	end)
end
