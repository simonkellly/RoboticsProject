# Sensing
def pressed():
    """
    Right Bumper pressed
    Returns if the Right Bumper is pressed

    right_bumper.pressed()

    How To Use
    The right_bumper.pressed() command returns a Boolean value. It returns True when the Bumper is pressed and False when the Bumper is not pressed.

    right_bumper.pressed() can be assigned to variables, be used in Boolean statements, or be used in other commands that take Boolean values as a parameter.

    Example
    In this project, the right_bumper.pressed() command is used as a Boolean statement. If the Right Bumper sensor is not pressed, the Drivetrain will move forward. If the Right Bumper sensor is pressed, the Drivetrain will stop.

    while True:
            wait(5,MSEC)
            if right_bumper.pressed():
                drivetrain.stop()
            else:
                drivetrain.drive(FORWARD)
    A wait command needs to be used with loops.

    Notice how the if/else statement contains a colon at the end of each line - this indicates to Python that a block of statements follows
    """
    return True
