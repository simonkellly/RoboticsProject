from vexcode import Color

# Sensing
def near_object():
    """
    Front Eye sensor near object
    Reports if the Front Eye sensor is close enough (within 100 mm) to an object to detect a color.

    front_eye.near_object()

    How To Use
    The front_eye.near_object() command returns a Boolean value. It returns True when the Front Eye sensor is close to an object that has detectable colors. It returns False when the Front Eye sensor isn’t close enough to an object with detectable colors.

    front_eye.near_object() can be assigned to variables, be used in Boolean statements, or be used in other commands that take Boolean values as a parameter.

    Example
    In this project, the front_eye.near_object() command is used as a Boolean statement.If the front_eye.near_object() command returns True, the Drivetrain will stop, Near an Object will be printed to the Monitor Console, and the project will stop.If the front_eye.near_object() command returns False, Not Near an Object will be continuously printed on new lines.

    while True:
            drivetrain.drive(FORWARD)
            if front_eye.near_object(): 
                drivetrain.stop()
                brain.print("Near an Object")
                stop_project()

            else:
                brain.print("Not Near an Object")
                brain.new_line()
            wait(5,MSEC)

    A wait command needs to be used with loops.

    Notice how the if/else statement contains a colon at the end of each line - this indicates to Python that a block of statements follows
    """
    return True

def detect(COLOR: Color):
    """
    Front Eye sensor color
    Returns the specific color detected by the Front Eye sensor .

    front_eye.detect(COLOR)

    How To Use
    The front_eye.detect(RED) command returns a Boolean value. It returns True when the Front Eye sensor detects the selected color. It returns False when the Front Eye sensor detects a color different from the one selected.

    Choose the color for the Front Eye sensor to detect:

    NONE
    RED
    GREEN
    BLUE
    front_eye.detect(RED) can be assigned to variables, be used in Boolean statements, or be used in other commands that take Boolean values as a parameter.

    Example
    In this project, the front_eye.detect(GREEN) command is used as a Boolean statement.If the front_eye.detect(GREEN) command returns True, Green will be printed to the Monitor Console. If the front_eye.detect(GREEN) command returns False, Not Green will be displayed in the Monitor Console.

    while True:
            drivetrain.drive(FORWARD)
            if front_eye.near_object(): 
                drivetrain.stop()
                if front_eye.detect(GREEN):
                    brain.print("Green")

                else:
                    brain.print("Not Green")
                stop_project()

            else:
                brain.print("Not Near an Object")
                brain.new_line()
            wait(5,MSEC)
    A wait command needs to be used with loops.

    Notice how the if/else statement contains a colon at the end of each line - this indicates to Python that a block of statements follows.
    """
    return True

def brightness(PERCENT):
    """
    Front Eye sensor brightness
    Returns the brightness of an object.

    front_eye.brightness(PERCENT)

    How To Use
    The front_eye.brightness(PERCENT) command returns a numerical value between 0 and 100. It returns a value in percent. White objects will report a brightness of 100%, black objects will report a brightness of 0%. All other colors will report a brightness somewhere between that range of values.

    front_eye.brightness(PERCENT) can be assigned to variables, be used in Boolean expressions, or be used in other commands that take numerical values as a parameter.
    """
    return 
