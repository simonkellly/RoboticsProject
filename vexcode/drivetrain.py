from vexcode import Direction, Units

# Drivetrain
def drive(DIRECTION: Direction):
    """
    Drive
    Moves the Drivetrain forever in the direction specified inside the parentheses.

    drivetrain.drive(DIRECTION)
    How To Use
    The drivetrain.drive() command will run the Drivetrain forever, until a new drivetrain command is used, or the project is stopped.

    The default velocity for drivetrain.drive() is 50%.

    Examples
    This command will move the Drivetrain forever forward.

    drivetrain.drive(FORWARD)
    This command will drive the Drivetrain forever backwards.

    drivetrain.drive(REVERSE)
    Notice that the parameter in each command is written in capitalized letters
    """
    return


def drive_for(DIRECTION: Direction, DISTANCE, UNITS: Units):
    """
    Drive For
    Moves the Drivetrain for a given distance.

    drivetrain.drive_for(DIRECTION, distance, UNITS)
    How To Use
    Set the distance and the direction that the Drivetrain will move by providing each of the following:

    Direction - either FORWARD or REVERSE
    Distance - a numeric value
    Units - either MM(millimeters) or INCHES
    Examples
    This command will move the Drivetrain forward for 200 millimeters.

    drivetrain.drive_for(FORWARD, 200, MM)
    This command will move the Drivetrain backwards for 150 inches.

    drivetrain.drive_for(REVERSE, 150, INCHES)
    Notice the parameter in each command is written in capitalized letters.
    """
    return


def turn(DIRECTION: Direction):
    """
    Turn
    Turns the Drivetrain forever to the right or left.

    drivetrain.turn(DIRECTION)
    How To Use
    The drivetrain.turn() command will turn the Drivetrain forever until a new drivetrain command is used, or the project is stopped.

    ##Examples

    This command will turn the Drivetrain right forever.

    drivetrain.turn(RIGHT)
    This command will turn the Drivetrain left forever.

    drivetrain.turn(LEFT)
    Notice that the parameter in each command is written in capitalized letters.
    """
    return


def turn_for(DIRECTION: Direction, ANGLE, UNITS: Units):
    """
    Turn For
    Turns the Drivetrain for a given angle.

    drivetrain.turn_for(DIRECTION, ANGLE, UNITS)
    How To Use
    Set the angle and the direction that the Drivetrain will turn by providing each of the following:

    Direction - either RIGHT or LEFT
    Angle - a numeric value
    Units - DEGREES
    Examples
    This command will turn the Drivetrain right for 90 degrees.

    drivetrain.turn_for(RIGHT, 90, DEGREES)
    This example will turn the Drivetrain left for 90 degrees.

    drivetrain.turn_for(LEFT, 90, DEGREES)
    """
    return


def turn_to_heading(ANGLE, UNITS: Units):
    """
    Turn To Heading
    Turns a Drivetrain to a specific heading(angle) using the built in Gyro sensor.

    drivetrain.turn_to_heading(ANGLE, UNITS)

    How To Use
    The drivetrain.turn_to_heading() command can be used to turn the Drivetrain to any given clockwise heading.

    Based on the current heading of the Gyro sensor, the drivetrain.turn_to_heading() command will determine which direction to turn.

    drivetrain.turn_to_heading() accepts a range of 0.00 to 359.99 degrees.

    drivetrain.turn_to_heading() can accept decimals, integers, or numeric blocks.

    Examples
    This command will turn the Drivetrain right 45 degrees

    drivetrain.turn_to_heading(45, DEGREES)
    This command will turn the Drivetrain left 45 degrees

    drivetrain.turn_to_heading(315, DEGREES)
    Note that the parameter in each command is written in capitalized letters.
    """
    return


def turn_to_rotation(ANGLE, UNITS: Units):
    """
    Turn To Rotation
    Turns a Drivetrain to a specific angle of rotation using the built in Gyro sensor.

    drivetrain.turn_to_rotation(ANGLE, DEGREES)

    How To Use
    The drivetrain.turn_to_rotation() command can be used to turn the Drivetrain to a given positive (clockwise) or negative (counter-clockwise) value.

    Based on the current rotation value of the Drivetrain, drivetrain.turn_to_rotation() will determine which direction to turn.

    drivetrain.turn_to_rotation() can accept decimals or integers.

    Examples
    This command will turn the Drivetrain to 90 degrees

    drivetrain.turn_to_rotation(90, DEGREES)
    This command will turn the Drivetrain to -45 degrees

    drivetrain.turn_to_rotation(-45, DEGREES)
    Note the parameter in each command is written in capitalized letters.
    """
    return


