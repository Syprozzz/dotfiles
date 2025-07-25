local success, wal_colors = pcall(function()
	local json = require("json")
	local file = io.open(os.getenv("HOME") .. "/.cache/wal/colors.json", "r")
	if not file then
		return nil
	end
	local content = file:read("*a")
	file:close()
	return json.decode(content)
end)

if not success or not wal_colors or not wal_colors.colors then
	return {}
end

return {
	foreground = wal_colors.special.foreground,
	background = wal_colors.special.background,
	cursor_bg = wal_colors.special.cursor,
	cursor_fg = wal_colors.special.background,
	cursor_border = wal_colors.special.cursor,
	selection_fg = wal_colors.special.background,
	selection_bg = wal_colors.colors.color2,
	ansi = {
		wal_colors.colors.color0,
		wal_colors.colors.color1,
		wal_colors.colors.color2,
		wal_colors.colors.color3,
		wal_colors.colors.color4,
		wal_colors.colors.color5,
		wal_colors.colors.color6,
		wal_colors.colors.color7,
	},
	brights = {
		wal_colors.colors.color8,
		wal_colors.colors.color9,
		wal_colors.colors.color10,
		wal_colors.colors.color11,
		wal_colors.colors.color12,
		wal_colors.colors.color13,
		wal_colors.colors.color14,
		wal_colors.colors.color15,
	},
}
