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
import random

ev3 = EV3Brick()

drive_sensor = LightSensor(Port.S3)
right_sensor = ColorSensor(Port.S1)
left_sensor = ColorSensor(Port.S2)

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)

robot = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)


#while True:
#    print(drive_sensor.ambient())
#    time.sleep(0.5)

prev_ambient = drive_sensor.ambient()


middle_value = 6
while True:
    cur_ambient = drive_sensor.ambient()

    #while True:
    #    print('light sensor ambient', drive_sensor.ambient())
    #    print()
    #    #print('left color:', left_sensor.color())
    #    #print('left ambient:', left_sensor.ambient())
    #    #print()
    #    #print('right color:', left_sensor.color())
    #    #print('right ambient:', left_sensor.ambient())
    #    #print()
    #    time.sleep(0.5)
    k = 5


    residual = cur_ambient - middle_value
    #residual = -1 if middle_value > cur_ambient else 1

    robot.drive(speed=60, 
                turn_rate=k*residual)
    time.sleep(0.1)

    

    if left_sensor.ambient() <= 1 or right_sensor.ambient() <= 1:
        ev3.speaker.beep()

    

while True:
    cur_ambient = drive_sensor.ambient()
    change = cur_ambient - prev_ambient

    k = 20

    robot.drive(speed=50, turn_rate=k*change)
    
    prev_ambient = cur_ambient
    time.sleep(0.2)
# only using left sensor for following


    


