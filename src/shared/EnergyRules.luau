--!strict
-- EnergyRules: a robot's energy (docs/NEXUS_01_CITY.md §2, charging and maintenance). Pure numbers, unit tested;
-- EnergyService (server) applies them, the client only shows them.
-- Design: energy 0..100 drains slowly while playing (about 25 minutes from full) and never punishes hard: at 0 the
-- robot just walks slower. Charge Bays refill it for free; an energy cell gives an instant boost.
--
-- Contract:
--   EnergyRules.MAX, DRAIN_PER_SECOND, CHARGE_PER_SECOND, CELL_AMOUNT, LOW
--   EnergyRules.drain(energy, dt)        -> new energy (never below 0)
--   EnergyRules.charge(energy, dt)       -> new energy (never above MAX)
--   EnergyRules.addCell(energy)          -> new energy after one energy cell
--   EnergyRules.speedFactor(energy)      -> 1 normally, EMPTY_SPEED at 0
--   EnergyRules.isLow(energy)            -> true below LOW (warning + waypoint to the nearest bay)

local EnergyRules = {}

EnergyRules.MAX = 100
EnergyRules.DRAIN_PER_SECOND = 100 / (25 * 60) -- full to empty in ~25 minutes of play
EnergyRules.CHARGE_PER_SECOND = 20             -- empty to full in 5 seconds on a Charge Bay
EnergyRules.CELL_AMOUNT = 50
EnergyRules.LOW = 20
EnergyRules.EMPTY_SPEED = 0.6

local function clamp(x: number): number
	return math.clamp(x, 0, EnergyRules.MAX)
end

function EnergyRules.drain(energy: number, dt: number): number
	assert(dt >= 0, "dt must not be negative")
	return clamp(energy - EnergyRules.DRAIN_PER_SECOND * dt)
end

function EnergyRules.charge(energy: number, dt: number): number
	assert(dt >= 0, "dt must not be negative")
	return clamp(energy + EnergyRules.CHARGE_PER_SECOND * dt)
end

function EnergyRules.addCell(energy: number): number
	return clamp(energy + EnergyRules.CELL_AMOUNT)
end

function EnergyRules.speedFactor(energy: number): number
	return if energy <= 0 then EnergyRules.EMPTY_SPEED else 1
end

function EnergyRules.isLow(energy: number): boolean
	return energy < EnergyRules.LOW
end

return EnergyRules
