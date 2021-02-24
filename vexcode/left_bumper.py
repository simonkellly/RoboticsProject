# Sensing
def pressed():
    """
    Left Bumper pressed
    Returns if the Left Bumper is pressed.

    left_bumper.pressed()

    How To Use
    The left_bumper.pressed() command returns a Boolean value. It returns True when the Bumper is pressed and False when the Bumper is not pressed.

    left_bumper.pressed() can be assigned to variables, be used in Boolean statements, or be used in other commands that take Boolean values as a parameter.

    Example
    In this project, the left_bumper.pressed() command is used as a Boolean statement. If the Left Bumper sensor is not pressed, the Drivetrain will move forward. If the Left Bumper sensor is pressed, the Drivetrain will stop.

    while True:
            wait(5,MSEC)
            if left_bumper.pressed():
                drivetrain.stop()
            else:
                drivetrain.drive(FORWARD)
    A wait command needs to be used with loops.

    Notice how the if/else statement contains a colon at the end of each line - this indicates to Python that a block of statements follows
    """
    return True
