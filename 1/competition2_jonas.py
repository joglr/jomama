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


# Create your objects here.
ev3 = EV3Brick()

speed = 300
turn_speed = 100

# Write your program here.
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
left_sensor = ColorSensor(Port.S2)
right_sensor = ColorSensor(Port.S1)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

while True:
  left_ambient = left_sensor.ambient()
  right_ambient = right_sensor.ambient()

  if left_ambient + 1 < right_ambient:
    print(left_ambient, " < ", right_ambient)
    robot.drive(turn_speed, - turn_speed)
    wait(100)
  elif left_ambient > right_ambient + 1:
    print(left_ambient," > ",right_ambient)
    robot.drive(turn_speed, turn_speed)
    wait(100)
  else:
    print("going straight")
    robot.drive(speed, 0)
