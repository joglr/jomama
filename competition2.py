#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time
import random

left_sensor = ColorSensor(Port.S2)
right_sensor = ColorSensor(Port.S1)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

ev3 = EV3Brick()

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

#robot.drive(speed=10)

while True:
  diff_ambient =  left_sensor.ambient() - right_sensor.ambient()
  k = 20

  #print("left: ",left_sensor.color(), "  right: ", right_sensor.color())
  #print("left: ",left_sensor.ambient(), "  right: ", right_sensor.ambient())
  #print("left: ",left_sensor.reflection(), "  right: ", right_sensor.reflection())

  
  if left_sensor.color() == Color.BLACK and right_sensor.color() == Color.BLACK:
    ev3.speaker.beep()

    direction = random.choice(('left', 'right', 'forward'))

    if direction == 'right':
      time.sleep(0.5)
      robot.drive(speed=0, turn_rate = 90)
      time.sleep(1)
      continue
    elif direction == 'left':
      time.sleep(0.5)
      robot.drive(speed=0, turn_rate = -90)
      time.sleep(1)
      continue
    elif direction == 'forward':
      time.sleep(1.5)
      continue

  robot.drive(speed=40, turn_rate = k * diff_ambient)
  time.sleep(0.1)

  #print("left: ",left_sensor.ambient(), "  right: ", right_sensor.ambient())
  #print("left: ",left_sensor.color(), "  right: ", right_sensor.color())





