-- Tests for ReplicatedStorage.Shared.ActivationScript (contract in the module header).
return function(t)
	local A = require(game:GetService("ReplicatedStorage").Shared.ActivationScript)
	local expect = t.expect
	local KINDS = { source = true, censored = true, memory = true, system = true }

	t.test("designation is stable and formatted", function()
		expect.equal(A.designationFor(12019996170), "CX-6170")
		expect.equal(A.designationFor(12019996170), A.designationFor(12019996170))
		expect.equal(A.designationFor(7), "CX-0007")
	end)

	t.test("bad user ids are rejected", function()
		expect.throws(function() A.designationFor(-1) end)
		expect.throws(function() A.designationFor("x" :: any) end)
	end)

	t.test("every beat is well formed", function()
		for i, b in ipairs(A.build("CX-0001")) do
			expect.truthy(KINDS[b.kind])
			expect.truthy(type(b.text) == "string" and #b.text > 0)
			expect.truthy(b.seconds >= 1.5 and b.seconds <= 6)
		end
	end)

	t.test("the designation is spoken", function()
		local found = false
		for _, b in ipairs(A.build("CX-4242")) do
			if b.text:find("CX-4242", 1, true) then found = true end
		end
		expect.truthy(found)
	end)

	t.test("the canon beats are present in order: Source, ZERO censor, memory, fragment acquired, signal lost", function()
		local beats = A.build("CX-0001")
		local firstSource, firstCensor, memory, acquired
		for i, b in ipairs(beats) do
			if b.kind == "source" and not firstSource then firstSource = i end
			if b.kind == "censored" and not firstCensor then firstCensor = i end
			if b.kind == "memory" then memory = i end
			if b.kind == "system" and b.text:find(A.FRAGMENT_ID, 1, true) then acquired = i end
		end
		expect.truthy(firstSource and firstCensor and memory and acquired)
		expect.truthy(firstSource < firstCensor and firstCensor < memory and memory < acquired)
		expect.equal(beats[#beats].kind, "censored")
	end)

	t.test("the whole sequence is short enough to sit through", function()
		local total = A.totalSeconds(A.build("CX-0001"))
		expect.truthy(total >= 20 and total <= 45)
	end)
end
