from vexcode import Color

# Looks
def print(text):
    """
    Print
    Prints values or text in the Print Console.

    brain.print("Hello")
    How To Use
    The brain.print(“HELLO”) command will print data (words and numbers) to the Print Console. All new projects will begin printing on the first line of the Print Console.

    Examples
    This example will print VEX. When printing numbers or text, they must be surrounded with quotation marks (either single (‘) or double (“) quotation marks will work).

    brain.print("VEX")
    This example will also print VEX. Notice that since a variable is within the brain.print() command, the variable does not have to be enclosed with parentheses.

    my_variable = "VEX"
    brain.print(my_variable)
    """
    return

def clear():
    """
    Clear
    Clears all the rows in the Print Console.

    brain.clear()
    How To Use
    The brain.clear command will clear all of the rows in the Print Console.

    Example
    This project will print Hello for one second and then clear rows in the Print Console before printing Goodbye.

    brain.print("Hello")
    wait(1, SECONDS)
    brain.clear()
    brain.print("Goodbye")
    """
    return

def new_line():
    """
    New Line
    Sets the cursor to a new line in the Print Console.

    brain.new_line()
    How To Use
    The brain.new_line() command will set the cursor to the next row in the Print Console.

    Example
    This project will print Drive, then on the next line in the display, it will print Forward.

    brain.print("Drive")
    brain.new_line()
    brain.print("Forward")
    """
    return

def set_print_color(COLOR: Color):
    """
    Set Print Color
    Sets the color of the text printed to the Print Console.

    brain.set_print_color(BLACK)
    How To Use
    Choose the color of the text to be printed:

    BLACK
    RED
    GREEN
    BLUE
    Example
    This example will print GO! in green, and STOP! in red to the Print Console.

    set_print_color(GREEN)
    brain.print("GO!")
    set_print_color(RED)
    brain.print("STOP!")
    """
    return

# Sensing

def timer_reset():
    """
    Reset Timer
    Resets the Brain's timer.

    brain.timer_reset()
    How To Use
    The brain's timer begins at the beginning of each project. The brain.timer_reset() function is used to reset the timer back to 0 seconds.

    Example
    This project has the Drivetrain drive forward while the timer in the Brain is less than five seconds. The brain.timer_reset() command is used at the beginning of the project to reset the Brain’s timer.

    brain.timer_reset()
    while brain.timer_time(SECONDS) < 5:
        wait(5,MSEC)
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    A wait command needs to be used with loops.

    Notice how the if statement contains a colon at the end - this indicates to Python that a block of statements follows
    """
    return

def timer_time(SECONDS):
    """
    Timer Value
    Reports the value of the Brain's timer in seconds.

    brain.timer_time(SECONDS)
    How To Use
    The timer starts at zero seconds when the project starts, and returns the timer's value as a decimal value.

    brain.timer_time() can be assigned to variables, be used in boolean expressions, or be used in other commands that take numerical values as a parameter.

    Example
    This project has the Drivetrain drive forward while the timer in the Brain is less than five seconds. The brain.timer_reset() command is used at the condition in the While loop.

    brain.timer_reset()
    while brain.timer_time(SECONDS) < 5:
        wait(5,MSEC)
        drivetrain.drive(FORWARD)
    drivetrain.stop()
    A wait command needs to be used with loops.

    Notice how the while statement contains a colon at the end - this indicates to Python that a block of statements follows
    """
    return
