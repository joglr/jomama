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

class MazeRobot:

    def __init__(self, instructions):
        self.drive_sensor = LightSensor(Port.S3)
        self.right_sensor = ColorSensor(Port.S1)
        self.left_sensor = ColorSensor(Port.S2)

        self.left_motor = Motor(Port.B)
        self.right_motor = Motor(Port.C)

        self.beeper = EV3Brick()

        self.drivebase = DriveBase(self.left_motor, 
                                   self.right_motor, 
                                   wheel_diameter=55.5, 
                                   axle_track=104)
    
        self.instructions = iter(instructions)

        self.neutral_ambient = self.find_neutral_ambient()

        # this will maybe also have some info about position, possibly

    def _follow_line(self):

        NEUTRAL_AMBIENT = self.neutral_ambient
        TURN_AMPLIFY = 3
        FACTOR_AMPLIFY_DARK = 2

        while True:
            current_ambient = self.drive_sensor.ambient()
            difference_neutral = current_ambient - NEUTRAL_AMBIENT

            dark = difference_neutral < 0
            if dark:
                self.drivebase.drive(speed=40, 
                                     turn_rate=difference_neutral * TURN_AMPLIFY * FACTOR_AMPLIFY_DARK)
            else:
                self.drivebase.drive(speed=40, 
                                     turn_rate=difference_neutral * TURN_AMPLIFY)
                
            if self._check_intersection():
                self._next_instruction()

            time.sleep(0.1)
    
    def _check_intersection(self):
        if self.left_sensor.ambient() <= 1 or self.right_sensor.ambient() <= 1:
            self.beeper.speaker.beep()
            return True
        
    def _next_instruction(self):
        instruction = next(self.instructions)

        if instruction == 'left':
            self._turn_left()
        elif instruction == 'right':
            self._turn_right()
        elif instruction == 'straight':
            self._go_straight()
        elif instruction == 'turn':
            self._turn_around()
        

    def _turn_right(self):
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(3.5)
        self.drivebase.drive(speed=0, turn_rate=45)
        time.sleep(2)
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(1.5)

    def _turn_left(self):
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(3.5)
        self.drivebase.drive(speed=0, turn_rate=-45)
        time.sleep(2)
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(1.5)

    def _go_straight(self):
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(4)

    def _turn_around(self):
        self.drivebase.drive(speed=-30, turn_rate=0)
        time.sleep(3.5)
        self.drivebase.drive(speed=0, turn_rate=-45)
        time.sleep(4)

    def find_neutral_ambient(self):
        ambients = []
        
        for i in range(100):
            ambients.append(self.drive_sensor.ambient())
            time.sleep(0.04)

        return sum(ambients) / len(ambients)


new_instructions = ['left',
                    'straight',
                    'turn',
                    'right',
                    'right',
                    'straight',
                    'right',
                    'straight',
                    'turn',
                    'left',
                    'left',
                    'left',
                    'straight']

maze_robot = MazeRobot(new_instructions)

maze_robot._follow_line()