--!strict
-- VehicleClient (client): drives the vehicle this player is driving (VehicleService). While the local robot sits in
-- a vehicle's PZ_DriverSeat, this client owns the vehicle's physics (the server sets network ownership) and steers it:
--   W / S (or the seat's throttle: arrows, gamepad, mobile thumbstick)  forward / reverse, smooth acceleration
--   A / D (the seat's steer)                                             turn; steering reverses when backing up
--   Space                                                                get out (Roblox default)
-- Only the vehicle's DriveVelocity (horizontal) and DriveTurn (yaw) constraints are changed; gravity stays free, so
-- the vehicle keeps to the ground and walls stop it.

local Players = game:GetService("Players")
local RunService = game:GetService("RunService")

local player = Players.LocalPlayer

-- the server checks driving against the same numbers (MovementGuard)
local V = require(game:GetService("ReplicatedStorage"):WaitForChild("Shared"):WaitForChild("MovementRules")).Vehicle
local MAX_FORWARD = V.MAX_FORWARD -- studs/s
local MAX_REVERSE = V.MAX_REVERSE
local ACCEL = V.ACCEL             -- studs/s²
local BRAKE = V.BRAKE
local TURN_RATE = V.TURN_RATE     -- rad/s at speed
local speed = 0

RunService.Heartbeat:Connect(function(dt)
	local c = player.Character
	local hum = c and c:FindFirstChildOfClass("Humanoid")
	local seat = hum and hum.SeatPart
	if not (seat and seat:IsA("VehicleSeat") and seat.Name == "PZ_DriverSeat") then
		speed = 0
		return
	end
	-- the vehicle is the ancestor that holds DriveBody (CrewLayer is itself a Model, so not the nearest one)
	local vehicle: Instance? = seat.Parent
	while vehicle and not vehicle:FindFirstChild("DriveBody") do vehicle = vehicle.Parent end
	local body = vehicle and vehicle:FindFirstChild("DriveBody") :: BasePart?
	local lv = body and body:FindFirstChild("DriveVelocity") :: LinearVelocity?
	local av = body and body:FindFirstChild("DriveTurn") :: AngularVelocity?
	if not (body and lv and av) then return end
	local throttle, steer = seat.ThrottleFloat, seat.SteerFloat
	local target = if throttle > 0 then throttle * MAX_FORWARD elseif throttle < 0 then throttle * MAX_REVERSE else 0
	local rate = if (target == 0) or (math.sign(target) ~= math.sign(speed) and speed ~= 0) then BRAKE else ACCEL
	if speed < target then speed = math.min(target, speed + rate * dt) else speed = math.max(target, speed - rate * dt) end
	local forward = body.CFrame.LookVector * Vector3.new(1, 0, 1)
	if forward.Magnitude > 0.01 then forward = forward.Unit end
	lv.VectorVelocity = forward * speed
	-- turning needs motion; full rate from a quarter of top speed; reversed when backing up
	local grip = math.clamp(math.abs(speed) / (MAX_FORWARD * 0.25), 0, 1)
	av.AngularVelocity = Vector3.new(0, -steer * TURN_RATE * grip * (if speed < 0 then -1 else 1), 0)
end)
