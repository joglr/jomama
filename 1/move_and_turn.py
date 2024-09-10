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



        self.neutral_ambient, self.right_min, self.left_min = self._calibrate_ambient_2()

        # this will maybe also have some info about position, possibly

    def _follow_line(self):

        NEUTRAL_AMBIENT = self.neutral_ambient
        TURN_AMPLIFY = 2
        FACTOR_AMPLIFY_DARK = 1

        while True:
            current_ambient = self.drive_sensor.ambient()
            difference_neutral = current_ambient - NEUTRAL_AMBIENT

            dark = difference_neutral < 0
            if dark:
                self.drivebase.drive(speed=30, 
                                     turn_rate=difference_neutral * TURN_AMPLIFY * FACTOR_AMPLIFY_DARK)
            else:
                self.drivebase.drive(speed=30, 
                                     turn_rate=difference_neutral * TURN_AMPLIFY)
                
            if self._check_intersection():
                
                #self._prepare_for_intersection()
                self._next_instruction()

            time.sleep(0.1)
    
    def _check_intersection(self):
        if self.left_sensor.ambient() <= self.left_min or self.right_sensor.ambient() <= self.right_min:
            self.beeper.speaker.beep()
            return True
        
    def _next_instruction(self):
        instruction = next(self.instructions)

        if instruction == 'left':
            self._turn_left()
            self.neutral_ambient, self.right_min, self.left_min = self._calibrate_ambient_2()
        elif instruction == 'right':
            self._turn_right()
            self.neutral_ambient, self.right_min, self.left_min = self._calibrate_ambient_2()
        elif instruction == 'straight':
            self._go_straight()
            self.neutral_ambient, self.right_min, self.left_min = self._calibrate_ambient_2()
        elif instruction == 'turn':
            self._turn_around()
            self.neutral_ambient, self.right_min, self.left_min = self._calibrate_ambient_2()
        

    def _turn_right(self):
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(3.5)
        self.drivebase.drive(speed=0, turn_rate=30)
        time.sleep(3)

    def _turn_left(self):
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(4.5)
        self.drivebase.drive(speed=0, turn_rate=-30)
        time.sleep(3)

    def _go_straight(self):
        self.drivebase.drive(speed=30, turn_rate=0)
        time.sleep(3)

    def _turn_around(self):
        self.drivebase.drive(speed=-20, turn_rate=0)
        time.sleep(5)
        self.drivebase.drive(speed=0, turn_rate=-30)
        time.sleep(6.2)

    def find_ambient(self):
        ambients = []
        
        for i in range(100):
            ambients.append(self.drive_sensor.ambient())
            time.sleep(0.01)

        return sum(ambients) / len(ambients)
    

    def _calibrate_ambient(self):

        # turns left and measures

        self.drivebase.drive(speed=0, turn_rate=-20)
        time.sleep(1)
        self.drivebase.drive(speed=0, turn_rate=0)
        light = self.find_ambient()
        self.drivebase.drive(speed=0, turn_rate=20)
        time.sleep(1)


        # turns right and measure

        self.drivebase.drive(speed=0, turn_rate=20)
        time.sleep(1)
        self.drivebase.drive(speed=0, turn_rate=0)
        dark = self.find_ambient()
        self.drivebase.drive(speed=0, turn_rate=-20)
        time.sleep(1)

        return (light + dark) / 2
    

    def _calibrate_ambient_2(self):
        
        ambients = []
        right_ambient = []
        left_ambient = []

        self.drivebase.drive(speed=0, turn_rate=-20)
        time.sleep(1.5)

        self.drivebase.drive(speed=0, turn_rate=20)

        for _ in range(40):
            ambients.append(self.drive_sensor.ambient())
            right_ambient.append(self.right_sensor.ambient())
            left_ambient.append(self.left_sensor.ambient())
            time.sleep(3 / 40)
        
        self.drivebase.drive(speed=0, turn_rate=-20)
        time.sleep(1.5)

        differences = []
        for i in range(40 - 5):
            differences.append([ambients[i], ambients[i] - ambients[i + 5]])

        differences.sort(key=lambda x: x[1], reverse=True)

        top_5_diffs = [x[0] for x in differences[:5]]

        print(differences)

        return sum(top_5_diffs) / len(top_5_diffs), min(right_ambient), min(left_ambient)
    


    def _prepare_for_intersection(self):

        self.drivebase.drive(speed=-20, turn_rate=0)
        time.sleep(2.5)

        ambients = []

        self.drivebase.drive(speed=0, turn_rate=-20)
        time.sleep(1.5)

        self.drivebase.drive(speed=0, turn_rate=20)

        for _ in range(40):
            ambients.append(self.drive_sensor.ambient())
            time.sleep(3 / 40)

        differences = []
        for ind, i in enumerate(range(40 - 5)):
            differences.append([ind, ambients[i] - ambients[i + 5]])

        differences.sort(key=lambda x: x[1], reverse=True)

        top_5_diffs = [x[0] for x in differences[:5]]

        avg_ind = sum(top_5_diffs) / len(top_5_diffs)

        print(avg_ind)

        self.drivebase.drive(speed=0, turn_rate=-20)
        time.sleep(3 * ((37.5 - avg_ind) / 37.5))

        self.drivebase.drive(speed=20, turn_rate=0)
        time.sleep(2.5)

    def _prepare_for_intersection_2(self):

        self.drivebase.drive(speed=-20, turn_rate=0)
        time.sleep(2.5)

        neutral_ambient = self._calibrate_ambient_2()
        TURN_AMPLIFY = 2
        FACTOR_AMPLIFY_DARK = 1

        for _ in range(40):
            current_ambient = self.drive_sensor.ambient()
            difference_neutral = current_ambient - neutral_ambient

            dark = difference_neutral < 0
            if dark:
                self.drivebase.drive(speed=0, 
                                     turn_rate=difference_neutral * TURN_AMPLIFY * FACTOR_AMPLIFY_DARK)
            else:
                self.drivebase.drive(speed=0, 
                                     turn_rate=difference_neutral * TURN_AMPLIFY)
            
            time.sleep(3 / 40)

        self.drivebase.drive(speed=20, turn_rate=0)
        time.sleep(2.5)


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