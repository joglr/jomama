#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time


drive_sensor = LightSensor(Port.S3)
right_sensor = ColorSensor(Port.S1)
left_sensor = ColorSensor(Port.S2)


while True:


    print('Ambient')

    print(drive_sensor.ambient())

    time.sleep(1)