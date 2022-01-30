# -*- coding: utf-8 -*-
import os
import re
import socket
import subprocess
from libqtile.config import Click, Drag, Group, KeyChord, Key, Match, Screen, ScratchPad, DropDown
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook, qtile
from typing import List  # noqa: F401from typing import List  # noqa: F401

mod = "mod4"              # Sets mod key to SUPER/WINDOWS
alt = "mod1"
myTerm = "alacritty"      # My terminal of choice
myBrowser = "qutebrowser" # My terminal of choice

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


def to_urgent():
    @lazy.function
    def __inner(qtile):
        cg = qtile.currentGroup
        for group in qtile.groupMap.values():
            if group == cg:
                continue
            if len([w for w in group.windows if w.urgent]) > 0:
                qtile.currentScreen.setGroup(group)
                break

    return __inner



def switch_screens(qtile):
    i = qtile.screens.index(qtile.current_screen)
    group = qtile.screens[i - 1].group
    qtile.current_screen.set_group(group)


keys = [
        ### The essentials
         Key([mod], "Return",lazy.spawn(myTerm),desc="Launch terminal"),
         Key([mod], "KP_Enter",lazy.spawn('alacritty'),desc="Launch terminal"),
         Key([alt], "Return",lazy.spawn("pamac-manager"),desc="Pamac Manager"),
         Key([mod, "shift"], "Return",lazy.spawn("thunar"),desc="Launch Thunar"),
         Key([mod, "control"], "Return",lazy.spawn("geany"),desc="Launch Geany"),
         
         Key([mod, "shift"], "d",lazy.spawn("dmenu_run -i -nb '#191919' -nf '#fea63c' -sb '#fea63c' -sf '#191919' -fn 'DejaVuSansMono:bold:pixelsize=14'"),desc='Run dmenu'),
         Key([mod], "d",lazy.spawn("rofi -modi drun -show drun -config ~/.config/rofi/rofidmenu.rasi"),desc='Run rofi'),
         Key([mod, "control"], "d",lazy.spawn('nwggrid -p -o 0.4'),desc="Run nwggrid"),
        
         Key([mod], "t",lazy.spawn("rofi -show window -config ~/.config/rofi/rofidmenu.rasi"),desc='Show running applications'),
         
         Key([mod], "w",lazy.spawn("brave"),desc='Run Brave'),
         Key([mod, "shift"], "w",lazy.spawn("firefox"),desc='Firefox'),
         Key([mod, "control"], "w",lazy.spawn(myBrowser),desc='Qutebrowser'),
         
         Key([mod], "space",lazy.next_layout(),desc='Next layout'),
         Key([mod, "control"], "space",lazy.prev_layout(),desc='Previous layout'),
         Key([mod, "shift"], "space",lazy.window.toggle_floating(),desc='toggle floating'),
         
         Key([mod], "q",lazy.window.kill(),desc='Kill active window'),
         Key([mod, "shift"], "q",lazy.shutdown(),desc='Shutdown Qtile'),
         
         Key([mod], "r",lazy.spawncmd(),desc="Spawn a command using a prompt widget"),
         Key([mod, "shift"], "r",lazy.restart(),desc='Restart Qtile'),
         Key([mod, "control"], "r",lazy.reload_config(),desc="Reload the config"),
     
         Key([mod, "shift"], "e",lazy.spawn("/home/rekla/.config/qtile/scripts/powermenu"),desc='Exit Menu'),
         
         Key([alt, "control"], "l",lazy.spawn("i3lock"),desc='i3exit lock'),

         ### Switch focus to specific monitor (out of two)
         Key([mod], "comma",lazy.prev_screen(),desc='Move focus to prev monitor'),
         Key([mod], "semicolon",lazy.next_screen(),desc='Move focus to next monitor'),
         Key([mod, "control"], "comma",lazy.to_screen(0),desc='Keyboard focus to monitor 1'),
         Key([mod, "control"], "semicolon",lazy.to_screen(1),desc='Keyboard focus to monitor 2'),      
         
         # Move windows to different physical screens
         Key([mod, "shift"], "semicolon", lazy.function(window_to_previous_screen), desc="Move windows to previous screen"),
         Key([mod, "shift"], "comma", lazy.function(window_to_next_screen), desc="Move windows to next screen"),
         Key([mod, "shift"], "t", lazy.function(switch_screens), desc="Sxitch windows to next/previous screen"),
         
         Key([mod], "n",lazy.layout.normalize(),desc='normalize window size ratios'),
         Key([mod], "m",lazy.layout.maximize(),desc='toggle window between minimum and maximum sizes'),
         Key([mod], "f",lazy.window.toggle_fullscreen(),desc='toggle fullscreen'),

         Key([mod, "shift"], "f", lazy.layout.flip(), desc="FLIP LAYOUT FOR MONADTALL/MONADWIDE"),

         ### Layout control [h,l,j,k]
         Key([mod], "h",lazy.layout.move_left(), lazy.layout.left(),desc='Move left / Move up a section in treetab'),
         Key([mod], "l",lazy.layout.move_right(), lazy.layout.right(),desc='Move right / Move down a section in treetab'),
         Key([mod], "j",lazy.layout.down(),desc='Move focus down in current stack pane'),
         Key([mod], "k",lazy.layout.up(),desc='Move focus up in current stack pane'),
         
         Key([mod, "mod1"], "h", lazy.layout.previous(), lazy.layout.flip_left(), desc='Move up a section in stack / flip left BSP'),
         Key([mod, "mod1"], "l", lazy.layout.next(), lazy.layout.flip_right(), desc='Move up a section in stack / flip right BSP'),
         Key([mod, "mod1"], "j", lazy.layout.flip_down(),lazy.layout.section_down(), desc="flip down BSP / Move down a section in treetab"),
         Key([mod, "mod1"], "k", lazy.layout.flip_up(),lazy.layout.section_up(), desc="flip up BSP / Move up a section in treetab"),
         
         Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="move left BSP"),
         Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="move right BSP"),
         Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="move down BSP"),
         Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="move up BSP"),
         
         ### Layout control [Left,Right,Down,Up]
         Key([mod], "Left",lazy.layout.move_left(), lazy.layout.left(),desc='Move left / Move up a section in treetab'),
         Key([mod], "Right",lazy.layout.move_right(), lazy.layout.right(),desc='Move right / Move down a section in treetab'),
         Key([mod], "Down",lazy.layout.down(),desc='Move focus down in current stack pane'),
         Key([mod], "Up",lazy.layout.up(),desc='Move focus up in current stack pane'),
         
         Key([mod, "mod1"], "Left", lazy.layout.previous(), lazy.layout.flip_left(), desc='Move up a section in stack / flip left BSP'),
         Key([mod, "mod1"], "Right", lazy.layout.next(), lazy.layout.flip_right(), desc='Move up a section in stack / flip right BSP'),
         Key([mod, "mod1"], "Down", lazy.layout.flip_down(),lazy.layout.section_down(), desc="flip down BSP / Move down a section in treetab"),
         Key([mod, "mod1"], "Up", lazy.layout.flip_up(),lazy.layout.section_up(), desc="flip up BSP / Move up a section in treetab"),
         
         Key([mod, "shift"], "Left", lazy.layout.shuffle_left(), desc="move left BSP"),
         Key([mod, "shift"], "Right", lazy.layout.shuffle_right(), desc="move right BSP"),
         Key([mod, "shift"], "Down", lazy.layout.shuffle_down(), desc="move down BSP"),
         Key([mod, "shift"], "Up", lazy.layout.shuffle_up(), desc="move up BSP"),
         
        
         ### Stack controls
         Key([mod, "mod1"], "KP_Enter",lazy.layout.rotate(),lazy.layout.flip(),desc='Switch which side main pane occupies (XmonadTall)'),
         Key([mod, "mod1"], "space",lazy.layout.next(),desc='Switch window focus to other pane(s) of stack'),
         Key([mod, "mod1", "control"], "space",lazy.layout.toggle_split(),desc='Toggle between split and unsplit sides of stack'),

         # RESIZE UP, DOWN, LEFT, RIGHT
         Key([mod, "control"], "l",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
            desc="resize right"
            ),
         Key([mod, "control"], "Right",
            lazy.layout.grow_right(),
            lazy.layout.grow(),
            lazy.layout.increase_ratio(),
            lazy.layout.delete(),
            desc="resize right"
            ),
         Key([mod, "control"], "h",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
            desc="resize left"
            ),
         Key([mod, "control"], "Left",
            lazy.layout.grow_left(),
            lazy.layout.shrink(),
            lazy.layout.decrease_ratio(),
            lazy.layout.add(),
            desc="resize left"
            ),
         Key([mod, "control"], "k",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
            desc="resize up"
            ),
         Key([mod, "control"], "Up",
            lazy.layout.grow_up(),
            lazy.layout.grow(),
            lazy.layout.decrease_nmaster(),
            desc="resize up"
            ),  
        Key([mod, "control"], "j",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
            desc="resize down"
            ),
        Key([mod, "control"], "Down",
            lazy.layout.grow_down(),
            lazy.layout.shrink(),
            lazy.layout.increase_nmaster(),
            desc="resize down"
            ),


        # INCREASE/DECREASE BRIGHTNESS
        Key([], "XF86MonBrightnessUp", lazy.spawn("/home/rekla/.config/system_scripts/brightness up")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("/home/rekla/.config/system_scripts/brightness down")),

       # Media hotkeys
        Key([], 'XF86AudioRaiseVolume',lazy.spawn('amixer -D pulse sset Master 5%+'),desc='Raise volume'),
        Key([], 'XF86AudioLowerVolume',lazy.spawn('amixer -D pulse sset Master 5%-'),desc='Decrease volume'),
        Key([], 'XF86AudioMute',lazy.spawn('pamixer -t'),desc='Mute volume'),
        Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
        Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
        Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
        Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

		# SCREENSHOTS
        Key([], "Print", lazy.spawn('flameshot screen -p /home/rekla/Images')),
        Key(["control"], "Print", lazy.spawn('flameshot full -p /home/rekla/Images')),

        # Qtile CMD
        Key([mod], 'F1',lazy.spawn('/home/rekla/.config/qtile/scripts/dqtile-cmd.sh'),desc='Qtile CMD'),
        Key([mod], 'F2', lazy.spawn('/home/rekla/.config/qtile/scripts/picom-toggle.sh')),
        Key([mod], 'F6', lazy.spawn('/home/rekla/.config/qtile/scripts/keyhint_script.sh')),
        Key([mod], 'F10', to_urgent()),

         # Emacs programs launched using the key chord CTRL+e followed by 'key'
         KeyChord(["control"],"e", [
             Key([], "e",
                 lazy.spawn("emacsclient -c -a 'emacs'"),
                 desc='Launch Emacs'
                 ),
             Key([], "b",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(ibuffer)'"),
                 desc='Launch ibuffer inside Emacs'
                 ),
             Key([], "d",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(dired nil)'"),
                 desc='Launch dired inside Emacs'
                 ),
             Key([], "i",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(erc)'"),
                 desc='Launch erc inside Emacs'
                 ),
             Key([], "m",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(mu4e)'"),
                 desc='Launch mu4e inside Emacs'
                 ),
             Key([], "n",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(elfeed)'"),
                 desc='Launch elfeed inside Emacs'
                 ),
             Key([], "s",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(eshell)'"),
                 desc='Launch the eshell inside Emacs'
                 ),
             Key([], "v",
                 lazy.spawn("emacsclient -c -a 'emacs' --eval '(+vterm/here nil)'"),
                 desc='Launch vterm inside Emacs'
                 )
         ]),

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

