-- Server entry point: starts Project Zero services in dependency order.
local Services = script.Parent.Services

local PlayerDataService = require(Services.PlayerDataService)

PlayerDataService.Start()
