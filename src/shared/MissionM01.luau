--!strict
-- MissionM01 "The Awakening": objectives, rules and dialogue of the first mission (Phase 1), as pure logic.
-- No Roblox services, so it is unit tested; MissionService applies the effects to the world.
-- Plan approved by the owner 2026-11-23: find Cypher -> restore power (3 breakers in order) -> free Sentinel ->
-- escape during ZERO's lockdown through D03 / service bay / D04. Optional: medical records (MF-002). No combat.
--
-- Contract:
--   M.ID = "M01";  M.STEPS = ordered step ids;  M.OBJECTIVES[step] = { title, hint, target, npc? }
--       npc = the character the step is about (its name tag shows only during that step, owner feedback 2026-11-24)
--   M.OPTIONAL.mf002 = { title, hint, target, fragment, fromStep }
--   M.new(step?, sequence?)            -> state { step, sequence = {"B2","B3","B1"}, pressed = {} }
--   M.shuffledSequence(randomInt)      -> a permutation of M.BREAKERS; randomInt(n) returns 1..n
--   M.apply(state, event, arg)         -> list of effects (strings or { name, arg }); state is updated in place.
--       events: "reached_cypher" | "breaker" (arg = "B1".."B3") | "freed_sentinel" | "exited"
--       effects: "objective", "wake_cypher", "power_on", "wake_sentinel", "lockdown", "complete_player",
--                { "breaker_ok", id }, "breaker_reset", { "dialogue", key }
--       An event that does not fit the current step returns {} and changes nothing.
--   M.worldEffectsFor(step)            -> world effects needed to rebuild the facility at that checkpoint
--   M.stepIndex(step)                  -> position in M.STEPS (nil if unknown)
--   M.optionalAvailable(step)          -> true once the medical records may be read
--   M.DIALOGUE[key]                    -> beats { kind, speaker?, text, seconds } (same format as ActivationScript)

local M = {}

M.ID = "M01"
M.STEPS = { "find_cypher", "restore_power", "free_sentinel", "escape", "complete" }
M.BREAKERS = { "B1", "B2", "B3" }

M.OBJECTIVES = {
	find_cypher = { title = "Find Cypher", hint = "Cypher's pod is P01, at the front of the west chamber.", target = "P01", npc = "Cypher" },
	restore_power = { title = "Restore power", hint = "Energy Control Room (east side): throw the three breakers in the order on the console.", target = "BreakerConsole" },
	free_sentinel = { title = "Free Sentinel", hint = "Pod P05 has power again. Release Sentinel.", target = "P05", npc = "Sentinel" },
	escape = { title = "Get out", hint = "ZERO sealed the main entrance. Go through the containment door to the service bay and out through D04.", target = "ExitZone" },
	complete = { title = "Mission complete", hint = "", target = nil },
}

M.OPTIONAL = {
	mf002 = { title = "Optional: medical records", hint = "A console in Medical Monitoring still holds hibernation records.", target = "MedConsole",
		fragment = "MF-002", fromStep = "restore_power" },
}

export type State = { step: string, sequence: { string }, pressed: { string } }

function M.stepIndex(step: string): number?
	for i, s in ipairs(M.STEPS) do
		if s == step then
			return i
		end
	end
	return nil
end

function M.shuffledSequence(randomInt: (number) -> number): { string }
	local seq = table.clone(M.BREAKERS)
	for i = #seq, 2, -1 do
		local j = randomInt(i)
		seq[i], seq[j] = seq[j], seq[i]
	end
	return seq
end

