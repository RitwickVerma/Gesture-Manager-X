import fileIOHelper as fh

SWIPE_THRESHOLD = 'swipe_threshold'
GESTURE_TIMEOUT = 'timeout'

swipe_threshold = fh.get_element(SWIPE_THRESHOLD)
gesture_timeout = fh.get_element(GESTURE_TIMEOUT)

if swipe_threshold == '':
    swipe_threshold = "0.0"
    fh.update_element(SWIPE_THRESHOLD, swipe_threshold)

if gesture_timeout == '':
    gesture_timeout = "1.5"
    fh.update_element(GESTURE_TIMEOUT, gesture_timeout)

def set_swipe_threshold(dist):
    fh.update_element(SWIPE_THRESHOLD, str(dist))

def set_gesture_timeout(timeout):
    fh.update_element(GESTURE_TIMEOUT, str(timeout))

