--!strict
-- ShopUI (client): NEXUS Credits balance (right edge, above PAINT) and the vendor window.
-- Reads the player attribute PZ_Credits; talks to ShopService on PZ_Remotes.Shop:
--   server -> client ("open" | "state", state), ("result", { ok, reason, itemId, action })
--   client -> server ("buy", id) | ("equip", id) | ("unequip", slot)
-- The server decides everything; this only shows state and sends requests.

local Players = game:GetService("Players")
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local UserInputService = game:GetService("UserInputService")

local player = Players.LocalPlayer
local remote = ReplicatedStorage:WaitForChild("PZ_Remotes"):WaitForChild("Shop") :: RemoteEvent

local PANEL = Color3.fromRGB(12, 16, 22)
local CYAN = Color3.fromRGB(0, 230, 220)
local WHITE = Color3.fromRGB(235, 240, 245)
local MUTED = Color3.fromRGB(170, 180, 190)

local function make(className: string, props: { [string]: any }, parent: Instance?): any
	local inst = Instance.new(className)
	for k, v in pairs(props) do (inst :: any)[k] = v end
	if parent then inst.Parent = parent end
	return inst
end

local gui = make("ScreenGui", { Name = "PZ_Shop", ResetOnSpawn = false, DisplayOrder = 12 }, player:WaitForChild("PlayerGui"))

-- balance -----------------------------------------------------------------------------------------------------
local balance = make("TextLabel", { Name = "Credits", AnchorPoint = Vector2.new(1, 0), Position = UDim2.new(1, -16, 0.4, -42),
	Size = UDim2.fromOffset(150, 32), BackgroundColor3 = PANEL, BackgroundTransparency = 0.2, Font = Enum.Font.GothamBold,
	TextSize = 15, TextColor3 = CYAN, Text = "" }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, balance)
local function showBalance()
	balance.Text = "CREDITS  " .. tostring(player:GetAttribute("PZ_Credits") or 0)
end
player:GetAttributeChangedSignal("PZ_Credits"):Connect(showBalance)
showBalance()

-- vendor window -----------------------------------------------------------------------------------------------
local win = make("Frame", { Name = "Vendor", AnchorPoint = Vector2.new(0.5, 0.5), Position = UDim2.fromScale(0.5, 0.5),
	Size = UDim2.fromOffset(440, 0), AutomaticSize = Enum.AutomaticSize.Y, BackgroundColor3 = PANEL, BackgroundTransparency = 0.05,
	Visible = false }, gui)
make("UICorner", { CornerRadius = UDim.new(0, 8) }, win)
make("UIStroke", { Color = CYAN, Transparency = 0.5 }, win)
make("UIPadding", { PaddingTop = UDim.new(0, 14), PaddingBottom = UDim.new(0, 14), PaddingLeft = UDim.new(0, 16), PaddingRight = UDim.new(0, 16) }, win)
make("UIListLayout", { Padding = UDim.new(0, 10), SortOrder = Enum.SortOrder.LayoutOrder }, win)
make("TextLabel", { LayoutOrder = 1, Size = UDim2.new(1, 0, 0, 24), BackgroundTransparency = 1, Font = Enum.Font.GothamBold,
	TextSize = 20, TextColor3 = WHITE, TextXAlignment = Enum.TextXAlignment.Left, Text = "NEXUS VENDOR" }, win)
local list = make("Frame", { LayoutOrder = 2, Size = UDim2.new(1, 0, 0, 0), AutomaticSize = Enum.AutomaticSize.Y, BackgroundTransparency = 1 }, win)
make("UIListLayout", { Padding = UDim.new(0, 8), SortOrder = Enum.SortOrder.LayoutOrder }, list)
local message = make("TextLabel", { LayoutOrder = 3, Size = UDim2.new(1, 0, 0, 20), BackgroundTransparency = 1, Font = Enum.Font.Gotham,
	TextSize = 14, TextColor3 = MUTED, TextXAlignment = Enum.TextXAlignment.Left, Text = "" }, win)
