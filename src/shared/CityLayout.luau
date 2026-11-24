--!strict
-- CityLayout: positions in the Founders' Quarter, the first district (docs/NEXUS_01_CITY.md §1). Pure data, shared by
-- the edit-time builder (Roblox/CITY-01_founders_quarter_build.lua) and the runtime services, so both agree.
--
-- District frame: origin = the start of the street, just past the Stasis Facility's exit zone (behind door D04);
-- local -Z leads away from the facility, +X is to the right walking in. Studio position = CityLayout.at(x, z, y).
-- Ground top is Y = 0 (the facility floor is at 0.2).
--
-- Contract:
--   CityLayout.ORIGIN                       Vector3 (Studio)
--   CityLayout.at(x, z, y?)                 Vector3 (Studio) for a district point
--   CityLayout.BUILDINGS[name]              { model, x, z, yaw (deg), length } ; model = ServerStorage.City child
--   CityLayout.LIGHTS                       ordered { id, x, z } street lights (contract C01 targets)
--   CityLayout.SPOTS[name]                  { x, z, y? } named points (crate, Patch, doors, counter, pads, arms…)
--   CityLayout.INTERIOR                     workshop interior placement (Studio Vector3 of its floor centre)
--   CityLayout.CITIZEN_ROUTE                ordered { x, z } loop for walking citizens

local CityLayout = {}

CityLayout.ORIGIN = Vector3.new(0, 0, -135)

function CityLayout.at(x: number, z: number, y: number?): Vector3
	return CityLayout.ORIGIN + Vector3.new(x, y or 0, z)
end

CityLayout.ROAD_HALF = 12      -- road x -12..12
CityLayout.WALK_HALF = 20      -- sidewalks x ±12..±20
CityLayout.LENGTH = 250        -- street from z 0 to z -250
CityLayout.PLAZA = { x = 0, z = -100, radius = 24 }

-- yaw: rotation about Y so the building's front faces the street (0 = front faces -Z in the model's own frame,
-- set per model when it is placed in Studio; see the builder).
CityLayout.BUILDINGS = {
	PatchWorkshop       = { model = "PZ_PatchWorkshop",       x = -62, z = -60,  yaw = 90,  length = 70 },
	ChargeBay           = { model = "PZ_ChargeBay",           x = 32,  z = -40,  yaw = -90, length = 20 },
	ResidentialTower    = { model = "PZ_ResidentialTower",    x = 100, z = -40,  yaw = -90, length = 32 },
	MaintenanceHospital = { model = "PZ_MaintenanceHospital", x = 64,  z = -110, yaw = -90, length = 80 },
	CircuitMarket       = { model = "PZ_CircuitMarket",       x = -68, z = -160, yaw = 90,  length = 80 },
	EmergencyStation    = { model = "PZ_EmergencyStation",    x = 56,  z = -178, yaw = -90, length = 48 },
	PoliceStation       = { model = "PZ_PoliceStation",       x = 50,  z = -222, yaw = -90, length = 36 },
}

CityLayout.LIGHTS = {
	{ id = "L1", x = -16, z = -20 }, { id = "L2", x = 16, z = -20 },
	{ id = "L3", x = -16, z = -70 }, { id = "L4", x = 16, z = -70 },
	{ id = "L5", x = -16, z = -130 }, { id = "L6", x = 16, z = -130 },
	{ id = "L7", x = -16, z = -190 }, { id = "L8", x = 16, z = -190 },
}

CityLayout.SPOTS = {
	Sign            = { x = 0, z = -8, y = 14 },          -- "FOUNDERS' QUARTER" arrival sign
	WorkshopDoor    = { x = -24, z = -60 },               -- street side of Patch's Workshop (enter)
	WorkshopCrate   = { x = -24, z = -48 },               -- Patch's supply crate (power cells), by the door
	MarketCounter   = { x = -24, z = -160 },              -- market kiosk on the sidewalk
	ChargePad       = { x = 32, z = -40 },                -- the bay's platform
	BayArm1         = { x = 27, z = -35 }, BayArm2 = { x = 37, z = -35 }, BayArm3 = { x = 32, z = -47 },
	Arrival         = { x = 0, z = -6 },                  -- where a player walks in from the facility
}

-- Patch's workshop interior is built away from the street (a door takes you there and back).
CityLayout.INTERIOR = Vector3.new(0, 0, -900)
CityLayout.INTERIOR_SPOTS = {
	Spawn   = { x = 0, z = 12 },   -- just inside the door
	Exit    = { x = 0, z = 17 },   -- the door back to the street
	Patch   = { x = 0, z = -6 },   -- Patch at the workbench
}

CityLayout.CITIZEN_ROUTE = {
	{ x = -16, z = -10 }, { x = -16, z = -60 }, { x = -16, z = -95 }, { x = -10, z = -100 },
	{ x = -16, z = -110 }, { x = -16, z = -160 }, { x = -16, z = -230 }, { x = 16, z = -230 },
	{ x = 16, z = -178 }, { x = 16, z = -120 }, { x = 10, z = -100 }, { x = 16, z = -85 },
	{ x = 16, z = -40 }, { x = 16, z = -10 },
}

return CityLayout
