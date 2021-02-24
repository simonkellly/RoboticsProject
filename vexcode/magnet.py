from enum import Enum
from vexcode import MagnetState

# Magnet
def energize(BOOST: MagnetState):
    """
    Energize Electromagnet
    Sets the VR Robot Electromagnet to two different modes: boost or drop.

    magnet.energize(BOOST)
    How To Use
    Enter either BOOST or DROP within the parentheses.
    BOOST: will attract a nearby magnetic object to the Electromagnet
    DROP: will release any object the Electromagnet is holding

    Example
    In the Disk Mover playground, this example will have the robot drive forward 800mm, pick up an object, and then drop the object after driving 200mm in reverse.

    drivetrain.drive_for(FORWARD, 800, MM, wait=True)
    magnet.energize(BOOST)
    drivetrain.drive_for(REVERSE, 200, MM, wait=True)
    magnet.energize(DROP)
    """
    return