local close = make("TextButton", { LayoutOrder = 4, Size = UDim2.new(1, 0, 0, 34), BackgroundColor3 = Color3.fromRGB(30, 36, 44),
	Font = Enum.Font.GothamBold, TextSize = 15, TextColor3 = WHITE, Text = "Close" }, win)
make("UICorner", { CornerRadius = UDim.new(0, 6) }, close)
close.MouseButton1Click:Connect(function() win.Visible = false end)
UserInputService.InputBegan:Connect(function(input, processed)
	if not processed and input.KeyCode == Enum.KeyCode.Escape then win.Visible = false end
end)

local REASONS = { credits = "Not enough NEXUS Credits.", owned = "You already own this.", not_owned = "Buy it first.",
	unknown = "Unknown item.", too_far = "Step up to the vendor to buy.",
	not_for_sale = "Not sold here." }

local function render(state: any)
	for _, c in ipairs(list:GetChildren()) do
		if c:IsA("Frame") then c:Destroy() end
	end
	if not state then return end
	local order = 0
	for id, item in pairs(state.catalog) do
		order += 1
		local row = make("Frame", { Name = id, LayoutOrder = order, Size = UDim2.new(1, 0, 0, 86), BackgroundColor3 = Color3.fromRGB(22, 28, 36) }, list)
		make("UICorner", { CornerRadius = UDim.new(0, 6) }, row)
		make("TextLabel", { Position = UDim2.fromOffset(12, 8), Size = UDim2.new(1, -150, 0, 22), BackgroundTransparency = 1,
			Font = Enum.Font.GothamBold, TextSize = 17, TextColor3 = WHITE, TextXAlignment = Enum.TextXAlignment.Left, Text = item.name }, row)
		make("TextLabel", { Position = UDim2.fromOffset(12, 32), Size = UDim2.new(1, -150, 0, 46), BackgroundTransparency = 1,
			Font = Enum.Font.Gotham, TextSize = 13, TextColor3 = MUTED, TextWrapped = true, TextXAlignment = Enum.TextXAlignment.Left,
			TextYAlignment = Enum.TextYAlignment.Top, Text = item.description }, row)
		local owned = state.items[id] == true
		local equipped = state.equipped[item.slot] == id
		local text, action, enabled
		if not owned then
			local short = item.price - state.credits
			text = if short > 0 then ("%d CR  (need %d)"):format(item.price, short) else ("BUY  %d CR"):format(item.price)
			action, enabled = "buy", short <= 0
		elseif equipped then
			text, action, enabled = "UNEQUIP", "unequip", true
		else
			text, action, enabled = "EQUIP", "equip", true
		end
		local btn = make("TextButton", { Name = "Action", AnchorPoint = Vector2.new(1, 0.5), Position = UDim2.new(1, -10, 0.5, 0),
			Size = UDim2.fromOffset(126, 38), BackgroundColor3 = if enabled then Color3.fromRGB(0, 150, 145) else Color3.fromRGB(50, 56, 64),
			Font = Enum.Font.GothamBold, TextSize = 13, TextColor3 = WHITE, Text = text, AutoButtonColor = enabled }, row)
		make("UICorner", { CornerRadius = UDim.new(0, 6) }, btn)
		btn.MouseButton1Click:Connect(function()
			if not enabled then return end
			message.Text = "..."
			remote:FireServer(action, if action == "unequip" then item.slot else id)
		end)
	end
end

remote.OnClientEvent:Connect(function(kind, data)
	if kind == "open" then
		message.Text = ""
		render(data)
		win.Visible = true
	elseif kind == "state" then
		if win.Visible then render(data) end
	elseif kind == "result" and type(data) == "table" then
		if data.ok then
			message.Text = if data.action == "buy" then "Purchased and equipped."
				elseif data.action == "equip" then "Equipped." else "Unequipped."
		else
			message.Text = REASONS[data.reason] or "Request refused."
		end
	end
end)
