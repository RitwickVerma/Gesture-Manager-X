import os
import json
import fileIOHelper as fh

GESTURE_PREFIX='gesture:'

ACTION_SWIPE='swipe'
ACTION_PINCH='pinch'

ACTIONS=[ACTION_SWIPE, ACTION_PINCH]

D_UP='up'
D_DOWN='down'
D_LEFT='left'
D_RIGHT='right'
D_IN='in'
D_OUT='out'
D_RIGHT_UP='right_up'
D_RIGHT_DOWN='right_down'
D_LEFT_UP='left_up'
D_LEFT_DOWN='left_down'
D_CLOCK='clockwise'
D_ANTICLOCK='anticlockwise'

DIRECTIONS=[D_UP, D_DOWN, D_LEFT, D_RIGHT, D_IN, D_OUT, D_RIGHT_UP, D_RIGHT_DOWN, D_LEFT_UP, D_LEFT_DOWN, D_CLOCK, D_ANTICLOCK]

EXCEPTION_ACTION_NOT_IN_ACTIONS='The specified action is neither swipe or pinch'
EXCEPTION_DIRECTION_NOT_IN_DIRECTIONS='The specified direction is invalid'
EXCEPTION_FINGER_COUNT_OUT_OF_RANGE='The specified finger count is out of range'

BASE_XDOTOOL_KEYSTROKE='xdotool key '


class Gesture:
    def __init__(self, action, direction, fingers):
        if not action in ACTIONS:
            raise ValueError(EXCEPTION_ACTION_NOT_IN_ACTIONS)
        if not direction in DIRECTIONS:
            raise ValueError(EXCEPTION_DIRECTION_NOT_IN_DIRECTIONS)
        if not fingers in [2,3,4]:
            raise ValueError(EXCEPTION_FINGER_COUNT_OUT_OF_RANGE)
        self.action=action
        self.direction=direction
        self.fingers=fingers

    def build_gesture_string(self, command):
        gesture_string=' '.join([GESTURE_PREFIX, self.action, self.direction, str(self.fingers), command])
        return gesture_string

    def __repr__(self):
        return ' '.join([str(self.fingers), 'fingers', self.action, self.direction])

    def __str__(self):
        return self.__repr__()

GESTURES_POSSIBLE=[
    Gesture(ACTION_PINCH, D_IN, 2),
    Gesture(ACTION_PINCH, D_OUT, 2),
    Gesture(ACTION_PINCH, D_CLOCK, 2),
    Gesture(ACTION_PINCH, D_ANTICLOCK, 2),
    Gesture(ACTION_SWIPE, D_UP, 3),
    Gesture(ACTION_SWIPE, D_DOWN, 3),
    Gesture(ACTION_SWIPE, D_LEFT, 3),
    Gesture(ACTION_SWIPE, D_RIGHT, 3),
    Gesture(ACTION_SWIPE, D_RIGHT_UP, 3),
    Gesture(ACTION_SWIPE, D_RIGHT_DOWN, 3),
    Gesture(ACTION_SWIPE, D_LEFT_UP, 3),
    Gesture(ACTION_SWIPE, D_LEFT_DOWN, 3),
    Gesture(ACTION_PINCH, D_IN, 3),
    Gesture(ACTION_PINCH, D_OUT, 3),
    Gesture(ACTION_PINCH, D_CLOCK, 3),
    Gesture(ACTION_PINCH, D_ANTICLOCK, 3),
    Gesture(ACTION_SWIPE, D_UP, 4),
    Gesture(ACTION_SWIPE, D_DOWN, 4),
    Gesture(ACTION_SWIPE, D_LEFT, 4),
    Gesture(ACTION_SWIPE, D_RIGHT, 4),
    Gesture(ACTION_SWIPE, D_RIGHT_UP, 4),
    Gesture(ACTION_SWIPE, D_RIGHT_DOWN, 4),
    Gesture(ACTION_SWIPE, D_LEFT_UP, 4),
    Gesture(ACTION_SWIPE, D_LEFT_DOWN, 4),
    Gesture(ACTION_PINCH, D_IN, 4),
    Gesture(ACTION_PINCH, D_OUT, 4),
    Gesture(ACTION_PINCH, D_CLOCK, 4),
    Gesture(ACTION_PINCH, D_ANTICLOCK, 4)
]

# initialize empty gesture:command dict
gestures_list = fh.get_gesture_dict()

def build_xdotool_keystroke(keys):
    command=BASE_XDOTOOL_KEYSTROKE
    for key in keys:
        if keys.index(key) == 0:
            command+=key
        else:
            command+='+'+key
    return command

def get_gesture(gesture):
    return gestures_list.get(gesture, '')

def add_gesture(gesture, command):
    if command == "":
        remove_gesture(gesture)
        return
    gestures_list[str(gesture)] = command
    fh.update_element(str(gesture), command)

def remove_gesture(gesture):
    gestures_list[str(gesture)] = ''
    fh.remove_element(str(gesture))
