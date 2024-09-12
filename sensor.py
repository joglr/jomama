#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile, Font

import time

ev3 = EV3Brick()

drive_sensor = LightSensor(Port.S3)
right_sensor = ColorSensor(Port.S1)
left_sensor = ColorSensor(Port.S2)

small_font = Font(size=12)       # 6 pixel height for text on screen
ev3.screen.set_font(small_font)   #Choose a preset font for writing next texts
ev3.screen.clear()              #Make the screen empty (all pixels white)

while True:
  drive_sensor_value = drive_sensor.ambient()
  right_sensor_value = right_sensor.ambient()
  left_sensor_value = left_sensor.ambient()
  print("Drive sensor: ", drive_sensor_value)
  print("Right sensor: ", right_sensor_value)
  print("Left sensor: ", left_sensor_value)

  ev3.screen.draw_text(72, 15, "Drive sensor: " + str(drive_sensor_value), text_color=Color.BLACK, background_color=Color.WHITE)
  ev3.screen.draw_text(72, 30, "Right sensor: " + str(right_sensor_value), text_color=Color.BLACK, background_color=Color.WHITE)
  ev3.screen.draw_text(72, 45, "Left sensor: " + str(left_sensor_value), text_color=Color.BLACK, background_color=Color.WHITE)
  time.sleep(0.5)
