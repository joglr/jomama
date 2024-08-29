#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import math

left_sensor = ColorSensor(Port.S2)
right_sensor = ColorSensor(Port.S1)

'''while True:
  print("left: ",left_sensor.ambient(), "  right: ", right_sensor.ambient())
  time.sleep(0.4)
  print("left: ",left_sensor.color(), "  right: ", right_sensor.color())'''

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)


