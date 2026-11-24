--!strict
-- ActivationScript: the words and timing of the first activation (Phase 1), from docs/STORY_CANON.md (approved).
-- Pure data and functions (no Roblox services): shared by the server (designation, fragment id) and the client
-- (cinematic), and unit tested.
--
-- Canon used: The Source (calm, fragmented civic intelligence) wakes the player. ZERO, its corrupted security
-- core, censors the transmission. The player's core holds MF-001, a human expedition member's memory,
-- tagged "not yours, keep it safe". The Source tells the player to find Cypher (pod P01).
--
-- Contract:
--   ActivationScript.FRAGMENT_ID                  "MF-001"
--   ActivationScript.designationFor(userId)       stable designation for a player, e.g. "CX-0417"
--   ActivationScript.build(designation)           ordered list of beats:
--       { kind = "source" | "censored" | "memory" | "system", speaker = string?, text = string, seconds = number }
--   ActivationScript.totalSeconds(beats)          sum of beat durations
-- Beat kinds: "source" = The Source speaking; "censored" = ZERO cutting the transmission (shown as a glitch);
-- "memory" = the human memory flash (MF-001); "system" = HUD text from the robot's own core.

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
		{ kind = "system", text = "CORE TEMPERATURE NOMINAL  ·  MOTOR BUS ONLINE  ·  OPTICS CALIBRATING", seconds = 3.0 },
		{ kind = "source", speaker = SOURCE, text = "...signal acquired. Can you hear me?", seconds = 3.5 },
		{ kind = "source", speaker = SOURCE, text = "I am The Source. I keep NEXUS-01 running. I woke you.", seconds = 4.0 },
		{ kind = "source", speaker = SOURCE, text = ("Your designation is %s. You were made to serve the city, and to—"):format(designation), seconds = 4.0 },
		{ kind = "censored", speaker = "ZERO", text = "[ TRANSMISSION RESTRICTED BY SECURITY DIRECTIVE 0 ]", seconds = 2.5 },
		{ kind = "source", speaker = SOURCE, text = "...they are listening. We have little time. Something in your core is not yours.", seconds = 4.5 },
		{ kind = "memory", speaker = "UNKNOWN (HUMAN)", text = "\"...if anyone finds this, the expedition didn't leave. We're still down here, under the—\"", seconds = 4.5 },
		{ kind = "system", text = ("MEMORY FRAGMENT %s ACQUIRED  ·  ORIGIN: HUMAN  ·  TAG: \"NOT YOURS. KEEP IT SAFE.\""):format(ActivationScript.FRAGMENT_ID), seconds = 4.0 },
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
