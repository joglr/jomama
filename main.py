#!/usr/bin/env pybricks-micropython
from sokoban_new import solve
from move_and_turn_markus import MazeRobot

input_ = "worlds/board.txt"

instructions = solve(input_)

robot = MazeRobot(instructions)
robot.initialize_direction(input_)

robot.follow_line()

# #!/usr/bin/env pybricks-micropython
# from pybricks.hubs import EV3Brick
# from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
#                                  InfraredSensor, UltrasonicSensor, GyroSensor)
# from pybricks.nxtdevices import LightSensor
# from pybricks.parameters import Port, Stop, Direction, Button, Color
# from pybricks.tools import wait, StopWatch, DataLog
# from pybricks.robotics import DriveBase
# from pybricks.media.ev3dev import SoundFile, ImageFile


# right_sensor = ColorSensor(Port.S1)
# left_sensor = ColorSensor(Port.S2)

# brick = EV3Brick()

# while True:
#   left_rgb = left_sensor.rgb()
#   right_rgb = right_sensor.rgb()

#   brick.screen.draw_text(0, 0, "left: " + str(left_rgb), text_color=Color.BLACK, background_color=Color.WHITE)
#   brick.screen.draw_text(0, 30, "right: " + str(right_rgb), text_color=Color.BLACK, background_color=Color.WHITE)
#   wait(0.1)

