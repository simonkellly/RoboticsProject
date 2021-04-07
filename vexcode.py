# ------------------------------------------
# This is a module with what is essentially
# the skeleton of all the functions availible
# on the vexcode module on the VEXCODE VR
# platform. It serves to allow easier editing
# and intellisense support when writing code
# outside of the VEXCODE platform itself
# ------------------------------------------
from typing import NewType

import vexcode.brain as brain 
import vexcode.distance as distance
import vexcode.down_eye as down_eye
import vexcode.drivetrain as drivetrain
import vexcode.front_eye as front_eye
import vexcode.left_bumper as left_bumper
import vexcode.location as location
import vexcode.magnet as magnet
import vexcode.pen as pen
import vexcode.right_bumper as right_bumper

# Functions
def vr_thread(function):
    """
    VR Thread
    The VR Thread function must be used to call functions at the global level of the script.

    How To Use
    You can take any function you have made previously, and pass it to vr_thread() at the global level. Calling at least one function inside of this is required to run a program. You do not need to do all function calls with vr_thread(), just ones that are at the global level.

    If more than one vr_thread() call is made, the functions will execute in parallel.

    The functions will, in general, execute in the order they are called. However, if a function waits, it will pass execution to the next function, and continue when the other function finishes, or when the other function also waits.

    vr_thread(main())
    The functions that cause threads to switch:

    drivetrain.drive_for(FORWARD, 200, MM, wait=True)
    drivetrain.turn_for(RIGHT, 90, DEGREES, wait=True)
    drivetrain.turn_to_heading(90, DEGREES, wait=True)
    drivetrain.turn_to_rotation(90, DEGREES, wait=True)
    drivetrain.set_heading(0, DEGREES)
    drivetrain.set_rotation(0, DEGREES)
    wait(1, SECONDS)
    any user created function

    Calling a method with vr_thread() inside of another method will cause a runtime error. If you run this program:

    def main():
        vr_thread(print_hello())

    def print_hello():
        brain.print("Hello")

    vr_thread(main())
    It will give you an error that looks like this:

    Error: Traceback (most recent call last):
    line 9, in vr_thread
    line 5, in main
    NameError: name 'print_hello' is not defined
    Example 1
    We make a single function that is executed in the global space with vr_thread(). The move_drivetrain() function will make the robot move 200 mm and then print when it is done.

    def move_drivetrain():
        drivetrain.drive_for(FORWARD, 200, MM)
        brain.print("Done moving")
        brain.new_line()

    vr_thread(move_drivetrain())
    Example 2
    Now we added the move_pen_down() function. This will move the pen down and print a message. We make the call vr_thread(move_pen_down()) after the vr_thread(move_drivetrain()) call. However, because drivetrain.drive_for(FORWARD, 200, MM) makes the function wait, it will switch over to the move_pen_down() function, which will move the pen down before the robot is done moving.

    def move_drivetrain():
        drivetrain.drive_for(FORWARD, 200, MM)
        brain.print("Done moving")
        brain.new_line()

    def move_pen_down():
        pen.set_pen_color(BLACK)
        pen.move(DOWN)
        brain.print("Pen down")
        brain.new_line()

    vr_thread(move_drivetrain())
    vr_thread(move_pen_down())
    Example 3
    Moving the move_pen_down() in to the move_drivetrain() will now call it sequintially, so there will be no pen drawing since it doesn't drop until after the movement is finished. This also shows that calling functions within other functions can be done like normal function call.

    def move_drivetrain():
        drivetrain.drive_for(FORWARD, 200, MM)
        brain.print("Done moving")
        brain.new_line()
        move_pen_down()

    def move_pen_down():
        pen.set_pen_color(BLACK)
        pen.move(DOWN)
        brain.print("Pen down")
        brain.new_line()

    vr_thread(move_drivetrain())
    """
    return

