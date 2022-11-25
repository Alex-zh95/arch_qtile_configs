import os
import socket
import subprocess
from libqtile import layout, bar, widget, hook
from libqtile.config import Drag, Group, Key, Match, Screen
from libqtile.command import lazy
#from libqtile.widget import Spacer
import arcobattery

#mod4 or mod = super key
mod = "mod4"
mod1 = "alt"
mod2 = "control"
home = os.path.expanduser('~')

# Touchpad parameters for TUXEDO - touchpad controls relegated to different script
# touchpadName = r'"UNIW0001:00 093A:0255 Touchpad"'

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)


@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [
    Key([mod], "Return", lazy.spawn(f"alacritty -e {home}/.config/tmux/tmux_init.py"), desc="Launch terminal with last detached tmux instance"),
    Key([mod], "d", lazy.spawn("rofi -show drun"), desc="Launch rofi launcher"),
    Key([mod], "s", lazy.spawn(f'rofi -show dggr -modi "dggr:{home}/.config/rofi/ddgr_search.sh" -font "Hack 20" -eh 3'), desc="Lauch duckduckgo search in rofi"),
    Key([mod], "w", lazy.spawn("rofi -show window"), desc="Launch rofi window browser"),
   	Key([mod], "t", lazy.spawn(home+"/.config/qtile/tuxedo_trackpad_toggle.sh"), desc="Toggle touchpad"),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "p", lazy.spawn("pavucontrol"), desc="Launch pavucontrol"),

    Key([mod, "shift"], "Return", lazy.spawn("alacritty -e tmux"), desc="Launch terminal with new tmux instance"),
    Key([mod, "shift"], "q", lazy.spawn("archlinux-logout"), desc="Logout screen"),
    Key([mod, "shift"], "r", lazy.restart()),

    # Screenshot
    Key([mod, "shift"], "c", lazy.spawn('xfce4-screenshooter -r -o ristretto')), 
    Key([mod], 'n', subprocess.run(['setxkbmap', '-option', 'caps:escape'])),

    # QTILE LAYOUT KEYS
    Key([mod, "shift"], "n", lazy.layout.normalize()),
    Key([mod], "space", lazy.next_layout()),
    Key([mod, "shift"], "space", lazy.prev_layout()),

    # CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),

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

    # TOGGLE SPLIT FUNCTIONS FOR COLUMN/STACK LAYOUT
    # Split mode on a pane allows for windows to be stacked over each other
    Key([mod, "shift"], "s", lazy.layout.toggle_split()), 

    # FLIP LAYOUT FOR BSP
    #Key([mod, "mod1"], "k", lazy.layout.flip_up()),
    #Key([mod, "mod1"], "j", lazy.layout.flip_down()),
    #Key([mod, "mod1"], "l", lazy.layout.flip_right()),
    #Key([mod, "mod1"], "h", lazy.layout.flip_left()),

    # MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "h", lazy.layout.shuffle_left()), 
    Key([mod, "shift"], "l", lazy.layout.shuffle_right()),

    # MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),

    # TOGGLE FLOATING LAYOUT
    Key([mod, "shift"], "w", lazy.window.toggle_floating()),

]

groups = []

# FOR QWERTY KEYBOARDS
group_dict = {
        "1": "columns",
        "2": "bsp",
        "3": "columns",
        "4": "bsp",
        "5": "columns",
        "6": "bsp",
        "7": "columns",
        "8": "max",
        "9": "max",
        "0": "max"
}

group_names = list(group_dict.keys())
group_labels = group_names
group_layouts = list(group_dict.values())

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))

for i in groups:
    keys.extend([

        #CHANGE WORKSPACES
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.next_screen(), desc='Next monitor'),
        Key([mod, "shift"], "Tab", lazy.screen.prev_group(), desc='Prev monitor'),

        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
        # MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        # Key([mod, "shift"], i.name, lazy.window.togroup(
        #    i.name), lazy.group[i.name].toscreen()),
    ])


def init_default_theme():
    return {
        "margin": [10, 5, 10, 5],
        "border_width": 2,
        "border_focus": "#fe8019",
        "border_normal": "#4c566a",
        'margin_on_single': 0
    }


default_theme = init_default_theme()

# Max theme - no margins needed
max_theme = init_default_theme()
max_theme["margin"] = 0
max_theme["border_width"] = 0

# BSP theme - set new splits at currently focused window
bsp_theme = init_default_theme()
bsp_theme["fair"] = False 