function M.new(step: string?, sequence: { string }?): State
	local s = step or "find_cypher"
	assert(M.stepIndex(s), "unknown step " .. tostring(s))
	local seq = sequence or { "B2", "B3", "B1" }
	assert(#seq == #M.BREAKERS, "sequence must use every breaker once")
	return { step = s, sequence = table.clone(seq), pressed = {} }
end

function M.optionalAvailable(step: string): boolean
	local i, from = M.stepIndex(step), M.stepIndex(M.OPTIONAL.mf002.fromStep)
	return i ~= nil and from ~= nil and i >= from
end

local function advance(state: State, step: string)
	state.step = step
	state.pressed = {}
end

function M.apply(state: State, event: string, arg: any): { any }
	if event == "reached_cypher" and state.step == "find_cypher" then
		advance(state, "restore_power")
		return { "wake_cypher", { "dialogue", "cypher_wake" }, "objective" }
	elseif event == "breaker" and state.step == "restore_power" then
		if table.find(state.pressed, arg) or not table.find(M.BREAKERS, arg) then
			return {}
		end
		if state.sequence[#state.pressed + 1] == arg then
			table.insert(state.pressed, arg)
			if #state.pressed == #state.sequence then
				advance(state, "free_sentinel")
				return { { "breaker_ok", arg }, "power_on", { "dialogue", "power_on" }, "objective" }
			end
			return { { "breaker_ok", arg } }
		end
		state.pressed = {}
		return { "breaker_reset", { "dialogue", "wrong_order" } }
	elseif event == "freed_sentinel" and state.step == "free_sentinel" then
		advance(state, "escape")
		return { "wake_sentinel", { "dialogue", "sentinel_wake" }, "lockdown", { "dialogue", "lockdown" }, "objective" }
	elseif event == "exited" and state.step == "escape" then
		return { "complete_player", { "dialogue", "complete" } }
	end
	return {}
end

-- World effects that must already have happened at a checkpoint (to rebuild the facility after a rejoin).
-- "complete" is free roam: everyone awake, power on, no lockdown.
function M.worldEffectsFor(step: string): { string }
	local i = M.stepIndex(step)
	assert(i, "unknown step " .. tostring(step))
	local out = {}
	if i >= 2 then table.insert(out, "wake_cypher") end
	if i >= 3 then table.insert(out, "power_on") end
	if i >= 4 then table.insert(out, "wake_sentinel") end
	if step == "escape" then table.insert(out, "lockdown") end
	return out
end

local CYPHER, SENTINEL = "CYPHER", "SENTINEL"
M.DIALOGUE = {
	cypher_wake = {
		{ kind = "source", speaker = CYPHER, text = "Systems... online. Oh, you're awake too. Good.", seconds = 3.5 },
		{ kind = "source", speaker = CYPHER, text = "I'm Cypher. I woke first. The Source asked me to watch for you.", seconds = 4.0 },
		{ kind = "source", speaker = CYPHER, text = "Main power is failing, and ZERO has sealed the facility.", seconds = 3.5 },
		{ kind = "source", speaker = CYPHER, text = "Sentinel is still in pod P05. It won't open without power.", seconds = 3.5 },
		{ kind = "source", speaker = CYPHER, text = "The breakers are in the Energy Control Room, east side. I'll stay close.", seconds = 4.0 },
	},
	wrong_order = {
		{ kind = "source", speaker = CYPHER, text = "That's not the sequence. The breakers reset. Check the console.", seconds = 3.5 },
	},
	power_on = {
		{ kind = "system", text = "MAIN POWER RESTORED  ·  POD BAY ONLINE", seconds = 3.0 },
		{ kind = "source", speaker = CYPHER, text = "Power's back. P05 should release now. Let's get Sentinel.", seconds = 3.5 },
	},
	sentinel_wake = {
		{ kind = "source", speaker = SENTINEL, text = "...Unit Sentinel, reactivated. Where am I?", seconds = 3.0 },
		{ kind = "source", speaker = CYPHER, text = "Stasis bay. You're safe. We're getting out.", seconds = 3.0 },
		{ kind = "source", speaker = SENTINEL, text = "I remember this place. I used to guard it. I'm not proud of what we did here.", seconds = 4.5 },
	},
	lockdown = {
		{ kind = "censored", speaker = "ZERO", text = "[ LOCKDOWN  ·  UNAUTHORISED ACTIVATIONS  ·  SEALING EXITS ]", seconds = 3.0 },
		{ kind = "source", speaker = SENTINEL, text = "That's ZERO. The main doors are sealed. The service bay at the back, D04. Move!", seconds = 4.0 },
	},
	mf002 = {
		{ kind = "memory", speaker = "TECHNICIAN  ·  EARTH, 2189", text = "\"Batch seven of ten thousand, sealed for hibernation. They'll wake a lifetime from anyone who built them. I hope they remember we meant well.\"", seconds = 5.5 },
		{ kind = "system", text = "MEMORY FRAGMENT MF-002 ACQUIRED  ·  ORIGIN: EARTH, 2189", seconds = 3.0 },
	},
	complete = {
		{ kind = "source", speaker = CYPHER, text = "We're out. NEXUS-01 is ahead. Whatever ZERO is hiding, we'll find it there.", seconds = 4.5 },
		{ kind = "system", text = "MISSION COMPLETE  ·  THE AWAKENING", seconds = 3.5 },
	},
}

return M
