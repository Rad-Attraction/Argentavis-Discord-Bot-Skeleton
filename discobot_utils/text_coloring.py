"""
This module can be used to color terminal text on windows.

You can refer to its globals, for basic colors.
You can also call its functions for custom colors.
"""

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[34m' # blue
P  = '\033[35m' # purple
GR = '\033[90m' # grey

color_setting = True

def toggle_coloring():
    """
    Turn all color strings into empty strings or back.
    """
    global color_setting
    global W 
    W = '' if color_setting else '\033[0m'
    global R 
    R = '' if color_setting else '\033[31m'
    global G 
    G = '' if color_setting else '\033[32m'
    global O 
    O = '' if color_setting else '\033[33m'
    global B 
    B = '' if color_setting else '\033[34m'
    global P 
    P = '' if color_setting else '\033[35m'
    global GR
    GR = '' if color_setting else '\033[90m'
    color_setting = False

def new(red, green, blue):
    return f"\033[38;2;{red};{green};{blue}m"

def newbg(red, green, blue):
    return f"\033[48;2;{red};{green};{blue}m"
    
def newfgbg(fore_red, fore_green, fore_blue, back_red, back_green, back_blue):
    return f"\033[38;2;{fore_red};{fore_green};{fore_blue};48;2;{back_red};{back_green};{back_blue}m"


print(f"{R}Text {G}co{O}lo{B}ring.{W}")

#https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
"""
color cheatcodes
start
\033[

foreground
38;2;

background
48;2;

therefore
"\033[38;2;255;82;197;48;2;155;106;0m"
means a foreground of 255;82;197
and a bacnground of 155;106;0
"""