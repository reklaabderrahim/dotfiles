# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, qtile
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
alt = "mod1"
myTerm = "alacritty"      # My terminal of choice
myBrowser = "qutebrowser" # My terminal of choice

keys = [
        ### The essentials
         Key([mod], "Return",
             lazy.spawn(myTerm),
             desc="Launch terminal"
             ),
         Key([mod], "KP_Enter",
             lazy.spawn('alacritty'),
             desc="Launch terminal"
             ),
         Key([alt], "Return",
             lazy.spawn("pamac-manager"),
             desc="Pamac Manager"
             ),
         Key([mod, "shift"], "Return",
             lazy.spawn("thunar"),
             desc="Launch Thunar"
             ),
         Key([mod, "control"], "Return",
             lazy.spawn("geany"),
             desc="Launch Geany"
             ),
        Key([mod, "shift"], "d",
             lazy.spawn("dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'DejaVuSansMono:bold:pixelsize=14'"),
             desc='Run dmenu'
             ),
        Key([mod], "d",
             lazy.spawn("rofi -modi drun -show drun -config ~/.config/rofi/rofidmenu.rasi"),
             desc='Run rofi'
             ),
        Key([mod, "control"], "d",
            lazy.spawn('nwggrid -p -o 0.4'),
            desc="Run nwggrid"
            ),
        Key([mod], "t",
             lazy.spawn("rofi -show window -config ~/.config/rofi/rofidmenu.rasi"),
             desc='Show running applications'
             ),
         Key([mod], "w",
             lazy.spawn("brave"),
             desc='Google Chrome'
             ),
         Key([mod, "shift"], "w",
             lazy.spawn("firefox"),
             desc='Firefox'
             ),
         Key([mod, "control"], "w",
             lazy.spawn(myBrowser),
             desc='Qutebrowser'
             ),
         Key([mod], "space",
             lazy.next_layout(),
             desc='Toggle through layouts'
             ),
        Key([mod], "q",
             lazy.window.kill(),
             desc='Kill active window'
             ),
         Key([mod, "shift"], "r",
             lazy.restart(),
             desc='Restart Qtile'
             ),
        Key([mod, "control"], "r",
            lazy.reload_config(),
            desc="Reload the config"
            ),
        Key([mod], "r",
            lazy.spawncmd(),
            desc="Spawn a command using a prompt widget"
            ),
         Key([mod, "shift"], "q",
             lazy.shutdown(),
             desc='Shutdown Qtile'
             ),
         Key([mod, "shift"], "e",
             lazy.spawn("/home/rekla/.config/i3/scripts/powermenu"),
             desc='Exit Menu'
             ),
         Key([mod, "control"], "l",
             lazy.spawn("i3exit lock"),
             desc='i3exit lock'
             ),

         ### Switch focus to specific monitor (out of two)
         Key([mod], "i",
             lazy.to_screen(0),
             desc='Keyboard focus to monitor 1'
             ),
         Key([mod], "o",
             lazy.to_screen(1),
             desc='Keyboard focus to monitor 2'
             ),
         ### Switch focus of monitors
         Key([mod], "period",
             lazy.next_screen(),
             desc='Move focus to next monitor'
             ),
         Key([mod], "comma",
             lazy.prev_screen(),
             desc='Move focus to prev monitor'
             ),
         ### Treetab controls
          Key([mod], "h",
             lazy.layout.move_left(),
             desc='Move up a section in treetab'
             ),
         Key([mod], "l",
             lazy.layout.move_right(),
             desc='Move down a section in treetab'
             ),
         ### Window controls
         Key([mod], "j",
             lazy.layout.down(),
             desc='Move focus down in current stack pane'
             ),
         Key([mod], "k",
             lazy.layout.up(),
             desc='Move focus up in current stack pane'
             ),
         # CHANGE FOCUS
         Key([mod], "Up", lazy.layout.up()),
         Key([mod], "Down", lazy.layout.down()),
         Key([mod], "Left", lazy.layout.left()),
         Key([mod], "Right", lazy.layout.right()),
        Key([mod], "n",
             lazy.layout.normalize(),
             desc='normalize window size ratios'
             ),
         Key([mod], "m",
             lazy.layout.maximize(),
             desc='toggle window between minimum and maximum sizes'
             ),
         Key([mod, "shift"], "f",
             lazy.window.toggle_floating(),
             desc='toggle floating'
             ),
         Key([mod], "f",
             lazy.window.toggle_fullscreen(),
             desc='toggle fullscreen'
             ),

         # RESIZE UP, DOWN, LEFT, RIGHT
        Key([mod, "control"], "l",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
            ),
         Key([mod, "control"], "Right",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
            ),
        Key([mod, "control"], "h",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
            ),
        Key([mod, "control"], "Left",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
            ),
        Key([mod, "control"], "k",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
            ),
        Key([mod, "control"], "Up",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
            ),
        Key([mod, "control"], "j",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
            ),
        Key([mod, "control"], "Down",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
            ),


        # FLIP LAYOUT FOR MONADTALL/MONADWIDE
        Key([mod, "shift"], "f", lazy.layout.flip()),

        # FLIP LAYOUT FOR BSP
        Key([mod, "mod1"], "k", lazy.layout.flip_up()),
        Key([mod, "mod1"], "j", lazy.layout.flip_down()),
        Key([mod, "mod1"], "l", lazy.layout.flip_right()),
        Key([mod, "mod1"], "h", lazy.layout.flip_left()),

        # MOVE WINDOWS UP OR DOWN BSP LAYOUT
        Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
        Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
        Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
        Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

         ### Treetab controls
        Key([mod, "control"], "k",
            lazy.layout.section_up(),
            desc='Move up a section in treetab'
            ),
        Key([mod, "control"], "j",
            lazy.layout.section_down(),
            desc='Move down a section in treetab'
        ),



        # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
         Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
         Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
         Key([mod, "shift"], "Left", lazy.layout.swap_left()),
         Key([mod, "shift"], "Right", lazy.layout.swap_right()),
        ### Stack controls
        Key([mod, "shift"], "Tab",
             lazy.layout.rotate(),
             lazy.layout.flip(),
             desc='Switch which side main pane occupies (XmonadTall)'
             ),
        Key([mod], "space",
             lazy.layout.next(),
             desc='Switch window focus to other pane(s) of stack'
             ),
        Key([mod, "shift"], "space",
             lazy.layout.toggle_split(),
             desc='Toggle between split and unsplit sides of stack'
             ),

        # INCREASE/DECREASE BRIGHTNESS
        Key([], "XF86MonBrightnessUp", lazy.spawn("~/system_scripts/brightness up")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("~/system_scripts/brightness down")),

       # Media hotkeys
        Key([], 'XF86AudioRaiseVolume',
            lazy.spawn('amixer -D pulse sset Master 1%+'),
            desc='Raise volume'
            ),
        Key([], 'XF86AudioLowerVolume',
            lazy.spawn('amixer -D pulse sset Master 1%-'),
            desc='Decrease volume'
            ),
        Key([], 'XF86AudioMute',
            lazy.spawn('pamixer -t'),
            desc='Mute volume'
            ),
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
        Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
        Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
        Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
# SCREENSHOTS

        Key([], "Print", lazy.spawn('flameshot full -p ~/Images')),
        Key(["control"], "Print", lazy.spawn('flameshot full -p ~/Images')),

        # Qtile CMD
        Key([mod], 'F1',
            lazy.spawn('/home/rekla/.config/qtile/dqtile-cmd.sh'),
            desc='Qtile CMD'
            ),
        Key([mod], 'F2', lazy.spawn('~/.config/qtile/scripts/picom-toggle.sh')),

         # Dmenu scripts launched using the key chord SUPER+p followed by 'key'
         KeyChord([mod], "p", [
             Key([], "e",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-confedit"),
                 desc='Choose a config file to edit'
                 ),
             Key([], "i",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-maim"),
                 desc='Take screenshots via dmenu'
                 ),
             Key([], "k",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-kill"),
                 desc='Kill processes via dmenu'
                 ),
             Key([], "l",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-logout"),
                 desc='A logout menu'
                 ),
             Key([], "m",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-man"),
                 desc='Search manpages in dmenu'
                 ),
             Key([], "o",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-bookman"),
                 desc='Search your qutebrowser bookmarks and quickmarks'
                 ),
             Key([], "r",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-reddit"),
                 desc='Search reddit via dmenu'
                 ),
             Key([], "s",
                 lazy.spawn("/home/rekla/.config/dmscripts/scripts/dm-websearch"),
                 desc='Search various search engines via dmenu'
                 )
         ])

]