layouts = [
    layout.Columns(**default_theme),
    layout.Max(**max_theme),
    layout.Bsp(**bsp_theme),
    layout.Floating(**default_theme),
]

# COLORS FOR THE BAR

def init_colors():
    return [["#2E3440", "#2E3440"],  # color 0 - Background 1 - Polar night - darkest
            ["#4c566a", "#4c566a"],  # color 1 - Background 2 - Polar night - lightest
            ["#c0c5ce", "#c0c5ce"],  # color 2 - LIGHT GRAY
            ["#fba922", "#fba922"],  # color 3 - ORANGE
            ["#3384d0", "#3384d0"],  # color 4 - Arco-Linux BLUE
            ["#eceff4", "#eceff4"],  # color 5 - OFF-WHITE
            ["#bf616a", "#bf616a"],  # color 6 - RED
            ["#90ff83", "#90ff83"],  # color 7 - BRIGHT GREEN
            ["#6c0000", "#6c0000"],  # color 8 - MAROON
            ["#d8dee9", "#d8dee9"],  # color 9 - DARKER GRAY
            ["#3b4252", "#3b4252"],  # color 10 - Background 3 - Polar night - darker
            ["#d08770", "#d08770"],  # color 11 - Foreground highest - aurora orange
            ]


colors = init_colors()


# WIDGETS FOR THE BAR

# Remark: font size up'd to 24 due to high pixel density
def init_widgets_defaults() -> dict:
    return dict(
        font="Noto Sans",
        fontsize=24,
        padding=0,
        background=colors[0]
    )


def text_concatenator(input_string: str, sep=' - ') -> str:
	'''
	For the TaskList widget, the window names contain more string info than needed, so save only the first and last item (separated by character '-' (DEFAULT)
	'''
	mod_string = input_string.split(sep)

	return f'{mod_string[-1]} - {mod_string[0]}' if len(mod_string) > 1 else mod_string[-1]

widget_defaults = init_widgets_defaults()

def init_widgets_list(screen_id=1) -> list:
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
        widget.CurrentLayoutIcon(
            custom_icon_paths=[home+"/.config/qtile/icons"],
            scale=0.7,
            foreground=colors[5], 
            background=colors[10]
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[10] 
        ),
        widget.GroupBox(
            font="Noto Sans",
            fontsize=24,
            margin_y=2,
            margin_x=0,
            padding_y=10,
            padding_x=5,
            borderwidth=0,
            disable_drag=True,
            active=colors[4],
            inactive=colors[9],
            rounded=False,
            highlight_method="text",
            this_current_screen_border=colors[11],
            hide_unused=False,
            foreground=colors[3],
            background=colors[10]
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[10]
        ),
        widget.TextBox(
            font='MesloLGS NF',
            text='',
            padding=5,
            foreground=colors[9],
            background=colors[10],
            fontsize=36,
            mouse_callbacks = {'Button1': lazy.spawn('xfce4-screenshooter -r -o ristretto'), 'Button3': lazy.spawn('xfce4-screenshooter')}
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[10]
        ),
        widget.AGroupBox(
            foreground=colors[5],
            background=colors[10],
            border=colors[10], # Make the border invisible
            font='MesloLGS NF',
            fmt=' {}:',
            fontsize=24,
            mouse_callbacks = {'Button1': lazy.spawn("rofi -show drun")}
        ),
        widget.TextBox( # Powerline right-arrow
            font='MesloLGS NF',
            text=u"\ue0b0",
            foreground=colors[10],
            background=colors[1],
            fontsize=36
        ),
        widget.WindowName(
            foreground=colors[5],
            background=colors[1],
            font='Noto Sans',
            fmt='{}',
            empty_group_string='Ø',
            parse_text=text_concatenator,
            padding=7

        ),
        widget.TextBox(
            font='FontAwesome',
            text='',
            foreground=colors[6],
            background=colors[1],
            padding=4,
            fontsize=30,
            mouse_callbacks = {'Button1': lazy.window.kill()}
        ),
        widget.TextBox( # Powerline left-arrow
            font='MesloLGS NF',
            text=u"\ue0b2",
            foreground=colors[10],
            background=colors[1],
            fontsize=36
        ),
        # # battery option 1  ArcoLinux Horizontal icons do not forget to import arcobattery at the top
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[10],
            background=colors[10]
        ),
        arcobattery.BatteryIcon(
            padding=2,
            scale=0.9,
            y_poss=0,
            theme_path=home + "/.config/qtile/icons/battery_icons_horiz",
            update_interval=2,
            background=colors[10]
        ),
        widget.Battery(
            font="Noto Sans",
            update_interval=10,
            fontsize=24,
            foreground=colors[5],
            background=colors[10],
            show_short_text=False,
            format='{percent:2.0%}',
        )
    ]
    
    if screen_id == 1:
        widgets_list.extend([
            widget.Sep(
                linewidth=1,
                padding=10,
                foreground=colors[2],
                background=colors[10]
            ),
            widget.Systray(
                background=colors[10],
                icon_size=40,
                padding=4
            )
        ])

    widgets_list.extend([
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[2],
            background=colors[10]
        ), 
        widget.Memory(
            font="Noto Sans",
            format='  : {MemUsed:,.1f}G/{MemTotal:,.1f}G',
            measure_mem='G',
            measure_wap='G',
            update_interval=1,
            fontsize=24,
            foreground=colors[5],
            background=colors[10],
            mouse_callbacks = {'Button1': lazy.spawn("rofi -show window")},
            padding=4
        ),
        widget.TextBox( # Powerline left-arrow
            font='MesloLGS NF',
            text=u"\ue0b2",
            foreground=colors[11], # Foreground to be orange
            background=colors[10], # Background to match left gray box
            fontsize=36,
        ),
        widget.Clock(
            font="Noto Sans",
            foreground=colors[0],
            background=colors[11],
            fontsize=24,
            padding=1,
                format="  %Y-%m-%d  %H:%M "
        ),
        widget.Sep(
            linewidth=1,
            padding=10,
            foreground=colors[0],
            background=colors[11]
        ),
        widget.TextBox(
            foreground=colors[0],
            background=colors[11],
            font="Noto Sans",
            fontsize=24,
            text=os.getlogin() + " ⏻ ", 
            mouse_callbacks = {'Button1': lazy.spawn("archlinux-logout")}
        )
    ])

    return widgets_list

