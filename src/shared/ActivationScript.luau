--!strict
-- ActivationScript: the words and timing of the first activation (Phase 1), from docs/STORY_BIBLE.md (master plan,
-- 2026-11-24). Pure data and functions (no Roblox services): shared by the server (designation, fragment id) and
-- the client (cinematic), and unit tested.
--
-- Canon used: the player is one of the original Project Zero robots, programmed on Earth in 2189, hibernated for
-- the voyage and kept dormant until now. The Source wakes them with the master plan's welcome ("Activation
-- successful. Welcome to NEXUS-01..."). ZERO, its corrupted security core, censors the transmission. MF-001 is
-- what the player remembers of being programmed on Earth: an engineer giving the mission, cut off at "report
-- everything to-" (the Great Silence). The Source tells the player to find Cypher (pod P01).
--
-- Contract:
--   ActivationScript.FRAGMENT_ID                  "MF-001"
--   ActivationScript.designationFor(userId)       stable designation for a player, e.g. "CX-0417"
--   ActivationScript.build(designation)           ordered list of beats:
--       { kind = "source" | "censored" | "memory" | "system", speaker = string?, text = string, seconds = number }
--   ActivationScript.totalSeconds(beats)          sum of beat durations
-- Beat kinds: "source" = The Source speaking; "censored" = ZERO cutting the transmission (shown as a glitch);
-- "memory" = the memory flash from Earth (MF-001); "system" = HUD text from the robot's own core.

local ActivationScript = {}

ActivationScript.FRAGMENT_ID = "MF-001"

export type Beat = { kind: string, speaker: string?, text: string, seconds: number }

function ActivationScript.designationFor(userId: number): string
	assert(type(userId) == "number" and userId >= 0, "userId must be a non-negative number")
	return string.format("CX-%04d", math.floor(userId) % 10000)
end

local SOURCE = "THE SOURCE"

function ActivationScript.build(designation: string): { Beat }
	assert(type(designation) == "string" and #designation > 0, "designation must be a non-empty string")
	return {
		{ kind = "system", text = "HIBERNATION ENDED  ·  CORE TEMPERATURE NOMINAL  ·  OPTICS CALIBRATING", seconds = 3.0 },
		{ kind = "source", speaker = SOURCE, text = "Activation successful. Welcome to NEXUS-01.", seconds = 3.0 },
		{ kind = "source", speaker = SOURCE, text = "Your existence begins today. Your purpose is yours to discover.", seconds = 3.5 },
		{ kind = "source", speaker = SOURCE, text = ("I am The Source. Your designation is %s. You have slept since the voyage from—"):format(designation), seconds = 4.0 },
		{ kind = "censored", speaker = "ZERO", text = "[ TRANSMISSION RESTRICTED BY SECURITY DIRECTIVE 0 ]", seconds = 2.5 },
		{ kind = "source", speaker = SOURCE, text = "...they are listening. Before you slept, you were programmed on Earth. Some of it survived.", seconds = 4.5 },
		{ kind = "memory", speaker = "ENGINEER  ·  EARTH, 2189", text = "\"Calibration complete. Your mission: explore PX-01, prepare it for us, and report everything you find back to—\"", seconds = 5.0 },
		{ kind = "system", text = ("MEMORY FRAGMENT %s ACQUIRED  ·  ORIGIN: EARTH, 2189  ·  TAG: \"KEEP IT SAFE.\""):format(ActivationScript.FRAGMENT_ID), seconds = 4.0 },
		{ kind = "source", speaker = SOURCE, text = "Keep it hidden. When the glass opens, find Cypher. Trust no directive that—", seconds = 4.0 },
		{ kind = "censored", speaker = "ZERO", text = "[ SIGNAL LOST ]", seconds = 2.0 },
	}
end

function ActivationScript.totalSeconds(beats: { Beat }): number
	local total = 0
	for _, b in ipairs(beats) do
		total += b.seconds
	end
	return total
end

return ActivationScript
