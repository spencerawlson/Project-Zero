--!strict
-- WingVisuals (client): unfolds and folds the wings of every robot on this screen (owner feedback 2026-11-24:
-- wings are only there while flying). EquipmentService welds the back module and the wings to the robot,
-- stowed (invisible), and sets the character attribute PZ_WingsOut while it flies. Here, per robot:
--   deploy: the back module fades in, then each wing grows out of its hinge and swings open (UNFOLD seconds)
--   stow:   the reverse; at 0 everything is invisible again
-- Only local properties change (Weld.C0, Size, Transparency of the welded parts), so every client animates
-- smoothly and the server's values (the fully open pose, in PZ_FullC0 / PZ_FullSize) stay untouched.

local RunService = game:GetService("RunService")

local UNFOLD = 0.55          -- seconds for a full unfold
local FOLD_ANGLE = math.rad(80) -- stowed wings are swung back this far along the robot's back
local MIN_SCALE = 0.12       -- stowed wing size

type Piece = { part: BasePart, weld: Weld, role: string, side: number, fullC0: CFrame, fullSize: Vector3, base: number }
type Rig = { model: Model, back: Model, hinge: CFrame, pieces: { Piece }, t: number, applied: number }
local rigs: { [Model]: Rig } = {}

local function ease(x: number): number
	return 1 - (1 - x) ^ 3
end

local function collect(model: Model, back: Model): Rig?
	local hinge = back:GetAttribute("PZ_Hinge")
	if typeof(hinge) ~= "CFrame" then return nil end
	local pieces = {}
	for _, d in ipairs(back:GetDescendants()) do
		if d:IsA("BasePart") then
			local weld = d:FindFirstChild("PZ_Weld") :: Weld?
			local fullC0, fullSize = d:GetAttribute("PZ_FullC0"), d:GetAttribute("PZ_FullSize")
			if weld and typeof(fullC0) == "CFrame" and typeof(fullSize) == "Vector3" then
				table.insert(pieces, {
					part = d, weld = weld, role = d:GetAttribute("PZ_Role") or "wing", side = d:GetAttribute("PZ_Side") or 1,
					fullC0 = fullC0, fullSize = fullSize, base = d:GetAttribute("PZ_BaseTransparency") or 0,
				})
			else
				return nil -- not fully replicated yet
			end
		end
	end
	if #pieces == 0 then return nil end
	return { model = model, back = back, hinge = hinge :: CFrame, pieces = pieces, t = 0, applied = -1 }
end

local function apply(rig: Rig)
	local t = rig.t
	local core = math.clamp(t / 0.3, 0, 1)                -- module first
	local w = ease(math.clamp((t - 0.15) / 0.85, 0, 1))  -- then the wings
	for _, p in ipairs(rig.pieces) do
		if p.role == "core" then
			p.part.Transparency = if core <= 0 then 1 else p.base + (1 - p.base) * (1 - core)
		else
			if w <= 0 then
				p.part.Transparency = 1
			else
				p.part.Transparency = p.base
				local k = MIN_SCALE + (1 - MIN_SCALE) * w
				local rel = rig.hinge:Inverse() * p.fullC0
				rel = rel - rel.Position + rel.Position * k
				p.weld.C0 = rig.hinge * CFrame.Angles(0, -p.side * FOLD_ANGLE * (1 - w), 0) * rel
				p.part.Size = p.fullSize * k
			end
		end
	end
	rig.applied = t
end

RunService.RenderStepped:Connect(function(dt)
	for model, rig in pairs(rigs) do
		if not model.Parent or not rig.back.Parent then
			rigs[model] = nil
		else
			local target = if model:GetAttribute("PZ_WingsOut") == true then 1 else 0
			if rig.t ~= target then
				local stepAmount = dt / UNFOLD
				rig.t = if target > rig.t then math.min(target, rig.t + stepAmount) else math.max(target, rig.t - stepAmount)
			end
			if rig.applied ~= rig.t then apply(rig) end
		end
	end
end)

-- find robots wearing a back item (players and NPCs); re-collect when the item is replaced
local function watch(model: Instance)
	if not model:IsA("Model") then return end
	local function check()
		local back = model:FindFirstChild("PZ_Back")
		if back and back:IsA("Model") then
			local current = rigs[model]
			if not current or current.back ~= back then
				-- wait for the replicated welds and attributes
				task.defer(function()
					for _ = 1, 30 do
						local rig = collect(model, back)
						if rig then
							rig.t = if model:GetAttribute("PZ_WingsOut") == true then 1 else 0
							rigs[model] = rig
							apply(rig)
							return
						end
						task.wait(0.1)
					end
				end)
			end
		else
			rigs[model] = nil
		end
	end
	model.ChildAdded:Connect(function(c) if c.Name == "PZ_Back" then check() end end)
	model.ChildRemoved:Connect(function(c) if c.Name == "PZ_Back" then check() end end)
	check()
end

workspace.ChildAdded:Connect(watch)
for _, m in ipairs(workspace:GetChildren()) do watch(m) end
