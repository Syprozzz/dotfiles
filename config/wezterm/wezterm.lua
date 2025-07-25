local wezterm = require("wezterm")
local pywal = require("pywal")

wezterm.add_to_config_reload_watch_list(os.getenv("HOME") .. "/.cache/wal/colors.json")

return {
	font = wezterm.font("JetBrainsMono Nerd Font", { weight = "Bold" }),
	font_size = 13.0,

	enable_tab_bar = false,
	window_background_opacity = 0.3,
	hide_tab_bar_if_only_one_tab = false,
	warn_about_missing_glyphs = false,
	colors = pywal,
}
