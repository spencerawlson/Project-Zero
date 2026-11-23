-- Tests for ServerScriptService.Server.ProfileStore (contract in the module header).
-- Uses an in-memory fake DataStore and an injected clock: no network, no real time.
return function(t)
	local ProfileStore = require(game:GetService("ServerScriptService").Server.ProfileStore)
	local expect = t.expect

	-- Fake DataStore with UpdateAsync semantics: transform(old) -> new, or nil for "no write".
	local function makeFakeStore()
		local data = {}
		local fake = { data = data, writes = 0 }
		function fake:UpdateAsync(key, transform)
			local new = transform(data[key])
			if new ~= nil then
				data[key] = new
				self.writes += 1
			end
			return data[key]
		end
		return fake
	end

	local function clock(start)
		local t0 = { now = start }
		return t0, function() return t0.now end
	end

	-- First load creates a profile, counts one session, and locks the record to this server.
	t.test("first load creates a locked profile", function()
		local fake = makeFakeStore()
		local _, now = clock(100)
		local s = ProfileStore.new({ store = fake, jobId = "A", now = now })
		local p, err = s:load(5)
		expect.equal(err, nil)
		expect.equal(p.userId, 5)
		expect.equal(p.stats.sessions, 1)
		expect.equal(fake.data["u_5"].lock.jobId, "A")
	end)

	-- Loading again from the same server is allowed and counts another session.
	t.test("reload by the same server increments sessions", function()
		local fake = makeFakeStore()
		local _, now = clock(100)
		local s = ProfileStore.new({ store = fake, jobId = "A", now = now })
		s:load(5)
		local p = s:load(5)
		expect.equal(p.stats.sessions, 2)
	end)

	-- Another live session's lock blocks the load and leaves its data unchanged.
	t.test("load is refused while another server holds a fresh lock", function()
		local fake = makeFakeStore()
		local c, now = clock(100)
		ProfileStore.new({ store = fake, jobId = "A", now = now }):load(5)
		local before = fake.data["u_5"]
		c.now = 200
		local p, err = ProfileStore.new({ store = fake, jobId = "B", now = now }):load(5)
		expect.equal(p, nil)
		expect.equal(err, "locked")
		expect.equal(fake.data["u_5"], before)
	end)

	-- A lock older than lockTtl is stale (crashed server) and is taken over.
	t.test("stale lock is taken over", function()
		local fake = makeFakeStore()
		local c, now = clock(100)
		ProfileStore.new({ store = fake, jobId = "A", now = now, lockTtl = 60 }):load(5)
		c.now = 100 + 61
		local p, err = ProfileStore.new({ store = fake, jobId = "B", now = now, lockTtl = 60 }):load(5)
		expect.equal(err, nil)
		expect.equal(p.stats.sessions, 2)
		expect.equal(fake.data["u_5"].lock.jobId, "B")
	end)

	-- Saved progress is what the next load returns.
	t.test("save then load round-trips progress", function()
		local fake = makeFakeStore()
		local _, now = clock(100)
		local s = ProfileStore.new({ store = fake, jobId = "A", now = now })
		local p = s:load(5)
		p.progress.activated = true
		p.progress.memoryFragments["MF-001"] = true
		local ok = s:save(5, p, true)
		expect.truthy(ok)
		local again = s:load(5)
		expect.truthy(again.progress.activated)
		expect.truthy(again.progress.memoryFragments["MF-001"])
	end)

	-- Releasing on save clears the lock so another server can load immediately.
	t.test("save with release clears the lock", function()
		local fake = makeFakeStore()
		local _, now = clock(100)
		local s = ProfileStore.new({ store = fake, jobId = "A", now = now })
		local p = s:load(5)
		s:save(5, p, true)
		expect.equal(fake.data["u_5"].lock, nil)
		local p2, err = ProfileStore.new({ store = fake, jobId = "B", now = now }):load(5)
		expect.equal(err, nil)
		expect.truthy(p2)
	end)

	-- A server that lost its lock must not overwrite the new owner's data.
	t.test("save is refused after another server took the lock", function()
		local fake = makeFakeStore()
		local c, now = clock(100)
		local a = ProfileStore.new({ store = fake, jobId = "A", now = now, lockTtl = 60 })
		local pa = a:load(5)
		c.now = 200 -- A's lock is now stale
		ProfileStore.new({ store = fake, jobId = "B", now = now, lockTtl = 60 }):load(5)
		local writes = fake.writes
		pa.progress.activated = true
		local ok, err = a:save(5, pa, false)
		expect.falsy(ok)
		expect.equal(err, "lock lost")
		expect.equal(fake.writes, writes)
		expect.falsy(fake.data["u_5"].data.progress.activated)
	end)

	-- Store failures surface to the caller (who decides whether to retry).
	t.test("store errors propagate", function()
		local broken = { UpdateAsync = function() error("DataStore unavailable") end }
		local s = ProfileStore.new({ store = broken, jobId = "A", now = function() return 0 end })
		expect.throws(function() s:load(5) end)
	end)

	-- Construction without required dependencies fails fast.
	t.test("new requires store, jobId and now", function()
		expect.throws(function() ProfileStore.new({ jobId = "A", now = os.time } :: any) end)
	end)
end