def stop():
    """
    Stop
    Stops the Drivetrain.

    drivetrain.stop()
    How To Use
    The drivetrain.stop() command will cause the robot to come to a complete stop. The drivetrain.stop() command does not require any parameters inside of its parenthesis.

    Example
    This example project will stops the Drivetrain after it moves forward for 3 seconds.

    drivetrain.drive(FORWARD)
    wait(3, SECONDS)
    drivetrain.stop()
    Notice the parameter in each command is written in capitalized letters.
    """
    return


def set_drive_velocity(VELOCITY, PERCENT):
    """
    Set Drive Velocity
    Sets the velocity of the Drivetrain

    drivetrain.set_drive_velocity(VELOCITY, PERCENT)
    How To Use
    The drivetrain.set_drive_velocity() command accepts a range form 0% to 100%. The default Drivetrain velocity is 50%.

    Examples
    This example project will move the Drivetrain forward for 200 millimeters at a velocity of 25%

    drivetrain.set_drive_velocity(25, PERCENT)
    drivetrain.drive_for(FORWARD, 200, MM)
    Note the parameter in each command is written in capitalized letters
    """
    return


def set_turn_velocity(VELOCITY, PERCENT):
    """
    Set Turn Velocity
    Sets the velocity of the Drivetrain's turns.

    drivetrain.set_turn_velocity(VELOCITY, PERCENT)
    How To Use
    The drivetrain.set_turn_velocity() command accepts a range from 0% to 100%. The default velocity is 50%.

    Example
    This example project will turn the Drivetrain right for 90 degrees at a velocity of 25%

    drivetrain.set_turn_velocity(25, PERCENT)
    drivetrain.turn_for(RIGHT, 90, DEGREES)
    Note that the parameter in each command is written in capitalized letters
    """
    return


def set_heading(VALUE, UNITS: Units):
    """
    Set Heading
    Sets the Drivetrain's Gyro heading value.

    drivetrain.set_heading(VALUE, UNITS)
    How To Use
    The drivetrain.set_heading() command can be used to set the Drivetrain's position to any given heading. This command can be used to reset the orientation of the Drivetrain's Gyro when the heading is set to a value of 0.

    The drivetrain.set_heading() command accepts a range of 0 to 360 degrees.
    """
    return


def set_rotation(VALUE, UNITS: Units):
    """
    Set Rotation
    Sets the drivetrain's angle of rotation.

    drivetrain.set_rotation(VALUE, UNITS)
    How To Use
    The drivetrain.set_rotation() command can be used to set the Drivetrain's angle of rotation to any given positive or negative value.
    """
    return

# Sensing


def is_done():
    """
    Drive Is Done
    Returns if the Drivetrain has completed its movement.

    drivetrain.is_done()
    How To Use
    drivetrain.is_done() is a command that returns a Boolean value. It returns true when the Drivetrain's motors have completed their movement. It returns false when the Drivetrain's motors are still moving.

    drivetrain.is_done() can be assigned to variables, be used in Boolean statements, or be used in other commands that take Boolean values as a parameter.
    """
    return True


def is_moving():
    """
    Drive Is Moving
    Reports if the Drivetrain is currently moving.

    drivetrain.is_moving()
    How To Use
    drivetrain.is_moving() returns true when the Drivetrain's motors are moving.

    drivetrain.is_moving() returns false when the Drivetrain's motors are stopped.

    The drivetrain.is_moving() function returns a true or false value. It can be called and assigned to variables, be used as a condition for control statements, or be used as a function parameter.

    Setting a variable:

    still_driving = drivetrain.is_moving()
    Using it in a control statement:

    if drivetrain.is_moving():
        brain.print("Still driving")
    Passing it to another function:

    brain.print(drivetrain.is_moving())
    """
    return True


def heading(UNITS: Units):
    """
    Drive Heading
    Returns the direction that the Drivetrain is facing by using the Gyro sensor's current angular position.

    drivetrain.heading(DEGREES)
    How To Use
    The drivetrain.heading(DEGREES) command returns a numeric value. The numerical value (the DEGREES) will increase when rotating clockwise and a decrease when rotating counter-clockwise.

    The drivetrain.heading(DEGREES) command returns a range from 0.00 to 359.99 degrees.

    drivetrain.heading(DEGREES) can be assigned to variables, be used in Boolean expressions, or be used in other commands that take numerical values as a parameter.
    """
    return 33


def rotation(UNITS: Units):
    """
    Drive Rotation
    Returns the Drivetrain's angle of rotation.

    drivetrain.rotation(DEGREES)
    How To Use
    The drivetrain.rotation(DEGREES) command reports a numeric value. It returns a positive value when the Drivetrain turns in a clockwise direction. It returns a negative value when the Drivetrain turns in a counter-clockwise direction.

    drivetrain.rotation(DEGREES) can be assigned to variables, be used in Boolean expressions, or be used in other commands that take numerical values as a parameter.
    """
    return 33
