--!strict
-- FacilityService: the Stasis Facility's doors, lighting states and mission props (server authoritative).
--
-- Doors: the parts in PZ_StasisFacility.Doors (D01-D18, from BLD-01_greybox_build.lua). Each is "auto" (opens
-- while a robot or NPC is within OPEN_RANGE studs) or "locked" (closed, red). Closed = CanCollide on.
-- A PathfindingModifier on each door lets NPC paths pass through auto doors only.
-- Lighting (bible SF-05): "Degraded" (dim cyan, flicker) -> "Online" -> "Lockdown" (red pulse).
-- Mission props are created at runtime in PZ_StasisFacility.M01_Props (positions in the facility frame of
-- pz_layout.py: Studio X = x, Y = h, Z = -y):
--   B1..B3 breaker cabinets (R10 east wall), BreakerConsole (R10 north wall, shows the sequence),
--   MedConsole (R09 east wall), ExitZone (outside the service roll-up door D04).
-- Prompts on props fire FacilityService.PromptTriggered(name, player); MissionService enables them per step.

local Lighting = game:GetService("Lighting")
local CollectionService = game:GetService("CollectionService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local TweenService = game:GetService("TweenService")

local FacilityService = {}

local OPEN_RANGE = 8
local promptEvent = Instance.new("BindableEvent")
FacilityService.PromptTriggered = promptEvent.Event -- (name: string, player: Player)

local facility: Model
local doors: { [string]: BasePart } = {}
local doorMode: { [string]: string } = {}
local doorColour: { [string]: Color3 } = {}
local props: { [string]: Instance } = {}
local prompts: { [string]: ProximityPrompt } = {}
local lights: { Light } = {}
local neon: { BasePart } = {} -- art-pass light tubes and status strips (tag "PZ_FacilityNeon"): recoloured per lighting state
local lightState = "Degraded"
local extraCharacters: () -> { Model } = function() return {} end

local RED = Color3.fromRGB(229, 56, 59)
local GREEN = Color3.fromRGB(61, 187, 107)
local CYAN = Color3.fromHex("#22D3EE")
local OFF = Color3.fromRGB(40, 44, 50)

local function F(x: number, y: number, h: number): Vector3
	return Vector3.new(x, h, -y)
end

local function part(name: string, size: Vector3, cf: CFrame, colour: Color3, material: Enum.Material?, parent: Instance): Part
	local p = Instance.new("Part")
	p.Name = name; p.Anchored = true; p.Size = size; p.CFrame = cf; p.Color = colour
	p.Material = material or Enum.Material.Metal
	p.TopSurface = Enum.SurfaceType.Smooth; p.BottomSurface = Enum.SurfaceType.Smooth
	p.Parent = parent
	return p
end

local function addPrompt(name: string, parent: BasePart, action: string, object: string, hold: number, range: number?)
	local pr = Instance.new("ProximityPrompt")
	pr.Name = "Prompt"; pr.ActionText = action; pr.ObjectText = object; pr.HoldDuration = hold
	pr.MaxActivationDistance = range or 8; pr.RequiresLineOfSight = false; pr.Enabled = false
	pr.Parent = parent
	pr.Triggered:Connect(function(player)
		promptEvent:Fire(name, player)
	end)
	prompts[name] = pr
end

local function screen(p: BasePart, face: Enum.NormalId, text: string, colour: Color3): TextLabel
	local g = Instance.new("SurfaceGui")
	g.Face = face; g.SizingMode = Enum.SurfaceGuiSizingMode.PixelsPerStud; g.PixelsPerStud = 40; g.LightInfluence = 0
	local t = Instance.new("TextLabel")
	t.Size = UDim2.fromScale(1, 1); t.BackgroundColor3 = Color3.fromRGB(10, 14, 18); t.TextColor3 = colour
	t.Font = Enum.Font.Code; t.TextScaled = true; t.Text = text; t.Parent = g
	g.Parent = p
	return t
end

-- ---- doors ---------------------------------------------------------------------------------------------
local function renderDoor(id: string, open: boolean)
	local d = doors[id]
	local locked = doorMode[id] == "locked"
	d.CanCollide = not open
	d.Color = if locked then Color3.fromRGB(120, 24, 28) else doorColour[id]
	-- closed doors are solid (a see-through locked door looked open in the M01 playtest); open = invisible
	d.Material = if locked then Enum.Material.Neon else Enum.Material.Metal
	local target = if open then 1 else (if locked then 0.05 else 0)
	if math.abs(d.Transparency - target) > 0.01 then
		TweenService:Create(d, TweenInfo.new(0.25), { Transparency = target }):Play()
	end
	d:SetAttribute("Open", open)
end

function FacilityService.SetDoor(id: string, mode: string)
	assert(doors[id], "unknown door " .. id)
	assert(mode == "auto" or mode == "locked", "door mode must be auto or locked")
	doorMode[id] = mode
	doors[id]:SetAttribute("Mode", mode)
	local mod = doors[id]:FindFirstChildOfClass("PathfindingModifier")
	if mod then
		mod.PassThrough = mode == "auto"
	end
	renderDoor(id, false)
end

function FacilityService.DoorMode(id: string): string?
	return doorMode[id]
end

local function doorLoop()
	local acc = 0
	RunService.Heartbeat:Connect(function(dt)
		acc += dt
		if acc < 0.2 then
			return
		end
		acc = 0
		local roots = {}
		for _, p in ipairs(Players:GetPlayers()) do
			local r = p.Character and p.Character:FindFirstChild("HumanoidRootPart")
			if r then table.insert(roots, (r :: BasePart).Position) end
		end
		for _, m in ipairs(extraCharacters()) do
			local r = m:FindFirstChild("HumanoidRootPart")
			if r then table.insert(roots, (r :: BasePart).Position) end
		end
		for id, d in pairs(doors) do
			local open = false
			if doorMode[id] == "auto" then
				for _, pos in ipairs(roots) do
					local off = pos - d.Position
					if Vector3.new(off.X, 0, off.Z).Magnitude < OPEN_RANGE and math.abs(off.Y) < 12 then
						open = true
						break
					end
				end
			end
			if d:GetAttribute("Open") ~= open then
				renderDoor(id, open)
			end
		end
	end)
end

-- ---- lighting ------------------------------------------------------------------------------------------
local LIGHT = {
	Degraded = { colour = Color3.fromRGB(120, 200, 220), brightness = 0.7, ambient = Color3.fromRGB(18, 22, 28) },
	Online = { colour = Color3.fromRGB(205, 235, 255), brightness = 1.8, ambient = Color3.fromRGB(55, 62, 72) },
	-- softened 2026-11-24 (owner: the lockdown red was too strong): less red ambient, lower peak brightness
	Lockdown = { colour = Color3.fromRGB(255, 70, 75), brightness = 1.1, ambient = Color3.fromRGB(38, 22, 26) },
}

function FacilityService.SetLighting(state: string)
	local spec = LIGHT[state]
	assert(spec, "unknown lighting state " .. state)
	lightState = state
	facility:SetAttribute("Lighting", state)
	Lighting.Ambient = spec.ambient
	for _, l in ipairs(lights) do
		l.Color = spec.colour
		l.Brightness = spec.brightness
	end
	for _, n in ipairs(neon) do
		n.Color = spec.colour
		n.Transparency = if state == "Degraded" then 0.35 else 0
	end
end

local function lightingLoop()
	task.spawn(function()
		local t = 0
		while true do
			task.wait(0.15)
			t += 0.15
			if lightState == "Degraded" then
				for i, l in ipairs(lights) do -- a few failing lights flicker
					if i % 3 == 0 then
						l.Brightness = if math.random() < 0.25 then 0.1 else LIGHT.Degraded.brightness
					end
				end
			elseif lightState == "Lockdown" then
				local b = LIGHT.Lockdown.brightness * (0.55 + 0.45 * math.abs(math.sin(t * 3)))
				for _, l in ipairs(lights) do l.Brightness = b end
			end
		end
	end)
end

-- Room lighting comes from the art-pass fixtures built at edit time (Roblox/BLD-01_art_pass_R04.lua and
-- BLD-01_art_pass_rooms.lua, 2026-11-24): light bars and ceiling panels tagged PZ_FacilityLight / PZ_FacilityNeon,
-- collected in FacilityService.Start. The old runtime cube lamps were removed. If the art pass is missing (a fresh
-- greybox), a few fallback lamps keep the facility playable.
local function buildLights(folder: Folder)
	if #CollectionService:GetTagged("PZ_FacilityLight") > 0 then return end
	warn("[Facility] no art-pass lights found; using fallback lamps")
	local spots = { { 0, 64, 14, 40 }, { 0, 12, 13, 30 }, { 0, 112, 13, 30 }, { 42, 42, 12, 26 }, { 42, 78, 12, 26 } }
	for i, s in ipairs(spots) do
		local a = part("Lamp" .. i, Vector3.new(1.2, 0.3, 1.2), CFrame.new(F(s[1], s[2], s[3])), Color3.fromRGB(230, 240, 255), Enum.Material.Neon, folder)
		a.CanCollide = false; a.CanQuery = false; a.CastShadow = false
		local l = Instance.new("PointLight"); l.Range = s[4]; l.Shadows = false; l.Parent = a
		table.insert(lights, l)
	end
end

-- ---- props ---------------------------------------------------------------------------------------------
local function buildProps(folder: Folder)
	-- breakers on the R10 east wall (inner face x = 51), 8 studs apart with a 5-stud prompt reach: when several
	-- same-key prompts are in range Roblox picks the most central on screen, not the nearest (B1 fired B2 in the
	-- M01 playtest), so only the breaker the robot stands at may be in range.
	for i, id in ipairs({ "B1", "B2", "B3" }) do
		local y = 58 + i * 8
		local cab = part(id, Vector3.new(1, 5, 3), CFrame.new(F(50.4, y, 3.7)), Color3.fromHex("#2B2F36"), Enum.Material.Metal, folder)
		screen(cab, Enum.NormalId.Left, id, CYAN)
		local lamp = part(id .. "_Lamp", Vector3.new(0.3, 0.6, 1.4), CFrame.new(F(49.8, y, 6.8)), OFF, Enum.Material.Neon, folder)
		lamp.CanCollide = false
		props[id] = cab; props[id .. "_Lamp"] = lamp
		addPrompt(id, cab, "Throw breaker", "Breaker " .. id, 0.4, 5)
	end
	-- sequence console on the R10 north wall (inner face y = 95.5), screen facing south (+Z in Studio)
	local con = part("BreakerConsole", Vector3.new(3.2, 4, 1), CFrame.new(F(44, 95, 2.2)), Color3.fromHex("#2B2F36"), Enum.Material.Metal, folder)
	props.BreakerConsole = con
	props.BreakerConsoleText = screen(con, Enum.NormalId.Back, "POWER RESTART\nSEQUENCE\n-- OFFLINE --", CYAN)
	-- medical records console on the R09 east wall, screen facing west (-X)
	local med = part("MedConsole", Vector3.new(1, 4, 3), CFrame.new(F(50.5, 42, 2.2)), Color3.fromHex("#2B2F36"), Enum.Material.Metal, folder)
	props.MedConsole = med
	screen(med, Enum.NormalId.Left, "MEDICAL\nMONITORING\n1 corrupted\nrecord", Color3.fromRGB(255, 196, 120))
	addPrompt("MedConsole", med, "Access records", "Medical console", 1.0)
	-- exit zone outside the service roll-up door D04 (y = 120)
	local zone = part("ExitZone", Vector3.new(20, 12, 12), CFrame.new(F(0, 127, 6)), GREEN, Enum.Material.ForceField, folder)
	zone.Transparency = 1; zone.CanCollide = false; zone.CanQuery = false; zone.CanTouch = false
	props.ExitZone = zone
end

function FacilityService.Prop(name: string): Instance?
	return props[name]
end

function FacilityService.EnablePrompt(name: string, on: boolean)
	local pr = prompts[name]
	if pr then pr.Enabled = on end
end

function FacilityService.SetBreakerLamp(id: string, status: string)
	local lamp = props[id .. "_Lamp"] :: BasePart?
	if lamp then
		lamp.Color = if status == "ok" then GREEN elseif status == "fault" then RED else OFF
	end
end

function FacilityService.SetSequence(sequence: { string }?)
	local label = props.BreakerConsoleText :: TextLabel
	label.Text = if sequence then "POWER RESTART\nSEQUENCE\n" .. table.concat(sequence, "  >  ") else "POWER RESTART\nSEQUENCE\n-- ONLINE --"
end

function FacilityService.InExitZone(pos: Vector3): boolean
	local z = props.ExitZone :: BasePart
	local rel = z.CFrame:PointToObjectSpace(pos)
	local h = z.Size / 2
	return math.abs(rel.X) <= h.X and math.abs(rel.Y) <= h.Y and math.abs(rel.Z) <= h.Z
end

-- ---- states used by the mission ------------------------------------------------------------------------
-- Start of M01: main entrance and emergency exits sealed by ZERO, containment door and service door without power.
-- (Deviation from SF-05 I9 "exits always openable", owner-approved M01 plan: the facility is sealed until the escape.)
function FacilityService.ResetForMission()
	for id in pairs(doors) do
		FacilityService.SetDoor(id, "auto")
	end
	for _, id in ipairs({ "D01", "D03", "D04", "D05", "D06" }) do
		FacilityService.SetDoor(id, "locked")
	end
	FacilityService.SetLighting("Degraded")
	for _, id in ipairs({ "B1", "B2", "B3" }) do FacilityService.SetBreakerLamp(id, "off") end
end

function FacilityService.PowerOn()
	FacilityService.SetLighting("Online")
	FacilityService.SetDoor("D03", "auto")
	for _, id in ipairs({ "B1", "B2", "B3" }) do FacilityService.SetBreakerLamp(id, "ok") end
	FacilityService.SetSequence(nil)
end

function FacilityService.Lockdown()
	FacilityService.SetLighting("Lockdown")
	FacilityService.SetDoor("D01", "locked")
	FacilityService.SetDoor("D02", "locked")
	FacilityService.SetDoor("D04", "auto")
end

function FacilityService.FreeRoam()
	for id in pairs(doors) do
		FacilityService.SetDoor(id, "auto")
	end
	FacilityService.SetLighting("Online")
	FacilityService.SetSequence(nil)
end

function FacilityService.SetExtraCharacters(fn: () -> { Model })
	extraCharacters = fn
end

function FacilityService.Start()
	facility = workspace:WaitForChild("PZ_StasisFacility", 30) :: Model
	assert(facility, "FacilityService: PZ_StasisFacility not found")
	for _, d in ipairs((facility:FindFirstChild("Doors") :: Folder):GetChildren()) do
		if d:IsA("BasePart") then
			doors[d.Name] = d
			doorColour[d.Name] = d.Color
			local mod = Instance.new("PathfindingModifier"); mod.PassThrough = true; mod.Parent = d
		end
	end
	local old = facility:FindFirstChild("M01_Props"); if old then old:Destroy() end
	local folder = Instance.new("Folder"); folder.Name = "M01_Props"; folder.Parent = facility
	buildProps(folder)
	buildLights(folder)
	-- art-pass fixtures (built at edit time) follow the same lighting states
	for _, l in ipairs(CollectionService:GetTagged("PZ_FacilityLight")) do
		if l:IsA("Light") and l:IsDescendantOf(facility) then table.insert(lights, l) end
	end
	for _, p in ipairs(CollectionService:GetTagged("PZ_FacilityNeon")) do
		if p:IsA("BasePart") and p:IsDescendantOf(facility) then table.insert(neon, p) end
	end
	FacilityService.ResetForMission()
	doorLoop()
	lightingLoop()
end

return FacilityService
