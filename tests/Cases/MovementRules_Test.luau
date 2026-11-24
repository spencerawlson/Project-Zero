-- Tests for ReplicatedStorage.Shared.MovementRules (audit remediation step 4: server checks on driving and flight).
return function(t)
	local M = require(game:GetService("ReplicatedStorage").Shared.MovementRules)
	local expect = t.expect
	local dt = M.SAMPLE

	t.test("honest walking, flying and driving pass every check", function()
		local o = Vector3.new(0, 5, 0)
		-- walking at full speed with a jump
		expect.truthy(M.checkStep(o, o + Vector3.new(16 * dt, 25 * dt, 0), dt, M.characterLimits(16, false)))
		-- flying diagonally up at full speed
		local f = M.Flight
		expect.truthy(M.checkStep(o, o + Vector3.new(f.SPEED * dt * 0.7, f.CLIMB * dt, f.SPEED * dt * 0.7), dt, M.characterLimits(16, true)))
		-- falling at terminal speed
		expect.truthy(M.checkStep(o, o - Vector3.new(0, 200 * dt, 0), dt, M.characterLimits(16, false)))
		-- a vehicle at top speed
		expect.truthy(M.checkStep(o, o + Vector3.new(0, 0, -M.Vehicle.MAX_FORWARD * dt), dt, M.vehicleLimits()))
		-- a vehicle turning at full rate
		expect.truthy(M.yawOk(0, M.Vehicle.TURN_RATE * dt, dt))
	end)

	t.test("speed, climb and teleport cheats fail with a reason", function()
		local o = Vector3.zero
		local ok, why = M.checkStep(o, o + Vector3.new(16 * 3 * dt + 10, 0, 0), dt, M.characterLimits(16, false))
		expect.falsy(ok); expect.equal(why, "speed")
		ok, why = M.checkStep(o, o + Vector3.new(0, 30 * 3 * dt + 10, 0), dt, M.characterLimits(16, false))
		expect.falsy(ok); expect.equal(why, "climb")
		ok, why = M.checkStep(o, o + Vector3.new(M.TELEPORT + 1, 0, 0), dt, M.vehicleLimits())
		expect.falsy(ok); expect.equal(why, "teleport")
		ok, why = M.checkStep(o, o + Vector3.new(0, 0, M.Vehicle.MAX_FORWARD * 2 * dt + M.SLACK), dt, M.vehicleLimits())
		expect.falsy(ok); expect.equal(why, "speed")
		expect.falsy(M.yawOk(0, math.pi / 2, dt)) -- a quarter turn in one sample
	end)

	t.test("yaw wraps around half a turn", function()
		expect.truthy(M.yawOk(math.pi - 0.05, -math.pi + 0.05, dt))
	end)

	t.test("wing energy: drains in flight, recharges only on the ground, take-off needs the minimum", function()
		local F = M.Flight
		expect.equal(M.wingEnergy(F.MAX_ENERGY, 1, true, false), F.MAX_ENERGY - F.DRAIN)
		expect.equal(M.wingEnergy(1, 1, true, false), 0)
		expect.equal(M.wingEnergy(50, 1, false, false), 50)          -- falling: no recharge
		expect.equal(M.wingEnergy(90, 1, false, true), F.MAX_ENERGY) -- capped
		expect.falsy(M.canTakeOff(F.MIN_TAKEOFF - 1))
		expect.truthy(M.canTakeOff(F.MIN_TAKEOFF))
		-- about 16 s of flight from full
		local e, s = F.MAX_ENERGY, 0
		while e > 0 do e = M.wingEnergy(e, 0.25, true, false); s += 0.25 end
		expect.near(s, F.MAX_ENERGY / F.DRAIN, 0.25)
	end)

	t.test("bounds cover the facility, the district, the interior and the hauler's street", function()
		expect.truthy(M.inBox(Vector3.new(0, 5, -60), M.WORLD))      -- R04
		expect.truthy(M.inBox(Vector3.new(0, 5, -235), M.WORLD))     -- the plaza
		expect.truthy(M.inBox(Vector3.new(0, 5, -900), M.WORLD))     -- workshop interior
		expect.falsy(M.inBox(Vector3.new(0, 5, -2000), M.WORLD))
		expect.truthy(M.inBox(Vector3.new(0, 3, -250), M.VEHICLE_ZONE))
		expect.falsy(M.inBox(Vector3.new(0, 3, -60), M.VEHICLE_ZONE)) -- no driving into the facility
		expect.truthy(M.FLIGHT_CEILING < M.WORLD.max.Y)
	end)
end
