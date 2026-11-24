--!strict
-- FlightController (client): free flight for robots wearing wings (owner decision 2026-11-24).
-- Available while the character attribute PZ_CanFly is true (set by the server's EquipmentService).
--   F (gamepad Y, touch "Fly")  take off / land
--   move keys                   fly where the camera points; release to hover
--   Space / Q or C              climb / descend (touch "Up" / "Down"). Not Ctrl: in the playtest a held Ctrl
--                               kept the robot descending and turned F into Ctrl+F (Studio's Find), so F stopped landing.
-- Wing energy (0-100) drains while flying and recharges on the ground; at 0 the robot drops (wings fold).
-- Physics: a LinearVelocity drives the root and an AlignOrientation faces the flight direction; the character is
-- client-owned, as for normal walking.

local ContextActionService = game:GetService("ContextActionService")
local Players = game:GetService("Players")
local RunService = game:GetService("RunService")
local UserInputService = game:GetService("UserInputService")

local player = Players.LocalPlayer

local SPEED = 34
local CLIMB = 22
local DRAIN = 6      -- energy per second in the air (~16 s of flight)
local RECHARGE = 25  -- energy per second on the ground
local MAX_ENERGY = 100

local energy = MAX_ENERGY
local flying = false
local up, down = false, false
local lv: LinearVelocity? = nil
local ao: AlignOrientation? = nil
local att: Attachment? = nil

-- energy bar ------------------------------------------------------------------------------------------------
local gui = Instance.new("ScreenGui")
gui.Name = "PZ_Flight"; gui.ResetOnSpawn = false; gui.DisplayOrder = 9
local bar = Instance.new("Frame")
bar.AnchorPoint = Vector2.new(0.5, 1); bar.Position = UDim2.new(0.5, 0, 1, -128); bar.Size = UDim2.fromOffset(240, 26)
bar.BackgroundColor3 = Color3.fromRGB(12, 16, 22); bar.BackgroundTransparency = 0.25; bar.Visible = false; bar.Parent = gui
Instance.new("UICorner", bar).CornerRadius = UDim.new(0, 6)
local fill = Instance.new("Frame")
fill.Position = UDim2.fromOffset(4, 4); fill.Size = UDim2.new(1, -8, 1, -8); fill.BackgroundColor3 = Color3.fromHex("#22D3EE")
fill.BorderSizePixel = 0; fill.Parent = bar
Instance.new("UICorner", fill).CornerRadius = UDim.new(0, 4)
local label = Instance.new("TextLabel")
label.Size = UDim2.fromScale(1, 1); label.BackgroundTransparency = 1; label.Font = Enum.Font.GothamBold; label.TextSize = 13
label.TextColor3 = Color3.fromRGB(235, 240, 245); label.TextStrokeTransparency = 0.5; label.Text = "WING ENERGY   [F] FLY"
label.ZIndex = 2; label.Parent = bar
gui.Parent = player:WaitForChild("PlayerGui")

local function character()
	local c = player.Character
	local hum = c and c:FindFirstChildOfClass("Humanoid")
	local root = c and c:FindFirstChild("HumanoidRootPart") :: BasePart?
	return c, hum, root
end

local function canFly(): boolean
	local c = player.Character
	return c ~= nil and c:GetAttribute("PZ_CanFly") == true
end

local function stopFlying()
	flying = false
	if lv then lv:Destroy(); lv = nil end
	if ao then ao:Destroy(); ao = nil end
	if att then att:Destroy(); att = nil end
	local _, hum = character()
	if hum then
		hum.PlatformStand = false
		hum:ChangeState(Enum.HumanoidStateType.Freefall)
	end
	label.Text = "WING ENERGY   [F] FLY"
end

local function startFlying()
	local _, hum, root = character()
	if not hum or not root or hum.Health <= 0 or not canFly() or energy < 10 then return end
	flying = true
	att = Instance.new("Attachment"); att.Name = "PZ_FlightAttachment"; att.Parent = root
	lv = Instance.new("LinearVelocity")
	lv.Attachment0 = att; lv.RelativeTo = Enum.ActuatorRelativeTo.World; lv.MaxForce = math.huge
	lv.VectorVelocity = Vector3.new(0, 6, 0); lv.Parent = root
	ao = Instance.new("AlignOrientation")
	ao.Mode = Enum.OrientationAlignmentMode.OneAttachment; ao.Attachment0 = att
	ao.MaxTorque = math.huge; ao.Responsiveness = 18; ao.CFrame = root.CFrame - root.Position; ao.Parent = root
	hum.PlatformStand = true
	label.Text = "WING ENERGY   [F] LAND"
end

local function toggle(_, state)
	if state ~= Enum.UserInputState.Begin then return Enum.ContextActionResult.Pass end
	if flying then stopFlying() else startFlying() end
	return Enum.ContextActionResult.Sink
end

local function hold(name, state)
	local on = state == Enum.UserInputState.Begin
	if state == Enum.UserInputState.Begin or state == Enum.UserInputState.End or state == Enum.UserInputState.Cancel then
		if name == "PZ_FlyUp" then up = on else down = on end
	end
	-- Space must still jump when not flying
	return if flying then Enum.ContextActionResult.Sink else Enum.ContextActionResult.Pass
end

local bound = false
local function bind(on: boolean)
	if on == bound then return end
	bound = on
	if on then
		ContextActionService:BindAction("PZ_Fly", toggle, true, Enum.KeyCode.F, Enum.KeyCode.ButtonY)
		ContextActionService:SetTitle("PZ_Fly", "Fly")
		ContextActionService:BindAction("PZ_FlyUp", hold, true, Enum.KeyCode.Space, Enum.KeyCode.ButtonA)
		ContextActionService:SetTitle("PZ_FlyUp", "Up")
		ContextActionService:BindAction("PZ_FlyDown", hold, true, Enum.KeyCode.Q, Enum.KeyCode.C, Enum.KeyCode.ButtonB)
		ContextActionService:SetTitle("PZ_FlyDown", "Down")
	else
		ContextActionService:UnbindAction("PZ_Fly")
		ContextActionService:UnbindAction("PZ_FlyUp")
		ContextActionService:UnbindAction("PZ_FlyDown")
		if flying then stopFlying() end
	end
end

RunService.RenderStepped:Connect(function(dt)
	local able = canFly()
	bind(able)
	bar.Visible = able
	local _, hum, root = character()
	if not hum or not root then return end
	if flying then
		if hum.Health <= 0 or not able then stopFlying() return end
		energy = math.max(0, energy - DRAIN * dt)
		if energy <= 0 then stopFlying() end
		if lv and ao then
			local move = hum.MoveDirection
			local vertical = (if up then CLIMB else 0) - (if down then CLIMB else 0)
			local target = move * SPEED + Vector3.new(0, vertical, 0)
			lv.VectorVelocity = lv.VectorVelocity:Lerp(target, math.clamp(dt * 6, 0, 1))
			local look = if move.Magnitude > 0.1 then move else (workspace.CurrentCamera.CFrame.LookVector * Vector3.new(1, 0, 1))
			if look.Magnitude > 0.01 then
				local pitch = math.rad(-12) * math.clamp(move.Magnitude, 0, 1)
				ao.CFrame = CFrame.lookAt(Vector3.zero, look.Unit) * CFrame.Angles(pitch, 0, 0)
			end
		end
	elseif hum.FloorMaterial ~= Enum.Material.Air then
		energy = math.min(MAX_ENERGY, energy + RECHARGE * dt)
	end
	fill.Size = UDim2.new((energy / MAX_ENERGY), -8 * (energy / MAX_ENERGY), 1, -8)
	fill.BackgroundColor3 = if energy < 25 then Color3.fromRGB(255, 120, 80) else Color3.fromHex("#22D3EE")
end)

player.CharacterAdded:Connect(function()
	flying = false; lv = nil; ao = nil; att = nil; energy = MAX_ENERGY
	bound = false
	ContextActionService:UnbindAction("PZ_Fly")
	ContextActionService:UnbindAction("PZ_FlyUp")
	ContextActionService:UnbindAction("PZ_FlyDown")
end)

UserInputService.WindowFocusReleased:Connect(function() up, down = false, false end)
