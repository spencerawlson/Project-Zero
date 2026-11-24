-- Server entry point: starts Project Zero services in dependency order.
local Services = script.Parent.Services

local PlayerDataService = require(Services.PlayerDataService)
local StasisService = require(Services.StasisService)
local AppearanceService = require(Services.AppearanceService)
local EquipmentService = require(Services.EquipmentService)
local ShopService = require(Services.ShopService)
local MissionService = require(Services.MissionService)
local WingPlatformService = require(Services.WingPlatformService)

PlayerDataService.Start()
StasisService.Start() -- creates ReplicatedStorage.PZ_Remotes
AppearanceService.Start()
EquipmentService.Start()
ShopService.Start()
MissionService.Start() -- also starts FacilityService and spawns the mission NPCs
WingPlatformService.Start() -- after FacilityService: the platform runs on facility power