groups = []

# FOR QWERTY KEYBOARDS
group_indices = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]

# FOR AZERTY KEYBOARDS
group_keys = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "section", "egrave", "exclam", "ccedilla", "agrave"]

#group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ", "7 ", "8 ", "9 ", "0",]
group_labels = ["", "", "", "", "", "", "", "", "", "",]
#group_labels = ["", "", "", "", "",]
#group_labels = ["Web", "Edit/chat", "Image", "Gimp", "Meld", "Video", "Vb", "Files", "Mail", "Music",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "treetab", "floating"]
#group_layouts = ["monadtall", "matrix", "monadtall", "bsp", "monadtall", "matrix", "monadtall", "bsp", "monadtall", "monadtall",]

for i in range(len(group_keys)):
    groups.append(
        Group(
            name=group_indices[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for k, group in zip(group_keys, groups):
    keys.extend([
        Key([mod], k, lazy.group[group.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
        Key(["mod1"], "Tab", lazy.screen.next_group()),
        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], k, lazy.window.togroup(group.name) , lazy.group[group.name].toscreen())
    ])

#for i in groups:
#    keys.extend([

#        Key([mod], i.name, lazy.group[i.name].toscreen()),
#        Key([mod], "Tab", lazy.screen.next_group()),
#        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),
#        Key(["mod1"], "Tab", lazy.screen.next_group()),
#        Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),
#        Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
#    ])


layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "e1acff",
                "border_normal": "1D2330"
                }

layouts = [
    layout.MonadWide(**layout_theme),
    layout.Bsp(**layout_theme),
    layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    layout.RatioTile(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    #layout.Stack(num_stacks=2),
    layout.RatioTile(**layout_theme),
    layout.TreeTab(
         font = "Ubuntu",
         fontsize = 10,
         sections = ["FIRST", "SECOND", "THIRD", "FOURTH"],
         section_fontsize = 10,
         border_width = 2,
         bg_color = "1c1f24",
         active_bg = "c678dd",
         active_fg = "000000",
         inactive_bg = "a9a1e1",
         inactive_fg = "1c1f24",
         padding_left = 0,
         padding_x = 0,
         padding_y = 5,
         section_top = 10,
         section_bottom = 20,
         level_shift = 8,
         vspace = 3,
         panel_width = 200
         ),
    layout.Floating(**layout_theme)
]

colors = [["#282c34", "#282c34"],
          ["#1c1f24", "#1c1f24"],
          ["#dfdfdf", "#dfdfdf"],
          ["#ff6c6b", "#ff6c6b"],
          ["#98be65", "#98be65"],
          ["#da8548", "#da8548"],
          ["#51afef", "#51afef"],
          ["#c678dd", "#c678dd"],
          ["#46d9ff", "#46d9ff"],
          ["#a9a1e1", "#a9a1e1"]]

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font="Ubuntu Bold",
    fontsize = 10,
    padding = 2,
    background=colors[2]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Image(
                       filename = "~/.config/qtile/icons/python-white.png",
                       scale = "False",
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm)}
                       ),
            widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "UbuntuMono Nerd Font",
                       fontsize = 18,
                       margin_y = 3,
                       margin_x = 0,
                       padding_y = 5,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[7],
                       rounded = False,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[6],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[6],
                       other_screen_border = colors[4],
                       foreground = colors[2],
                       background = colors[0]
                       ),
 
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[2],
                       background = colors[0],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[0],
                       padding = 5
                       ),
             widget.TextBox(
                       text = '|',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = '474747',
                       padding = 2,
                       fontsize = 14
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 5
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[0],
                       background = colors[0]
                       ),
              widget.TextBox(
                       text='',
                       font = "Ubuntu Mono",
                       background = colors[0],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.BatteryIcon(
                      background = colors[4],
                      padding = 5
                       ),
              widget.Battery(
                      background = colors[4],
                      foreground = colors[1],
                      charge_char = '+',
                      discharge_char = '',
                      unknown_char='',
                      format = '{char}{percent:2.0%}',
                      padding = 5
                      ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[4],
                       foreground = colors[3],
                       padding = 0,
                       fontsize = 37
                       ),
             widget.Net(
                       interface = "enp4s0",
                       format = 'Net: {down} ↓↑ {up}',
                       foreground = colors[1],
                       background = colors[3],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[3],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.ThermalSensor(
                       foreground = colors[1],
                       background = colors[4],
                       threshold = 90,
                       fmt = 'CPU: {}',
                       padding = 0
                       ),

              widget.NvidiaSensors(
                       foreground = colors[1],
                       background = colors[4],
                       threshold = 90,
                       format = '|  GPU: {temp}°C',
                       gpu_bus_id = '01:00.0',
                       padding = 5
                       ),
              widget.TextBox(
                       text='',
                       font = "Ubuntu Mono",
                       background = colors[4],
                       foreground = colors[5],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.CheckUpdates(
                       update_interval = 1800,
                       distro = "Arch_checkupdates",
                       display_format = "Updates: {updates} ",
                       foreground = colors[1],
                       colour_have_updates = colors[1],
                       colour_no_updates = colors[1],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       padding = 5,
                       background = colors[5],
                       no_update_string = 'no updates'
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[5],
                       foreground = colors[6],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.Memory(
                       foreground = colors[1],
                       background = colors[6],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')},
                       fmt = 'Mem: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[6],
                       foreground = colors[7],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.Volume(
                       foreground = colors[1],
                       background = colors[7],
                       fmt = 'Vol: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[7],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.KeyboardLayout(
                       foreground = colors[1],
                       background = colors[8],
                       fmt = 'Keyboard: {}',
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[8],
                       foreground = colors[7],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.OpenWeather(
                        app_key = '9186a934bce7914bfc0f42e4f04071a6',
                        cityid = '2986933',
                       foreground = colors[1],
                       background = colors[7],
                       format = '{location_city}: {main_temp} °{units_temperature} {weather_details}',
                       language = 'fr'
                      ),
              widget.TextBox(
                       text = '',
                       font = "Ubuntu Mono",
                       background = colors[7],
                       foreground = colors[9],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.Clock(
                       foreground = colors[1],
                       background = colors[9],
                       format = "%A, %B %d - %H:%M "
                       ),
              ]
    return widgets_list

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.85, size=20, background= "000000")),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.85, size=20, background= "000000"))]

if __name__ in ["config", "__main__"]:
    screens = init_screens()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()
    widgets_screen2 = init_widgets_screen2()

def window_to_previous_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

def window_to_previous_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i != 0:
        group = qtile.screens[i - 1].group.name
        qtile.current_window.togroup(group)

def window_to_next_screen(qtile):
    i = qtile.screens.index(qtile.current_screen)
    if i + 1 != len(qtile.screens):
        group = qtile.screens[i + 1].group.name
        qtile.current_window.togroup(group)

def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)

#keys.extend([
#    Key([mod,"shift"],  "Left",  lazy.function(window_to_next_screen)),    
#    Key([mod,"shift"],  "Right", lazy.function(window_to_previous_screen)),
#    Key([mod,"control"],"Left",  lazy.function(window_to_next_group)),
#    Key([mod,"control"],"Right", lazy.function(window_to_previous_group)),
#])

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_app_rules = []  # type: List
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    # default_float_rules include: utility, notification, toolbar, splash, dialog,
    # file_progress, confirm, download and error.
    *layout.Floating.default_float_rules,
    Match(title='Confirmation'),      # tastyworks exit box
    Match(title='Qalculate!'),        # qalculate-gtk
    Match(wm_class='kdenlive'),       # kdenlive
    Match(wm_class='pinentry-gtk-2'), # GPG key password entry
])
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

@hook.subscribe.startup_complete
def startup_complete():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/startup_complete.sh'])


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
