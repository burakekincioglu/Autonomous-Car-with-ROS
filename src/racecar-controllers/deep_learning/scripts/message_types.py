from enum import Enum

class motor:
    steering = 0.7
    speed = 0.3

class active_behavior:
    state = 4
    running = False

class message_types(int):
    PATH_PLANNING = 4
    LIDAR = 3
    OBJECT_DETECTION = 2
    LANE = 1

def behavior_callback(msg):
    active_behavior.state = int(msg.steering)
