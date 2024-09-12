#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# In this competition, we did a open loop robot that moves to a target point and angle.

# Input Parameters

# Left point
target = [127, 35]
target_angle = 180 - 130
speed = 200

# Center point
# target = [145, 0]
# target_angle = 180-225
# speed = 200

# Right point
target = [114, - 26]
target_angle = 180 - 60
speed = 200

# Setup
# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()

c = Motor(Port.C)
b = Motor(Port.B)


def move_to_target(target, target_angle):
  x, y = target
  hyp = ((x ** 2) + (y ** 2)) ** 0.5
  angle = math.acos(x / hyp) if hyp != 0 else 0
  angle_degrees = math.degrees(angle)

  print("Hypotenuse: ", hyp)
  print("Angle: ", angle_degrees)

  rotate(angle_degrees)
  move_forward(hyp)
  final_rotation = target_angle - angle_degrees
  if (final_rotation ** 2) ** 0.5 > 0.01:
    rotate(target_angle - angle_degrees)

"""
100 centimeters = 8.5 rotations
"""

def centimeters_to_degrees(centimeters):
    return (centimeters / 100) * (8.5 * (50 / 64)) * 360



def rotate(degrees):
    factor = 1.899
    c.run_angle(speed, degrees * factor, wait=False)
    b.run_angle(speed, -degrees * factor, wait=True)
    wait(500)


def move_forward(distance):
  c.run_angle(speed, centimeters_to_degrees(distance), wait=False)
  b.run_angle(speed, centimeters_to_degrees(distance), wait=True)

rotate(180)
move_to_target(target, target_angle)

ev3.speaker.beep(1000, 500)

"""
We need to be able to turn exactly. So we need to know how many degrees we need to turn to get to the target angle.

We can either go the manhatten way or the euclidean way to the target.



"""