# Looks
def monitor_variable(*args):
    """
    Monitor Variable
    The Monitor Variable command is used to add variables to the monitor console so that the value of the variables can be seen and monitored.

    monitor_variable("my_variable", "my_boolean", ...)
    How To Use
    To add variables to the monitor console, use the monitor_variable() command.Add the nae of the variable(s) as a string in the command. When using variables in the monitor_variable() command, they must be set as a global variable.

    Examples
    In this project, each time the VR Robot picks up a disk in the Disk Mover Playground, the value of the variable will increase by 1.

    def main():
        global diskCount
        monitor_variable("diskCount")
        while diskCount<3:
            wait(5, MSEC)
            
            drivetrain.drive(FORWARD)
            while not down_eye.near_object():
                wait(5, MSEC)
            
            magnet.energize(BOOST)
            diskCount += 1
            drivetrain.turn_for(RIGHT,180,DEGREES)
            
            drivetrain.drive(FORWARD)
            while distance.get_distance(MM)>150:
                wait(5,MSEC)
            magnet.energize(DROP)
            
            drivetrain.turn_for(LEFT,180,DEGREES)
    """
    return

def monitor_sensor(*args):
    """
    Monitor Sensor
    The Monitor sensor command is used to add sensors to the monitor console so that the sensor values can then be seen and monitored.

    monitor_sensor("sensor_name", "another_sensor_name", ...)
    How To Use
    To monitor sensor values in the monitor console, use the monitor_sensor() function by adding the identifiers of the sensors as string parameters. This function should be called at the start of the program.

    Below is the list of supported sensor identifiers:

    brain.timer_time
    drivetrain.is_done
    drivetrain.is_moving
    drivetrain.heading
    drivetrain.rotation
    left_bumper.pressed
    right_bumper.pressed
    distance.found_object
    distance.get_distance
    front_eye.near_object
    front_eye.detect
    front_eye.brightness
    down_eye.near_object
    down_eye.detect
    down_eye.brightness
    location.position
    location.position_angle
    When adding sensor identifiers to the monitor_sensor() command, they have to be added as strings - therefore enclosed with quotation marks:

    monitor_sensor("left_bumper.pressed")
    Multiple sensor identifier, separated by commas, can be added to the monitor_sensor() command:

    monitor_sensor(“distance.get_distance”, “drivetrain.rotation”, “brain.timer_time”)
    Example
    This project uses the location.position sensor identifier to show both the X and the Y position (in mm and inches) of the VR Robot as it moves in a square. It also uses the location.position_angle sensor identifier to show the angle of the VR Robot in degrees . Both of these sensor identifiers are in the motor_sensor() command.

    def main():
        monitor_sensor("location.position","location.position_angle")
        for i in range(4):
            wait(1, SECONDS)
            drivetrain.drive_for(FORWARD, 200, MM)
            drivetrain.turn_for(RIGHT, 90, DEGREES)
    """
    return

# Control
def wait(TIME, UNITS):
    """
    Wait
    Wait for a specific amount of time before moving to the next command.

    wait(TIME, UNITS)
    How To Use
    Set the amount of time to have a project wait before moving to the next command. The amount can be in seconds or milliseconds.

    Example
    This example will stop the Drivetrain after it has driven forward for three seconds.

    drivetrain.drive(FORWARD)
    wait(3, SECONDS)
    drivetrain.stop()
    Note that the parameter in each command is written in capitalized letters.
    """
    return

def stop_project():
    """
    Stop Project
    Stops a running project.

    stop_project()
    How To Use
    This command will cause a running project to stop.

    Example
    This project draws a 500 millimeter black square on the playground. The stop_project command stops the project after the square has been completed.

    pen.move(DOWN)
    pen.set_pen_color(BLACK)
    for repeat_count in range(4):
        wait(5,MSEC)
        drivetrain.drive_for(FORWARD, 500,MM)
        drivetrain.turn_for(RIGHT, 90,DEGREES)
    stop_project()
    """
    return


# Constants

# Colors
Color = NewType('Color', int)
BLACK: Color = 0
RED: Color = 1
GREEN: Color = 2
BLUE: Color = 3

# Directions
Direction = NewType('Direction', int)
FORWARD: Direction = 0
REVERSE: Direction = 1
LEFT: Direction = 2
RIGHT: Direction = 3
UP: Direction = 4
DOWN: Direction = 5

# Units
Units = NewType('Units', int)
MM: Units = 0
INCHES: Units = 1
DEGREES: Units = 2
MSEC: Units = 3
PERCENT: Units = 4

# Axis
Axis = NewType('Axis', int)
X: Axis = 0
Y: Axis = 1

# MagnetState
MagnetState = NewType('MagnetState', int)
BOOST: MagnetState = 0
DROP: MagnetState = 1