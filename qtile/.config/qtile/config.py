# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from libqtile import bar, layout, widget, qtile
from libqtile.config import Click, Drag, Group, Key, Match, Screen, ScratchPad, DropDown
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
import os
import subprocess
from libqtile import hook
from qtile_extras import widget
from qtile_extras.widget.decorations import PowerLineDecoration
from colors import dracula, nord


@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])
    
    
mod = "mod4"
terminal = 'alacritty'

def show_neofetch(qtile):
    command = ["alacritty", "--title", "Scratchpad", "--hold", "-e", "neofetch"]
    qtile.cmd_spawn(command)

keys = [
    # A list of available commands that can be bound to keys can be found
    # at https://docs.qtile.org/en/latest/manual/config/lazy.html
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "a", lazy.window.toggle_floating()),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "left", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "right", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "down", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "up", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "w", lazy.window.kill(), desc="Kill focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
    Key([mod], "d", lazy.spawn('rofi -show drun'), desc="menu rofi"),
    Key([], "Print", lazy.spawn('flameshot gui'), desc="flameshot screenshot"),
    # Key([], "F12", lazy.function(show_neofetch))
]
keys.append(Key([mod], "e", lazy.spawn("nemo")))

# groups = [Group(i) for i in "123456"]
groups = [Group(f"{i+1}") for i in range(8)]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )
    
