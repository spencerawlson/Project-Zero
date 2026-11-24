--!strict
-- ProfileStore: session-locked load/save of player profiles on top of a DataStore-like object.
-- All Roblox-specific dependencies are injected, so the logic is unit testable with a fake store.
--
-- Contract:
--   ProfileStore.new({ store, jobId, now, lockTtl? }) -> store object
--     store   : object with UpdateAsync(self, key, transform) like a DataStore (transform(old) -> new | nil = no write)
--     jobId   : string identifying this server (game.JobId in production)
--     now     : function() -> number (seconds); injected so tests are deterministic
--     lockTtl : seconds after which another server's lock counts as stale (default 1800)
--   store:load(userId) -> (profile, nil) on success
--                      -> (nil, "locked") if another live session holds the profile
--     On success the saved record is marked as locked by this jobId, sessions is incremented once,
--     and lastSeenAt = now(). A lock held by this same jobId, or a stale lock, is taken over.
--   store:save(userId, profile, release) -> (true, nil) | (false, "lock lost")
--     Writes the profile only while this jobId still owns the lock (never overwrites another session's data).
--     release = true clears the lock in the same write.
--   Errors raised by the underlying store propagate to the caller (callers decide on retries).
--   Key format: "u_<userId>".

local ProfileSchema = require(game:GetService("ReplicatedStorage").Shared.ProfileSchema)

local ProfileStore = {}
ProfileStore.__index = ProfileStore

export type Deps = {
	store: any,
	jobId: string,
	now: () -> number,
	lockTtl: number?,
}

function ProfileStore.new(deps: Deps)
	assert(deps and deps.store and type(deps.jobId) == "string" and type(deps.now) == "function", "store, jobId and now are required")
	local self = setmetatable({}, ProfileStore)
	self._store = deps.store
	self._jobId = deps.jobId
	self._now = deps.now
	self._lockTtl = deps.lockTtl or 1800
	return self
end

function ProfileStore.key(userId: number): string
	return "u_" .. tostring(userId)
end

function ProfileStore:load(userId: number)
	local now = self._now()
	local locked = false
	local result
	self._store:UpdateAsync(ProfileStore.key(userId), function(old)
		local record = old or {}
		local lock = record.lock
		if lock and lock.jobId ~= self._jobId and (now - (lock.time or 0)) < self._lockTtl then
			locked = true
			return nil -- leave the other session's data untouched
		end
		locked = false
		local profile = ProfileSchema.migrate(record.data, userId, now)
		profile.stats.sessions += 1
		profile.lastSeenAt = now
		result = profile
		return { data = profile, lock = { jobId = self._jobId, time = now } }
	end)
	if locked then
		return nil, "locked"
	end
	return result, nil
end

function ProfileStore:save(userId: number, profile: any, release: boolean?)
	local now = self._now()
	local owned = false
	self._store:UpdateAsync(ProfileStore.key(userId), function(old)
		local record = old or {}
		if not (record.lock and record.lock.jobId == self._jobId) then
			owned = false
			return nil
		end
		owned = true
		profile.lastSeenAt = now
		return { data = profile, lock = if release then nil else { jobId = self._jobId, time = now } }
	end)
	if not owned then
		return false, "lock lost"
	end
	return true, nil
end

return ProfileStore
