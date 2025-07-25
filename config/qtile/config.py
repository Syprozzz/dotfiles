from typing import List, Callable
from libqtile import bar, widget, layout, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
import json
from pathlib import Path
import os
import sys
import subprocess

sys.modules["libqtile.log_utils"].warn_about_missing_glyphs = False

mod = "mod4"
terminal = "wezterm"

# pywal
colors_file = Path.home() / ".cache/wal/colors.json"
with open(colors_file, "r") as f:
    wal_colors = json.load(f)["colors"]

background = wal_colors["color0"]
foreground = wal_colors["color7"]
accent = wal_colors["color4"]

keys = [
    # Window focus
    Key([mod], "h", lazy.layout.left(), desc="Move focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Focus next window"),
    # Move windows
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Resize windows
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Normalize sizes"),
    # Layout management
    Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle split"),
    Key([mod], "Tab", lazy.next_layout(), desc="Next layout"),
    # App launching
    Key([mod], "Return", lazy.spawn(terminal)),
    Key(
        [mod],
        "r",
        lazy.spawn("/home/concerned_penguin/.config/rofi/launchers/type-5/launcher.sh"),
        desc="Launch rofi custom launcher",
    ),
    Key([mod], "s", lazy.spawn("flameshot gui"), desc="Screenshot (flameshot)"),
    Key([mod], "b", lazy.spawn("brave"), desc="browser (brave)"),
    # System controls
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Toggle fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating"),
    # Volume keys
    Key([], "XF86AudioLowerVolume", lazy.spawn("pamixer -d 5")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("pamixer -i 5")),
    Key([], "XF86AudioMute", lazy.spawn("pamixer -t")),
    # brightness keys
    Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),
    Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set 5%+")),
    # sleep mode
    Key(["mod4", "shift"], "s", lazy.spawn("systemctl suspend")),
    # changing wallpapers
    Key([mod], "o", lazy.spawn("/home/concerned_penguin/scripts/wal-wall.sh")),
    # optimus manager
    Key([mod, "shift"], "o", lazy.spawn("optimus-manager-qt")),
]

# Groups
# groups = [Group(i) for i in "123456789"] #if u want numbers
groups = [Group(f"{i + 1}", label="") for i in range(9)]

for i in groups:
    keys.extend(
        [
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc=f"Switch to group {i.name}",
            ),
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc=f"Move focused window to group {i.name}",
            ),
        ]
    )

# Layouts
layouts = [
    layout.Columns(
        border_focus=wal_colors["color3"],
        border_normal=wal_colors["color3"],
        border_width=2,
        margin=6,
    ),
    layout.Max(),
]

# Widget defaults
widget_defaults = dict(
    font="Font Awesome 6 Free Solid",
    fontsize=12,
    padding=2,
    foreground=foreground,
    background=background,
)
extension_defaults = widget_defaults.copy()


power = lazy.spawn("/home/concerned_penguin/.config/rofi/powermenu/type-2/powermenu.sh")
search = lazy.spawn("/home/concerned_penguin/.config/rofi/launchers/type-5/launcher.sh")
# Screen/bar


screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(
                    length=20,
                    background=background,
                ),
                widget.TextBox(
                    text="",
                    # font="JetBrainsMono Nerd Font",
                    fontsize=29,
                    background=background,
                    foreground=foreground,
                    mouse_callbacks={"Button1": search},
                ),
                widget.Spacer(
                    length=20,
                    background=background,
                ),
                widget.GroupBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=28,
                    borderwidth=3,
                    highlight_method="block",
                    active=accent,
                    block_highlight_text_color=wal_colors["color2"],
                    highlight_color=wal_colors["color3"],
                    inactive=foreground,
                    foreground=wal_colors["color4"],
                    background=background,
                    this_current_screen_border=wal_colors["color3"],
                    this_screen_border=wal_colors["color3"],
                    other_current_screen_border=wal_colors["color3"],
                    other_screen_border=wal_colors["color3"],
                    urgent_border=wal_colors["color3"],
                    rounded=True,
                    disable_drag=True,
                ),
                widget.Spacer(
                    length=15,
                    background=background,
                ),
                widget.WindowName(
                    background=background,
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    empty_group_string="Desktop",
                    max_chars=26,
                    foreground=foreground,
                ),
                widget.Spacer(
                    length=15,
                    background=background,
                ),
                widget.GenPollText(
                    update_interval=1,
                    func=lambda: subprocess.run(
                        [
                            "playerctl",
                            "--player=spotify",
                            "metadata",
                            "--format",
                            "{{ artist }} - {{ title }}",
                        ],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.DEVNULL,
                    )
                    .stdout.decode("utf-8")
                    .strip(),
                    fmt=" {}",
                    fontsize=14,
                    # font="JetBrainsMono Nerd Font",
                    background=background,
                    foreground=foreground,
                ),
                widget.Spacer(
                    length=bar.STRETCH,
                    background=background,
                ),
                widget.TextBox(
                    text="",
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    background=background,
                    foreground=foreground,
                ),
                widget.Memory(
                    background=background,
                    format="{MemUsed: .0f}{mm}",
                    foreground=foreground,
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    update_interval=5,
                ),
                widget.Spacer(
                    length=15,
                    background=background,
                ),
                widget.TextBox(
                    text=" ",
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    background=background,
                    foreground=foreground,
                ),
                widget.Battery(
                    fontsize=12,
                    # font="Font Awesome 6 Free Solid",
                    foreground=foreground,
                    background=background,
                    format="{percent:2.0%}",
                ),
                widget.Spacer(
                    length=15,
                    background=background,
                ),
                widget.TextBox(
                    text=" ",
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    background=background,
                    foreground=foreground,
                ),
                widget.Volume(
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    background=background,
                    foreground=foreground,
                    mute_command="pamixer --toggle-mute",
                    volume_up_command="pamixer -i 5",
                    volume_down_command="pamixer -d 5",
                    get_volume_command="pamixer --get-volume-human",
                    update_interval=0.2,
                    unmute_format="{volume}%",
                    mute_format="M",
                ),
                widget.Spacer(length=15, background=background),
                widget.TextBox(
                    text=" ",
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                    background=background,
                    foreground=foreground,
                ),
                widget.Clock(
                    format="%I:%M %p",
                    background=background,
                    foreground=foreground,
                    # font="Font Awesome 6 Free Solid",
                    fontsize=12,
                ),
                widget.Spacer(
                    length=18,
                    background=background,
                ),
                widget.TextBox(
                    text="⏻",
                    # font="Font Awesome 6 Free Solid",
                    fontsize=21,
                    margin=5,
                    background=background,
                    foreground=foreground,
                    mouse_callbacks={"Button1": power},
                ),
                widget.Spacer(
                    length=18,
                    background=background,
                ),
            ],
            38,
            name="qtilebar",
            border_color=wal_colors["color3"],
            border_width=[0, 0, 0, 0],
            margin=[15, 60, 6, 60],
        ),
    ),
]


# Mouse
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]


# Autostart
@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser("~")
    autostart_script = os.path.join(home, ".config", "qtile", "autostart.sh")
    os.system(autostart_script)
    # subprocess.Popen(["nm-applet"]) #wifi icon
    # subprocess.Popen(["blueman-applet"])
    # subprocess.Popen(["pasystray"])
    subprocess.Popen(["dunst"])
    # subprocess.Popen(["flameshot"])
    subprocess.Popen(["xsetroot", "-cursor_name", "left_ptr"])


# Floating rules
floating_layout = layout.Floating(
    border_focus="#88C0D0",
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),
        Match(wm_class="makebranch"),
        Match(wm_class="ssh-askpass"),
        Match(title="branchdialog"),
        Match(title="pinentry"),
    ],
)

# Misc settings
dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floats_kept_above = True
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True

# Java fix
wmname = "LG3D"
