-- Server entry point: starts Project Zero services in dependency order.
local Services = script.Parent.Services

local PlayerDataService = require(Services.PlayerDataService)
local StasisService = require(Services.StasisService)
local MissionService = require(Services.MissionService)

PlayerDataService.Start()
StasisService.Start()
MissionService.Start() -- also starts FacilityService and spawns the mission NPCs
