import os
import json

GESTURE_PREFIX='gesture:'

# Libinput gestures configuration file path
LIG_CONF_FILE_PATH_ROOT='/etc/libinput-gestures.conf'

# paths for gestures manager own configuration file
HOME = os.environ.get('HOME')
CONFDIR = HOME+('/.config')
LIG_USER_CONF_FILE_PATH = CONFDIR+'/libinput-gestures.conf'
GM_CONF_FILE_PATH = CONFDIR+'/gesturesmanger.json'

if not os.path.isdir(CONFDIR):
    os.makedirs(CONFDIR)

if not os.path.isfile(LIG_USER_CONF_FILE_PATH):
    out=open(LIG_USER_CONF_FILE_PATH, 'w')
    out.write('# Gestures Manager created this configuration file for Libinput Gestures')
    out.close()

LIG_CONF_FILE_COMMENTS= \
"""# Configuration file for libinput-gestures.
#
# The default configuration file exists at /etc/libinput-gestures.conf
# but a user can create a personal custom configuration file at
# ~/.config/libinput-gestures.conf.
#
# Lines starting with '#' and blank lines are ignored.
# At present only gesture lines are configured in this file.
#
# Each gesture: line has 3 [or 4] arguments:
#
# action motion [finger_count] command
#
# where action and motion is either:
#     swipe up
#     swipe down
#     swipe left
#     swipe right
#     pinch in
#     pinch out
#
# command is the remainder of the line and is any valid shell command +
# arguments.
#
# finger_count is optional (and is typically 3 or 4). If specified then
# the command is executed when exactly that number of fingers is used in
# the gesture. If not specified then the command is executed when that
# gesture is executed with any number of fingers. Gesture lines
# specified with finger_count have priority over the same gesture
# specified without any finger_count.
#
# Typically command will be xdotool, or wmctrl. See "man xdotool" for
# the many things you can action with that tool."""

kvpairs = dict()

if not os.path.isfile(GM_CONF_FILE_PATH):
    gestures_f = open(GM_CONF_FILE_PATH, 'w')
    gestures_f.close()


def string_gm_to_lig(gm_string):
    words = gm_string.split()
    lig_string = ' '.join([GESTURE_PREFIX, words[2], words[3], words[0]])
    return lig_string

def save_gm_conf_file():
    gestures_f=open(GM_CONF_FILE_PATH, 'w')
    gestures_f.write(json.dumps(kvpairs))
    gestures_f.close()

def save_lig_conf_file():
    s=''
    for key, value in kvpairs.items():
        if value != '':
            if key[0].isdigit():
                s += string_gm_to_lig(key) + " " + value
            else:
                s += key + " " + value
            s += '\n'
    lig_f=open(LIG_USER_CONF_FILE_PATH, 'w')
    lig_f.write(s)
    lig_f.close()

def save_files():
    save_gm_conf_file()
    save_lig_conf_file()

def get_gesture_dict():
    gesture_dict = dict()
    for k, v in kvpairs.items():
        if k[0].isdigit():
            gesture_dict[k] = v
    return gesture_dict

def add_elements(datadict):
    for k, v in datadict.items():
        kvpairs[k] = v
    save_files()

def update_element(key, value):
    kvpairs[key] = value
    save_files()

def get_element(key, defaultval = ''):
    return kvpairs.get(key, defaultval)

def remove_element(key):
    kvpairs.pop(key)
    save_files()


gestures_f = open(GM_CONF_FILE_PATH, 'r')

try:
    gestures_text=gestures_f.read()
    kvpairs=json.loads(gestures_text)
    gestures_f.close()
except ValueError:
    gestures_f.close()
    save_gm_conf_file()