def init_widgets_screen(screen_id: int=1):
    widgets_screen = init_widgets_list(screen_id)
    return widgets_screen

def init_screens(): 
    return [
        Screen(top=bar.Bar(widgets=init_widgets_screen(1), size=36, opacity=0.8)),
        Screen(top=bar.Bar(widgets=init_widgets_screen(2), size=36, opacity=0.8)),
        Screen(top=bar.Bar(widgets=init_widgets_screen(3), size=36, opacity=0.8))
    ]


screens = init_screens()


# MOUSE CONFIGURATION - mod-left for move; mod-right or mod-control-left for resize
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod, "control"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size())
]

dgroups_key_binder = None
dgroups_app_rules = []

main = None


@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

    # Re-map the caps lock key to escape
    subprocess.run(['setxkbmap', '-option', 'caps:escape'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

    # In startup also refresh background
    home = os.path.expanduser('~')
    subprocess.run(['feh', '--bg-fill', home+'/Bilder/background.png', '&'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for()
            or window.window.get_wm_type() in floating_types):
        window.floating = True


floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = False 
bring_front_click = True
cursor_warp = False
floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    *layout.Floating.default_float_rules,
    Match(wm_class='confirmreset'),  # gitk
    Match(wm_class='makebranch'),  # gitk
    Match(wm_class='maketag'),  # gitk
    Match(wm_class='ssh-askpass'),  # ssh-askpass
    Match(title='branchdialog'),  # gitk
    Match(title='pinentry'),  # GPG key password entry
    Match(wm_class='Arcolinux-welcome-app.py'),
    Match(wm_class='Archlinux-tweak-tool.py'),
    Match(wm_class='Arcolinux-calamares-tool.py'),
    Match(wm_class='confirm'),
    Match(wm_class='dialog'),
    Match(wm_class='download'),
    Match(wm_class='error'),
    Match(wm_class='file_progress'),
    Match(wm_class='notification'),
    Match(wm_class='splash'),
    Match(wm_class='toolbar'),
    Match(wm_class='Arandr'),
    Match(wm_class='feh'),
    Match(wm_class='Galculator'),
    Match(wm_class='archlinux-logout'),
    Match(wm_class='xfce4-terminal'),
    Match(wm_class='pavucontrol'),

],  fullscreen_border_width=0, border_width=0)
auto_fullscreen = True

focus_on_window_activation = "focus"  # or smart

wmname = "LG3D"