# Define scratchpads
groups.append(ScratchPad("scratchpad", [
    DropDown("term", "alacritty --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    DropDown("obsidian", "obsidian --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    # DropDown("term2", "kitty --class=scratch", width=0.8, height=0.8, x=0.1, y=0.1, opacity=1),
    # DropDown("ranger", "kitty --class=ranger -e ranger", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    # DropDown("volume", "kitty --class=volume -e pulsemixer", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    # DropDown("mus", "kitty --class=mus -e ncmpcpp", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),
    # DropDown("news", "kitty --class=news -e newsboat", width=0.8, height=0.8, x=0.1, y=0.1, opacity=0.9),

]))

keys.extend([
    Key([mod], "m", lazy.group['scratchpad'].dropdown_toggle('term')),
    Key([mod], "n", lazy.group['scratchpad'].dropdown_toggle('obsidian')),
    # Key([mod], "c", lazy.group['scratchpad'].dropdown_toggle('ranger')),
    # Key([mod], "v", lazy.group['scratchpad'].dropdown_toggle('volume')),
    # Key([mod], "m", lazy.group['scratchpad'].dropdown_toggle('mus')),
    # Key([mod], "b", lazy.group['scratchpad'].dropdown_toggle('news')),
    # Key([mod, "shift"], "n", lazy.group['scratchpad'].dropdown_toggle('term2')),
])

layouts = [
    layout.Columns( margin= [10,10,10,10], border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
        border_width=0,
        focus_on_window_activation=False
    ),

    layout.Max(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=10,
	    border_width=0,
    ),

    layout.Floating(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=10,
	    border_width=0,
	),
    # Try more layouts by unleashing below layouts
   #  layout.Stack(num_stacks=2),
   #  layout.Bsp(),
     layout.Matrix(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=10,
	    border_width=0,
	),
     layout.MonadTall(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
        margin=10,
	    border_width=0,
	),
    layout.MonadWide(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
	    margin=10,
	    border_width=0,
	),
   #  layout.RatioTile(),
     layout.Tile(	border_focus='#1F1D2E',
	    border_normal='#1F1D2E',
    ),
   #  layout.TreeTab(),
   #  layout.VerticalTile(),
   #  layout.Zoomy(),
]

def search():
    qtile.cmd_spawn("rofi -show drun -show-icons")
    
    
def power():
    qtile.cmd_spawn("sh -c ~/.config/rofi/scripts/power")
    

colors = nord

    
widget_defaults = dict(
    font="sans",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

widget_list = []


screens = [
    Screen(
        top=bar.Bar(
            [
				widget.Spacer(length=20,
                    background=colors[0],
                ),
    
                widget.TextBox(
                    background=colors[0],
                    foreground=colors[2],
                    text="󰣇 ",
                    fontsize=28,
                    mouse_callbacks={"Button1":power},
                ),
                
				widget.Spacer(length=10,
                    background=colors[0],
                    decorations=[
                        PowerLineDecoration(
                            path='arrow_left',
                            background=colors[2]
                        )
                    ]
                ),
    
                widget.GroupBox(
                    fontsize=24,
                    borderwidth=3,
                    highlight_method='block',
                    active=colors[4],
                    block_highlight_text_color=colors[5],
                    highlight_color=colors[6],
                    inactive=colors[7],
                    foreground=colors[2],
                    background=colors[9],
                    this_current_screen_border=colors[10],
                    this_screen_border=colors[11],
                    other_current_screen_border=colors[12],
                    other_screen_border=colors[13],
                    urgent_border=colors[14],
                    rounded=True,
                    disable_drag=True,
                    decorations=[
                        PowerLineDecoration(
                            path='rounded_left',
                            # path='arrow_left',
                            background="#282738"
                        )]
                 ),
                
                 widget.TextBox(
                    fmt=' 󱂬',
                    background=colors[0],
                    font="JetBrains Mono Bold",
                    fontsize=20,
                    foreground=colors[2],
                    decorations=[
                        PowerLineDecoration(
                            path='rounded_left',
                            background=colors[15]
                        )]
                ),

                widget.CurrentLayout(
                    background=colors[0],
                    fmt='{}',
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    decorations=[
                        PowerLineDecoration(
                            path='forward_slash',
                            background=colors[15]
                        )]
                ),

                widget.TextBox(
                    fmt='󰍉',
                    background=colors[15],
                    font="JetBrains Mono Bold",
                    fontsize=20,
                    foreground=colors[2],
                    mouse_callbacks={"Button1": search},
                    decorations=[
                        PowerLineDecoration(
                            path='rounded_left',
                            background=colors[15]
                        )]
                ),
                widget.TextBox(
                    fmt='Search',
                    background=colors[15],
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    foreground=colors[2],
                    mouse_callbacks={"Button1": search},
                    decorations=[
                        PowerLineDecoration(
                            path='rounded_right',
                            background=colors[15]
                        )]
                ),
                 widget.Spacer(length=10,
                    background=colors[15],
                    decorations=[
                        PowerLineDecoration(
                            path='forward_slash',
                            background=colors[15]
                        )
                    ]
                ),

                widget.WindowName(
                    background = colors[16],
                    format = "{name}",
                    font='JetBrains Mono Bold',
                    foreground=colors[2],
                    empty_group_string = 'Desktop',
                    fontsize=13,
                ),
                widget.Spacer(length=10,
                    background=colors[16],
                    decorations=[
                        PowerLineDecoration(
                            path='arrow_right',
                            background=colors[0]
                        )
                    ]
                ),

                widget.Mpris2(
                    name='spotify',
                    objname="org.mpris.MediaPlayer2.spotify",
                    display_metadata=['xesam:title', 'xesam:artist'],
                    scroll_chars=None,
                    stop_pause_text='',
                    background=colors[0],
                    interval=0.1,
                    **widget_defaults,
                    decorations=[
                        PowerLineDecoration(
                            path='arrow_right',
                            background=colors[15]
                    )]
                ),
            
                widget.Systray(
                    background=colors[0],
                    fontsize=2,
                    decorations=[
                            PowerLineDecoration(
                                path='arrow_right',
                                background=colors[16]
                        )]
                ),

                widget.Net(
                format=' {up}   {down} ',
                background=colors[16],
                foreground=colors[2],
                font="JetBrains Mono Bold",
                prefix='k',
                decorations=[
                            PowerLineDecoration(
                                path='forward_slash',
                                background=colors[16]
                        )]
                ),
                 
                widget.TextBox(
                    background=colors[0],
                    foreground=colors[2],
                    text="󰘚",
                    fontsize=20,
                    decorations=[
                            PowerLineDecoration(
                                path='back_slash',
                                background=colors[0]
                        )]
                ),

                widget.Memory(
                    background=colors[0],
                    format='Mem: {MemPercent}%',
                    measure_mem='G',
                    foreground=colors[2],
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    update_interval=5,
                    
                ),
                
                widget.TextBox(
                    background=colors[0],
                    foreground=colors[2],
                    text="󰍛",
                    fontsize=20,
                    decorations=[
                            PowerLineDecoration(
                                path='back_slash',
                                background=colors[16]
                        )]
                ),
                
                widget.CPU(
                    format='CPU: {load_percent}%',
                    foreground=colors[2],
                    background=colors[0],
                    font="JetBrains Mono Bold",
                    fontsize=13,
                    update_interval=5,
                    decorations=[
                            PowerLineDecoration(
                                path='forward_slash',
                                background=colors[0]
                        )]
                    ),

                widget.BatteryIcon(
                    theme_path='~/.config/qtile/Assets/Battery/',
                    background=colors[16],
                    scale=1,
                    
                ),

                widget.Battery(
                    font='JetBrains Mono Bold',
                    background=colors[16],
                    foreground=colors[2],
                    format='{percent:2.0%}',
                    fontsize=13,
                ),
                
                widget.Spacer(
                    length=8,
                    background=colors[9],
                ),
                widget.Volume(
                    font='JetBrainsMono Nerd Font',
                    theme_path='~/.config/qtile/Assets/Volume/',
                    emoji=True,
                    fontsize=13,
                    background=colors[9],
                ),

                widget.Spacer(
                    length=-5,
                    background=colors[9],
                    ),

                widget.Volume(
                    font='JetBrains Mono Bold',
                    background=colors[9],
                    foreground=colors[2],
                    fontsize=13,
                    decorations=[
                            PowerLineDecoration(
                                path='forward_slash',
                                background=colors[0]
                        )]
                ),

                widget.Image(
                    filename='~/.config/qtile/Assets/Misc/clock.png',
                    background=colors[0],
                    margin_y=6,
                    margin_x=5,
                ),
                widget.Clock(
                    format='%a %d-%m-%Y  %I:%M %p',
                    background=colors[0],
                    foreground=colors[2],
                    font="JetBrains Mono Bold",
                    fontsize=13,
                ),

                widget.Spacer(
                    length=18,
                    background=colors[0],
                ),
            ],
            30,
            border_width = [0,0,0,0],
            margin = [5,20,5,20],
        ),
    )
]


# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"


    
    