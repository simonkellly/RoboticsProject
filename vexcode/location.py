from vexcode import Axis, Units

# Sensing
def position(AXIS: Axis, UNITS: Units):
    """
    Position
    Reports the X or Y coordinate position of the Robot.

    location.position(AXIS, UNITS)

    How To Use
    location.position(AXIS, UNITS) returns the X or Y coordinate position of the VR Robot as a numerical value.

    location.position(AXIS, UNITS) command can be assigned to variables, be used in Boolean expressions, or be used in other commands that take numerical values as a parameter.

    Example
    This project uses the location.position(AXIS, UNITS) command to code the VR robot to move to the number 28 on the Numbered Grid World Playground. The location.position(AXIS, UNITS) command is used as a Boolean expression in this project.

    drivetrain.turn_for(RIGHT, 90, DEGREES)
    while location.position(X, MM) < 500:
        drivetrain.drive(FORWARD)
        wait(5, MSEC)
    drivetrain.stop()
    drivetrain.turn_for(LEFT,90,DEGREES)
    while location.position(Y, MM) < -500:
        drivetrain.drive(FORWARD)
        wait(5, MSEC)
    drivetrain.stop()
    """
    return 100

def position_angle(DEGREES):
    """
    Position Angle in Degrees
    Reports angle of the Robot in degrees.

    location.position_angle(DEGREES)

    How To Use
    The location.position_angle(DEGREES) command returns the current angle of the VR robot as a numerical value.

    location.position_angle(DEGREES) command can be assigned to variables, be used in Boolean expressions, or be used in other commands that take numerical values as a parameter.
    """
    return 3