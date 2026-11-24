--!strict
-- ContractRules: civilian jobs (contracts) as pure logic: who offers them, their steps, rewards and cooldowns
-- (docs/NEXUS_01_CITY.md §2). No Roblox services: unit tested; ContractService applies them to the world.
--
-- Contracts in the Founders' Quarter slice (Patch, engineering):
--   C01 "Lights Out": take a power cell from the workshop crate, install it in a dark street light (hold E), one
--       cell at a time, for each target light; then report to Patch.
--   C02 "Bay Calibration": needs the engineering toolkit and C01 done once; calibrate each arm of the Charge Bay;
--       then report to Patch.
--
-- Contract:
--   ContractRules.CONTRACTS[id] = { id, title, giver, career, kind = "deliver" | "calibrate", targetCount,
--       first = { credits, xp }, repeat_ = { credits, xp }, cooldown (s), requiresItem?, requiresContract? }
--   ContractRules.canStart(profile, id, now) -> ok, reason?  ("unknown" | "needs_item" | "needs_contract" | "cooldown")
--   ContractRules.new(id, targets)           -> state { id, step, carrying, done = { [target] = true }, targets }
--       steps: "collect" -> "install" (deliver) | "calibrate" (calibrate) -> "report" -> "complete"
--   ContractRules.apply(state, event, arg)   -> effects (list); state updated in place. Events:
--       "take_cell"            (deliver, step collect)            -> { "carrying" }
--       "install", target      (deliver, step install, carrying) -> { { "done", target }, ... }
--       "calibrate", target    (calibrate)                        -> { { "done", target }, ... }
--       "report"               (step report)                      -> { "complete" }
--       Events that don't fit change nothing and return {}. "objective" is added whenever the step changes.
--   ContractRules.objective(state)          -> { title, hint, targets = remaining target ids, pickup = boolean }
--   ContractRules.reward(profile, id, now)  -> { credits, xp, first } and records it on the profile
--       (wallet.credits, careers[career].xp, contracts[id].completions / lastCompletedAt)

local ContractRules = {}

ContractRules.CONTRACTS = {
	C01 = {
		id = "C01", title = "Lights Out", giver = "Patch", career = "engineering", kind = "deliver", targetCount = 3,
		first = { credits = 120, xp = 50 }, repeat_ = { credits = 40, xp = 20 }, cooldown = 300,
	},
	C02 = {
		id = "C02", title = "Bay Calibration", giver = "Patch", career = "engineering", kind = "calibrate", targetCount = 3,
		first = { credits = 150, xp = 60 }, repeat_ = { credits = 150, xp = 30 }, cooldown = 300,
		requiresItem = "toolkit_engineering", requiresContract = "C01",
	},
}

export type State = { id: string, step: string, carrying: boolean, done: { [string]: boolean }, targets: { string } }

local function record(profile: any, id: string)
	profile.contracts = profile.contracts or {}
	return profile.contracts[id]
end

function ContractRules.canStart(profile: any, id: string, now: number): (boolean, string?)
	local c = ContractRules.CONTRACTS[id]
	if not c then return false, "unknown" end
	if c.requiresItem and not (profile.items and profile.items[c.requiresItem]) then return false, "needs_item" end
	if c.requiresContract then
		local r = record(profile, c.requiresContract)
		if not r or r.completions < 1 then return false, "needs_contract" end
	end
	local r = record(profile, id)
	if r and now - r.lastCompletedAt < c.cooldown then return false, "cooldown" end
	return true, nil
end

function ContractRules.new(id: string, targets: { string }): State
	local c = ContractRules.CONTRACTS[id]
	assert(c, "unknown contract " .. tostring(id))
	assert(#targets == c.targetCount, ("%s needs %d targets"):format(id, c.targetCount))
	return { id = id, step = if c.kind == "deliver" then "collect" else "calibrate", carrying = false, done = {},
		targets = table.clone(targets) }
end

local function remaining(state: State): { string }
	local out = {}
	for _, t in ipairs(state.targets) do
		if not state.done[t] then table.insert(out, t) end
	end
	return out
end

function ContractRules.apply(state: State, event: string, arg: any): { any }
	local c = ContractRules.CONTRACTS[state.id]
	if c.kind == "deliver" then
		if event == "take_cell" and state.step == "collect" then
			state.carrying = true
			state.step = "install"
			return { "carrying", "objective" }
		elseif event == "install" and state.step == "install" and state.carrying
			and table.find(state.targets, arg) and not state.done[arg] then
			state.done[arg] = true
			state.carrying = false
			state.step = if #remaining(state) == 0 then "report" else "collect"
			return { { "done", arg }, "objective" }
		end
	elseif c.kind == "calibrate" then
		if event == "calibrate" and state.step == "calibrate" and table.find(state.targets, arg) and not state.done[arg] then
			state.done[arg] = true
			if #remaining(state) == 0 then state.step = "report" end
			return { { "done", arg }, "objective" }
		end
	end
	if event == "report" and state.step == "report" then
		state.step = "complete"
		return { "complete" }
	end
	return {}
end

function ContractRules.objective(state: State)
	local c = ContractRules.CONTRACTS[state.id]
	local left = remaining(state)
	local n = c.targetCount - #left
	if state.step == "collect" then
		return { title = c.title, hint = ("Take a power cell from Patch's crate (%d/%d lights fixed)."):format(n, c.targetCount),
			targets = left, pickup = true }
	elseif state.step == "install" then
		return { title = c.title, hint = ("Install the cell in a dark street light (%d/%d)."):format(n, c.targetCount),
			targets = left, pickup = false }
	elseif state.step == "calibrate" then
		return { title = c.title, hint = ("Calibrate the Charge Bay arms (%d/%d)."):format(n, c.targetCount),
			targets = left, pickup = false }
	elseif state.step == "report" then
		return { title = c.title, hint = "Report back to Patch.", targets = {}, pickup = false }
	end
	return { title = c.title, hint = "Contract complete.", targets = {}, pickup = false }
end

function ContractRules.reward(profile: any, id: string, now: number)
	local c = ContractRules.CONTRACTS[id]
	assert(c, "unknown contract " .. tostring(id))
	profile.contracts = profile.contracts or {}
	local r = profile.contracts[id]
	local first = r == nil or r.completions == 0
	local pay = if first then c.first else c.repeat_
	profile.contracts[id] = { completions = (if r then r.completions else 0) + 1, lastCompletedAt = now }
	profile.wallet.credits += pay.credits
	profile.careers = profile.careers or {}
	profile.careers[c.career] = profile.careers[c.career] or { xp = 0 }
	profile.careers[c.career].xp += pay.xp
	return { credits = pay.credits, xp = pay.xp, first = first }
end

return ContractRules
