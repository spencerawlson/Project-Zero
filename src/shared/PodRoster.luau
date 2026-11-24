--!strict
-- PodRoster: which player owns which stasis pod. Pure logic (no Roblox services), so it is unit testable.
-- One mission instance holds a party of 1-4 (decision D5); each member gets their own player pod.
--
-- Contract:
--   PodRoster.new(podIds)        podIds: ordered list of pod ids, e.g. {"P02", "P03", "P04", "P06"}
--   roster:claim(userId)         -> podId, or nil when every pod is taken. Idempotent: a player who already
--                                   holds a pod gets the same pod back (respawns keep their pod).
--   roster:release(userId)       frees that player's pod (no-op if they hold none) -> the freed podId or nil
--   roster:podOf(userId)         -> podId or nil
--   roster:holderOf(podId)       -> userId or nil
--   roster:freeCount()           -> number of unclaimed pods
-- Pods are handed out in list order, lowest free first, so a party fills P02, P03, P04, P06.

local PodRoster = {}
PodRoster.__index = PodRoster

export type PodRoster = typeof(setmetatable({} :: {
	_order: { string },
	_holder: { [string]: number },
	_pod: { [number]: string },
}, PodRoster))

function PodRoster.new(podIds: { string }): PodRoster
	assert(type(podIds) == "table" and #podIds > 0, "podIds must be a non-empty list")
	local seen = {}
	for _, id in ipairs(podIds) do
		assert(type(id) == "string", "pod ids must be strings")
		assert(not seen[id], "duplicate pod id " .. id)
		seen[id] = true
	end
	return setmetatable({ _order = table.clone(podIds), _holder = {}, _pod = {} }, PodRoster)
end

function PodRoster.claim(self: PodRoster, userId: number): string?
	assert(type(userId) == "number", "userId must be a number")
	local current = self._pod[userId]
	if current then
		return current
	end
	for _, id in ipairs(self._order) do
		if self._holder[id] == nil then
			self._holder[id] = userId
			self._pod[userId] = id
			return id
		end
	end
	return nil
end

function PodRoster.release(self: PodRoster, userId: number): string?
	local id = self._pod[userId]
	if id then
		self._pod[userId] = nil
		self._holder[id] = nil
	end
	return id
end

function PodRoster.podOf(self: PodRoster, userId: number): string?
	return self._pod[userId]
end

function PodRoster.holderOf(self: PodRoster, podId: string): number?
	return self._holder[podId]
end

function PodRoster.freeCount(self: PodRoster): number
	local n = 0
	for _, id in ipairs(self._order) do
		if self._holder[id] == nil then
			n += 1
		end
	end
	return n
end

return PodRoster