group_names = ["1: ", "2: ", "3: ", "4: ", "5: ", "6: ", "7: ", "8: ", "9: ", "10: ",]
group_keys = ["ampersand", "eacute", "quotedbl", "apostrophe", "parenleft", "minus", "egrave", "underscore", "ccedilla", "agrave"]
group_keyspad = ["KP_1", "KP_2", "KP_3", "KP_4", "KP_5", "KP_6", "KP_7", "KP_8", "KP_9", "KP_0"]

group_labels = ["", "", "", "", "", "", "", "", "", "",]

group_layouts = ["monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "monadtall", "treetab", "floating"]

for i in range(len(group_keys)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i, (k, group) in enumerate(zip(group_keys, groups)):
    keys.extend([
        Key([mod], k, lazy.group[group.name].toscreen()),
        Key([mod], "Tab", lazy.screen.next_group()),
        Key([mod, "shift" ], "Tab", lazy.screen.prev_group()),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "control"], k, lazy.window.togroup(group.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([mod, "shift"], k, lazy.window.togroup(group.name) , lazy.group[group.name].toscreen()),
    ])


groups.append(
    ScratchPad("scratchpad", [
        # define a drop down terminal.
        # it is placed in the upper third of screen by default.
        DropDown("term", "/usr/bin/alacritty", opacity=0.88, height=0.55, width=0.80, ),
    ]) )

keys.extend([
    # Scratchpad
    # toggle visibiliy of above defined DropDown named "term"
    Key([mod], 'F12', lazy.group['scratchpad'].dropdown_toggle('term'))
])

layout_theme = {"border_width": 2,
                "margin": 8,
                "border_focus": "#ff00ff",
                "border_normal": "#f4c2c2"
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
         bg_color = "#141414",
         active_bg = "#0000ff",
         active_fg = "000000",
         inactive_bg = "#1e90ff",
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

colors = [
            ["#282c34", "#282c34"],
            ["#1c1f24", "#1c1f24"],
            ["#dfdfdf", "#dfdfdf"],
            ["#ff6c6b", "#ff6c6b"],
            ["#98be65", "#98be65"],
            ["#da8548", "#da8548"],
            ["#51afef", "#51afef"],
            ["#c678dd", "#c678dd"],
            ["#46d9ff", "#46d9ff"],
            ["#a9a1e1", "#a9a1e1"],
			["#2F343F", "#2F343F"], # color 0
            ["#2F343F", "#2F343F"], # color 1
            ["#c0c5ce", "#c0c5ce"], # color 2
            ["#e75480", "#e75480"], # color 3
            ["#f4c2c2", "#f4c2c2"], # color 4
            ["#ffffff", "#ffffff"], # color 5
            ["#ff0000", "#ff0000"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#000000", "#000000"], # color 8
            ["#c40234", "#c40234"], # color 9
            ["#6790eb", "#6790eb"], # color 10
            ["#ff00ff", "#ff00ff"], #11
            ["#4c566a", "#4c566a"], #12
            ["#282c34", "#282c34"], #13
            ["#212121", "#212121"], #14
            ["#98c379", "#98c379"], #15
            ["#b48ead", "#b48ead"], #16
            ["#abb2bf", "#abb2bf"],# color 17
            ["#81a1c1", "#81a1c1"], #18
            ["#56b6c2", "#56b6c2"], #19
            ["#c678dd", "#c678dd"], #20
            ["#e06c75", "#e06c75"], #21
            ["#fb9f7f", "#fb9f7f"], #22
            ["#ffd47e", "#ffd47e"]] #23


   # Widgets

def init_widgets_defaults():
    return dict(font="UbuntuMono Nerd Font",
                fontsize = 11,
                padding = 2,
                background=colors[2])

widget_defaults = init_widgets_defaults()

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
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
                       background = colors[15],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('jgmenu_run')}
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
                       highlight_color = colors[21],
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
                       font = "UbuntuMono Nerd Font",
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
                       font = "UbuntuMono Nerd Font",
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
                       font = "UbuntuMono Nerd Font",
                       background = colors[0],
                       foreground = colors[4],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.BatteryIcon(
                      background = colors[4],
                      padding = 2
                       ),
              widget.Battery(
                      background = colors[4],
                      foreground = colors[1],
                      charge_char = '+',
                      discharge_char = '',
                      unknown_char='',
                      format = '{char}{percent:2.0%}',
                      padding = 2
                      ),
              widget.TextBox(
                       text = '',
                       font = "UbuntuMono Nerd Font",
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
                       padding = 2
                       ),
              widget.TextBox(
                       text = '',
                       font = "UbuntuMono Nerd Font",
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
                       padding = 2
                       ),
              widget.TextBox(
                       text='',
                       font = "UbuntuMono Nerd Font",
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
                       padding = 2,
                       background = colors[5],
                       no_update_string = 'no updates'
                       ),
              widget.TextBox(
                       text = '',
                       font = "UbuntuMono Nerd Font",
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
                       padding = 2
                       ),
              widget.TextBox(
                       text = '',
                       font = "UbuntuMono Nerd Font",
                       background = colors[6],
                       foreground = colors[7],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.Volume(
                       foreground = colors[1],
                       background = colors[7],
                       fmt = 'Vol: {}',
                       padding = 2
                       ),
              widget.TextBox(
                       text = '',
                       font = "UbuntuMono Nerd Font",
                       background = colors[7],
                       foreground = colors[8],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.KeyboardLayout(
                       foreground = colors[1],
                       background = colors[8],
                       fmt = 'Keyboard: {}',
                       padding = 2
                       ),
              widget.TextBox(
                       text = '',
                       font = "UbuntuMono Nerd Font",
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
                       font = "UbuntuMono Nerd Font",
                       background = colors[7],
                       foreground = colors[9],
                       padding = 0,
                       fontsize = 37
                       ),
              widget.Clock(
                       foreground = colors[1],
                       background = colors[9],
                       mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e calcurse')},
                       format = "%A, %B %d - %H:%M "
                       ),
              ]
    return widgets_list


widgets_list = init_widgets_list()

def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
   # del widgets_screen1[9:10]               # Slicing removes unwanted widgets (systray) on Monitors 1,3
    return widgets_screen2                 # Monitor 2 will display all widgets in widgets_list

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()

def init_screens():
    return [Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=0.85, size=20, background= "000000")),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), opacity=0.85, size=20, background= "000000"))]

screens = init_screens()

mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

#########################################################
################ assgin apps to groups ##################
#########################################################
# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["pcmanfm", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "pcmanfm", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME

main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])
    
@hook.subscribe.startup_complete
def startup_complete():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/startup_complete.sh'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]

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
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='confirmreset'),
    Match(wm_class='makebranch'),
    Match(wm_class='maketag'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(title='branchdialog'),
    Match(title='Open File'),
    Match(title='pinentry'),
    Match(wm_class='ssh-askpass'),
    Match(wm_class='lxpolkit'),
    Match(wm_class='Lxpolkit'),
    Match(wm_class='yad'),
    Match(wm_class='Yad'),
    Match(wm_class='Cairo-dock'),
    Match(wm_class='cairo-dock')
])
auto_fullscreen = True
focus_on_window_activation = "focus" # or smart
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
