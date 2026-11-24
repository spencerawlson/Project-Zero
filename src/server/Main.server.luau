-- Server entry point: starts Project Zero services in dependency order.
local Services = script.Parent.Services

local PlayerDataService = require(Services.PlayerDataService)
local StasisService = require(Services.StasisService)

PlayerDataService.Start()
StasisService.Start()
