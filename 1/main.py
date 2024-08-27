#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.

# Input Parameters

target = [50, 50]
target_angle = 50
speed = 200

# Setup
# Create your objects here.
ev3 = EV3Brick()
ev3.speaker.beep()

c = Motor(Port.C)
b = Motor(Port.B)


# def move_to_target(target, target_angle):





"""
100 centimeters = 8.5 rotations
"""

def centimeters_to_degrees(centimeters):
    return (centimeters / 100) * (8.5) * 360



def rotate(degrees):
    factor = 1.884
    c.run_target(speed, degrees * factor, wait=False)
    b.run_target(speed, -degrees * factor, wait=False)

def move_forward(distance):
  c.run_target(speed, centimeters_to_degrees(distance), wait=False)
  b.run_target(speed, centimeters_to_degrees(distance), wait=False)

# rotate(360)
rotate(-360)

ev3.speaker.beep(1000, 500)

"""
We need to be able to turn exactly. So we need to know how many degrees we need to turn to get to the target angle.

We can either go the manhatten way or the euclidean way to the target.



"""
