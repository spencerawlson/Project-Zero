-- Tests for ReplicatedStorage.Shared.ProfileSchema (contract in the module header).
-- Covers defaults, migration of partial/old saves, protection against newer schemas, and input immutability.
return function(t)
	local ProfileSchema = require(game:GetService("ReplicatedStorage").Shared.ProfileSchema)
	local expect = t.expect

	-- A new profile is at the current schema version, owned by the user, and starts un-activated.
	t.test("default profile has the current version and owner", function()
		local p = ProfileSchema.default(42, 1000)
		expect.equal(p.schemaVersion, ProfileSchema.VERSION)
		expect.equal(p.userId, 42)
		expect.equal(p.createdAt, 1000)
		expect.equal(p.lastSeenAt, 1000)
		expect.falsy(p.progress.activated)
		expect.equal(p.stats.sessions, 0)
	end)

	-- Every new player starts in, and owns, the standard starter chassis (owner decision D2).
	t.test("default profile starts in the starter chassis", function()
		local p = ProfileSchema.default(1, 0)
		expect.equal(p.chassis.current, ProfileSchema.STARTER_CHASSIS)
		expect.deepEqual(p.chassis.owned, { ProfileSchema.STARTER_CHASSIS })
	end)

	-- Invalid input fails loudly instead of producing a broken profile.
	t.test("default rejects a non-number userId", function()
		expect.throws(function() ProfileSchema.default("abc" :: any, 0) end)
	end)

	-- No saved data means a fresh default profile.
	t.test("migrate of nil returns a default profile", function()
		local p = ProfileSchema.migrate(nil, 7, 500)
		expect.deepEqual(p, ProfileSchema.default(7, 500))
	end)

	-- Values already saved are kept; only missing fields are filled.
	t.test("migrate keeps existing saved values", function()
		local saved = ProfileSchema.default(7, 100)
		saved.progress.activated = true
		saved.chassis.owned = { "CypherFrame", "MedFrame" }
		saved.stats.sessions = 9
		local p = ProfileSchema.migrate(saved, 7, 999)
		expect.truthy(p.progress.activated)
		expect.deepEqual(p.chassis.owned, { "CypherFrame", "MedFrame" })
		expect.equal(p.stats.sessions, 9)
		expect.equal(p.createdAt, 100)
	end)

	-- A partial / version-0 save gains every missing nested field from the defaults.
	t.test("migrate fills missing nested fields", function()
		local p = ProfileSchema.migrate({ progress = { activated = true } }, 7, 50)
		expect.truthy(p.progress.activated)
		expect.deepEqual(p.progress.missions, {})
		expect.deepEqual(p.progress.memoryFragments, {})
		expect.equal(p.chassis.current, ProfileSchema.STARTER_CHASSIS)
		expect.equal(p.schemaVersion, ProfileSchema.VERSION)
	end)

	-- Unknown fields written by other systems are preserved, not dropped.
	t.test("migrate preserves unknown fields", function()
		local saved = ProfileSchema.default(7, 1)
		saved.futureFeature = { level = 3 }
		local p = ProfileSchema.migrate(saved, 7, 2)
		expect.deepEqual(p.futureFeature, { level = 3 })
	end)

	-- Data from a newer server version must never be downgraded.
	t.test("migrate refuses a newer schema version", function()
		expect.throws(function()
			ProfileSchema.migrate({ schemaVersion = ProfileSchema.VERSION + 1 }, 7, 0)
		end)
	end)

	-- Migration returns a new table and leaves the caller's saved table untouched.
	t.test("migrate does not mutate its input", function()
		local saved = { progress = { activated = true } }
		ProfileSchema.migrate(saved, 7, 0)
		expect.equal(saved.chassis, nil)
		expect.equal(saved.schemaVersion, nil)
	end)
end
