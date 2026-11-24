--!strict
-- MovementRules: the limits the server holds driving and flight to (audit remediation step 4, P0 "client-controlled
-- driving" and "client-controlled flight and energy"). Pure numbers and checks, unit tested; MovementGuard (server)
-- applies them, the clients read the same speeds so honest play never trips a check.
--
-- Why: robots and driven vehicles are client-owned for smooth physics, so a modified client could move them anywhere.
-- The server can't stop a client simulating its own parts, but it sees every replicated position: it compares
-- samples against these limits and puts the robot or vehicle back where it last was valid.
--
-- PROVISIONAL (no approved design value yet, technical anti-exploit bounds only; owner to confirm):
--   WORLD bounds, FLIGHT_CEILING and VEHICLE_ZONE. They are wide enough not to limit current content.
--
-- Contract:
--   MovementRules.Flight     { SPEED, CLIMB, MAX_ENERGY, DRAIN, RECHARGE, MIN_TAKEOFF }
--   MovementRules.Vehicle    { MAX_FORWARD, MAX_REVERSE, ACCEL, BRAKE, TURN_RATE }
--   MovementRules.wingEnergy(energy, dt, flying, grounded) -> new energy (0..MAX_ENERGY)
--   MovementRules.canTakeOff(energy)                       -> boolean
--   MovementRules.checkStep(from, to, dt, limits)          -> ok, reason?   (one sample of motion)
--      limits = { horizontal = studs/s, up = studs/s, down = studs/s? }
--   MovementRules.inBox(pos, box)                          -> boolean      box = { min = Vector3, max = Vector3 }
--   MovementRules.characterLimits(walkSpeed, flying)       -> limits
--   MovementRules.vehicleLimits()                          -> limits
--   MovementRules.yawOk(yaw0, yaw1, dt)                    -> boolean      (vehicle turn rate)

local MovementRules = {}

-- Flight (FlightController values, now enforced by the server)
MovementRules.Flight = {
	SPEED = 34,        -- studs/s horizontal
	CLIMB = 22,        -- studs/s up or down
	MAX_ENERGY = 100,
	DRAIN = 6,         -- wing energy per second in the air (~16 s of flight)
	RECHARGE = 25,     -- per second on the ground with wings stowed
	MIN_TAKEOFF = 10,  -- energy needed to take off
}

-- Driving (VehicleClient values)
MovementRules.Vehicle = {
	MAX_FORWARD = 34,  -- studs/s
	MAX_REVERSE = 12,
	ACCEL = 18,        -- studs/s²
	BRAKE = 40,
	TURN_RATE = 1.1,   -- rad/s
}

-- Tolerance: lag, physics pushes and sample jitter. A step is only a violation above limit * TOLERANCE + SLACK / dt.
MovementRules.TOLERANCE = 1.5
MovementRules.SLACK = 6            -- studs per sample, whatever the speed
MovementRules.TELEPORT = 80        -- studs in one sample: corrected at once, no strikes
MovementRules.FALL = 250           -- studs/s down (terminal-ish; Roblox gravity 196.2)
MovementRules.STRIKES = 3          -- consecutive bad samples before a correction
MovementRules.SAMPLE = 0.25        -- seconds between samples

-- PROVISIONAL bounds (Studio coordinates; measured in Studio 2026-11-24). Facility x -54..54, z 2..-122; district x -140..140,
-- street z -115..-400;
-- workshop interior around (0, 0, -900); skyline backdrop near z -520 (not reachable).
MovementRules.WORLD = { min = Vector3.new(-400, -60, -1050), max = Vector3.new(400, 400, 200) }
MovementRules.FLIGHT_CEILING = 250 -- Studio Y; above it the robot is put back
MovementRules.VEHICLE_ZONE = { min = Vector3.new(-160, -20, -440), max = Vector3.new(160, 80, -110) } -- district street; not the facility (z > -122)

function MovementRules.wingEnergy(energy: number, dt: number, flying: boolean, grounded: boolean): number
	assert(dt >= 0, "dt must not be negative")
	local F = MovementRules.Flight
	if flying then
		return math.max(0, energy - F.DRAIN * dt)
	elseif grounded then
		return math.min(F.MAX_ENERGY, energy + F.RECHARGE * dt)
	end
	return energy
end

function MovementRules.canTakeOff(energy: number): boolean
	return energy >= MovementRules.Flight.MIN_TAKEOFF
end

export type Limits = { horizontal: number, up: number, down: number? }

function MovementRules.checkStep(from: Vector3, to: Vector3, dt: number, limits: Limits): (boolean, string?)
	if dt <= 0 then return true, nil end
	local d = to - from
	if d.Magnitude > MovementRules.TELEPORT then return false, "teleport" end
	local horizontal = Vector3.new(d.X, 0, d.Z).Magnitude
	local tol, slack = MovementRules.TOLERANCE, MovementRules.SLACK
	if horizontal > limits.horizontal * tol * dt + slack then return false, "speed" end
	if d.Y > limits.up * tol * dt + slack then return false, "climb" end
	if -d.Y > (limits.down or MovementRules.FALL) * tol * dt + slack then return false, "drop" end
	return true, nil
end

function MovementRules.inBox(pos: Vector3, box: { min: Vector3, max: Vector3 }): boolean
	return pos.X >= box.min.X and pos.X <= box.max.X
		and pos.Y >= box.min.Y and pos.Y <= box.max.Y
		and pos.Z >= box.min.Z and pos.Z <= box.max.Z
end

-- Jump power 50 gives about 25 studs/s up at take-off; walking robots fall freely.
function MovementRules.characterLimits(walkSpeed: number, flying: boolean): Limits
	if flying then
		local F = MovementRules.Flight
		return { horizontal = F.SPEED, up = math.max(F.CLIMB, 25), down = MovementRules.FALL }
	end
	return { horizontal = math.max(walkSpeed, 16), up = 30, down = MovementRules.FALL }
end

-- Vehicles: ground speed; small climbs over kerbs and ramps; free to fall.
function MovementRules.vehicleLimits(): Limits
	return { horizontal = MovementRules.Vehicle.MAX_FORWARD, up = 20, down = MovementRules.FALL }
end

function MovementRules.yawOk(yaw0: number, yaw1: number, dt: number): boolean
	if dt <= 0 then return true end
	local d = (yaw1 - yaw0 + math.pi) % (2 * math.pi) - math.pi
	return math.abs(d) <= MovementRules.Vehicle.TURN_RATE * MovementRules.TOLERANCE * dt + 0.35
end

return MovementRules
