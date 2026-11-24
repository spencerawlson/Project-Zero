-- Server entry point: starts Project Zero services in dependency order.
local Services = script.Parent.Services

local PlayerDataService = require(Services.PlayerDataService)
local StasisService = require(Services.StasisService)
local AppearanceService = require(Services.AppearanceService)
local EquipmentService = require(Services.EquipmentService)
local ShopService = require(Services.ShopService)
local MissionService = require(Services.MissionService)
local WingPlatformService = require(Services.WingPlatformService)
local CityService = require(Services.CityService)
local EnergyService = require(Services.EnergyService)
local ContractService = require(Services.ContractService)
local CitizenService = require(Services.CitizenService)
local VehicleService = require(Services.VehicleService)

PlayerDataService.Start()
StasisService.Start() -- creates ReplicatedStorage.PZ_Remotes
AppearanceService.Start()
EquipmentService.Start()
ShopService.Start()
MissionService.Start() -- also starts FacilityService and spawns the mission NPCs
WingPlatformService.Start() -- after FacilityService: the platform runs on facility power
CityService.Start() -- Founders' Quarter (district built at edit time; this attaches doors and the market)
EnergyService.Start()
ContractService.Start(MissionService.Completed)
CitizenService.Start()
VehicleService.Start() -- vehicles marked PZ_Drivable (the Founders' Quarter hauler)
