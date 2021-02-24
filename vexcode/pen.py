from vexcode import Color, Direction

# Looks
def move(DIRECTION: Direction):
    """
    Set Pen Position
    Sets the position of the VR Pen.

    pen.move(DOWN)
    How To Use
    Choose the position of the VR Pen - either UP or DOWN

    UP - the pen will not draw a line on the playground

    DOWN - the pend will draw a colored line on the playground

    Example
    This project has the VR Pen draw a black line while the Drivetrain is driving forward.

    pen.move(DOWN)
    pen.set_pen_color(BLACK)
    drivetrain.drive(FORWARD)
    """
    return

def set_pen_color(COLOR: Color):
    """
    Set Pen Color
    Sets the color of the VR Pen.

    pen.set_pen_color(BLACK)
    How To Use
    Choose a color of the VR Pen:

    BLACK
    RED
    GREEN
    BLUE
    Example
    This example has the VR Pen draw a blue line while te Drivetrain is driving forward.

    pen.move(DOWN)
    pen.set_pen_color(BLUE)
    drivetrain.drive(FORWARD)
    """
    return