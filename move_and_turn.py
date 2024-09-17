#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (
    Motor,
    TouchSensor,
    ColorSensor,
    InfraredSensor,
    UltrasonicSensor,
    GyroSensor,
)
from pybricks.nxtdevices import LightSensor
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import time


class MazeRobot:
    def __init__(self, instructions):
        self.drive_sensor = LightSensor(Port.S3)
        self.right_sensor = ColorSensor(Port.S1)
        self.left_sensor = ColorSensor(Port.S2)

        self.left_motor = Motor(Port.A)
        self.right_motor = Motor(Port.C)

        self.left_min = 5
        self.right_min = 5

        self.brick = EV3Brick()

        self.orientation = 0

        self.drivebase = DriveBase(
            self.left_motor, self.right_motor, wheel_diameter=32, axle_track=135
        )

        self.instructions = iter(instructions)
        self.neutral_ambient = self.find_ambient()

    def drive(self, *args, **kwargs):
        if "speed" not in kwargs:
            kwargs["speed"] = 0
        else:
            kwargs["speed"] = -kwargs["speed"]

        self.drivebase.drive(*args, **kwargs)

    def follow_line(self):
        NEUTRAL_AMBIENT = self.neutral_ambient
        TURN_AMPLIFY = 8
        FACTOR_AMPLIFY_DARK = 1.5

        while True:
            current_ambient = self.drive_sensor.ambient()
            difference_neutral = current_ambient - NEUTRAL_AMBIENT

            self.brick.screen.draw_text(
                72,
                15,
                "Angle: " + str(self.orientation),
                text_color=Color.BLACK,
                background_color=Color.WHITE,
            )

            dark = difference_neutral < 0
            if dark:
                self.drive(
                    speed=(1 / (abs(difference_neutral) + 1)) * 50,
                    turn_rate=-difference_neutral * TURN_AMPLIFY * FACTOR_AMPLIFY_DARK,
                )
            else:
                self.drive(
                    speed=(1 / (abs(difference_neutral) + 1)) * 50,
                    turn_rate=-difference_neutral * TURN_AMPLIFY,
                )

            if self.check_intersection():
                self.next_instruction()

            time.sleep(0.05)

    def check_intersection(self):
        lr, lg, lb = self.left_sensor.rgb()
        rr, rg, rb = self.right_sensor.rgb()
        lmean = (lr + lg + lb) / 3
        rmean = (rr + rg + rb) / 3

        if lmean < self.left_min or rmean < self.right_min:
            self.brick.speaker.beep()
            return True

    def next_instruction(self):
        instruction_to_degrees = {"left": 90, "right": 270, "up": 0, "down": 180}
        degrees_to_instruction = {90: "left", 270: "right", 0: "straight", 180: "turn"}
        instruction_str = next(self.instructions)

        degrees = instruction_to_degrees[instruction_str]
        turn_degrees = ((degrees + self.orientation) + 360) % 360
        instruction = degrees_to_instruction[turn_degrees]

        if instruction == "left":
            self.add_orientation(-90)
            self.turn_left()

        elif instruction == "right":
            self.add_orientation(90)
            self.turn_right()

        elif instruction == "straight":
            self.go_straight()

        elif instruction == "turn":
            self.add_orientation(180)
            self.turn_around()

    def add_orientation(self, num):
        self.orientation += num + 360
        self.orientation %= 360

    def turn_right(self):
        self.drive(speed=30, turn_rate=0)
        time.sleep(3.5)
        self.drive(speed=0, turn_rate=-40)
        time.sleep(3)
        self.drive(speed=30, turn_rate=0)
        time.sleep(0.5)

    def turn_left(self):
        self.drive(speed=30, turn_rate=0)
        time.sleep(3.5)
        self.drive(speed=0, turn_rate=40)
        time.sleep(3)
        self.drive(speed=30, turn_rate=0)
        time.sleep(0.5)

    def go_straight(self):
        self.drive(speed=30, turn_rate=0)
        time.sleep(3)

    def turn_around(self):
        self.drive(speed=-20, turn_rate=0)
        time.sleep(3)
        self.drive(speed=0, turn_rate=40)
        time.sleep(6.3)
        self.drive(speed=-20, turn_rate=0)
        time.sleep(3.5)

    def find_ambient(self):
        ambients = []

        for i in range(100):
            ambients.append(self.drive_sensor.ambient())
            time.sleep(0.01)

        return sum(ambients) / len(ambients)

    def calibrate_ambient(self):
        # turns left and measures

        self.drive(speed=0, turn_rate=20)
        time.sleep(1)
        self.drive(speed=0, turn_rate=0)
        light = self.find_ambient()
        self.drive(speed=0, turn_rate=-20)
        time.sleep(1)

        # turns right and measure

        self.drive(speed=0, turn_rate=-20)
        time.sleep(1)
        self.drive(speed=0, turn_rate=0)
        dark = self.find_ambient()
        self.drive(speed=0, turn_rate=20)
        time.sleep(1)

        return (light + dark) / 2

    def calibrate_ambient_2(self):
        ambients = []
        right_ambient = []
        left_ambient = []

        self.drive(speed=0, turn_rate=20)
        time.sleep(1.5)

        self.drive(speed=0, turn_rate=-20)

        for _ in range(40):
            ambients.append(self.drive_sensor.ambient())
            right_ambient.append(self.right_sensor.ambient())
            left_ambient.append(self.left_sensor.ambient())
            time.sleep(3 / 40)

        self.drive(speed=0, turn_rate=20)
        time.sleep(1.5)

        differences = []
        for i in range(40 - 5):
            differences.append([ambients[i], ambients[i] - ambients[i + 5]])

        differences.sort(key=lambda x: x[1], reverse=True)

        top_5_diffs = [x[0] for x in differences[:5]]

        print(differences)

        return (
            sum(top_5_diffs) / len(top_5_diffs),
            min(right_ambient),
            min(left_ambient),
        )


def main():
    new_instructions = ["up", "up", "down"]

    maze_robot = MazeRobot(new_instructions)

    maze_robot.follow_line()


if __file__ == "__main__":
    main()
