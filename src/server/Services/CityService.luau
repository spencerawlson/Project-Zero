--!strict
-- CityService: brings the Founders' Quarter to life (docs/NEXUS_01_CITY.md). The district itself is built at edit
-- time (Roblox/CITY-01_founders_quarter_build.lua) and saved in the place as workspace.PZ_FoundersQuarter; this
-- service only attaches behaviour to it, by part name:
--   * Patch's Workshop door: "Enter" takes the robot to the workshop interior (built apart from the street), and
--     the interior's "Exit" brings it back to the sidewalk. Interiors are a common Roblox pattern: the street stays
--     light and the interior can be detailed.
--   * Market counter: "Trade" opens the vendor window (ShopService; purchases need the robot at the counter).
-- Other services ask for anchors: CityService.Anchor(name), CityService.InteriorSpot(name), CityService.Light(id).

local ReplicatedStorage = game:GetService("ReplicatedStorage")

local CityLayout = require(ReplicatedStorage.Shared.CityLayout)
local ShopService = require(script.Parent.ShopService)

local CityService = {}

local district: Instance? = nil

function CityService.Ready(): boolean
	return district ~= nil
end

function CityService.Anchor(name: string): BasePart?
	local a = district and district:FindFirstChild("Anchors")
	return a and a:FindFirstChild(name) :: BasePart?
end

function CityService.InteriorSpot(name: string): BasePart?
	local i = district and district:FindFirstChild("WorkshopInterior")
	return i and i:FindFirstChild(name) :: BasePart?
end

function CityService.Light(id: string): Model?
	local f = district and district:FindFirstChild("Lights")
	return f and f:FindFirstChild(id) :: Model?
end

local function prompt(parent: Instance, action: string, object: string, hold: number?, range: number?): ProximityPrompt
	local p = Instance.new("ProximityPrompt")
	p.ActionText = action; p.ObjectText = object; p.HoldDuration = hold or 0
	p.MaxActivationDistance = range or 8; p.RequiresLineOfSight = false
	p.Parent = parent
	return p
end

-- Move a character to a spot, facing `look` (keeps it upright; a short anchor stops it sliding on arrival).
local function teleport(player: Player, spot: Vector3, look: Vector3)
	local c = player.Character
	local root = c and c:FindFirstChild("HumanoidRootPart") :: BasePart?
	local hum = c and c:FindFirstChildOfClass("Humanoid")
	if not root or not hum or hum.Health <= 0 then return end
	local y = spot.Y + hum.HipHeight + root.Size.Y / 2 + 0.2
	c:PivotTo(CFrame.lookAt(Vector3.new(spot.X, y, spot.Z), Vector3.new(look.X, y, look.Z)))
end

function CityService.Start()
	district = workspace:WaitForChild("PZ_FoundersQuarter", 20)
	if not district then
		warn("[City] workspace.PZ_FoundersQuarter is missing: run Roblox/CITY-01_founders_quarter_build.lua in Studio")
		return
	end
	-- workshop door <-> interior
	local door = CityService.Anchor("WorkshopDoor")
	local inside = CityService.InteriorSpot("Spawn")
	local exit = CityService.InteriorSpot("Exit")
	local patch = CityService.InteriorSpot("Patch")
	if door and inside and exit then
		prompt(door, "Enter", "Patch's Workshop", 0, 9).Triggered:Connect(function(player)
			teleport(player, inside.Position, (patch or inside).Position)
		end)
		prompt(exit, "Exit", "To the street", 0, 9).Triggered:Connect(function(player)
			local out = door.Position + Vector3.new(6, 0, 0) -- on the sidewalk, toward the road
			teleport(player, out, out + Vector3.new(1, 0, 0))
		end)
	end
	-- market counter
	local counter = CityService.Anchor("MarketCounter")
	if counter then
		ShopService.SetVendor(counter)
		prompt(counter, "Trade", "Circuit Market", 0, 9).Triggered:Connect(function(player)
			ShopService.Open(player)
		end)
	end
end

return CityService
