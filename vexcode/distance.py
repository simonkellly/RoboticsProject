from vexcode import Units

# Sensing
def found_object():
    """
    Distance Found Object
    Reports whether the built-in Distance Sensor sees an object or surface in front of the robot.

    distance.found_object()

    How To Use
    distance.found_object() returns true when the built in Distance Sensor sees an object or surface within its field of view, and within 3000 mm of the sensor.

    distance.found_object() returns false when the built in Distance Sensor does not detect an object or surface within 3000 mm.

    The distance.found_object() function returns a true or false value. It can be called and assigned to variables, be used as a condition within control statements, or be used in functions that take boolean values as a parameter.

    Setting a variable:

    found_object = distance.found_object()
    Using it in a control statement:

    if distance.found_object():
        brain.print("Found object")
    Passing it to another function:

    brain.print(distance.found_object())
    """
    return True

def get_distance(UNITS: Units):
    """
    Distance From
    Reports the distance of the nearest object from the Distance Sensor.

    distance.get_distance(UNITS)

    How To Use
    Choose whether distance.get_distance(UNITS) is reported in millimeters or inches by replacing UNITS with either MM or INCHES as parameters.

    distance.get_distance(MM)
    distance.get_distance(INCHES)
    The distance.get_distance(UNITS) function can be called and assigned to variables, be used in comparison statements, or be used in functions that take number values as a parameter.

    Setting a variable:

    my_distance_mm = distance.get_distance(MM)
    Using it in a comparison statement:

    if distance.get_distance(INCHES) < 1:
        brain.print("Close to object")
    Passing it to another function:

    brain.print(distance.get_distance(INCHES))
    """
    return 100