# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode VR Python Project
# 
# ------------------------------------------

# Library imports
from vexcode import *

length = 250
def step(dist,unit):
    wait(2,MSEC)
    drivetrain.drive_for(FORWARD,dist,unit)
    wait(2,MSEC)

def check_forward(dist):
    if distance.get_distance(MM)>dist and distance.get_distance(MM)<1500:
        wait(2,MSEC)
        step(length,MM)
        wait(2,MSEC)
    else:
        wait(2,MSEC)
        drivetrain.turn_for(RIGHT,90,DEGREES)
        wait(2,MSEC)
    return

def check_left(dist):
    wait(2,MSEC)
    #brain.print("checking left\n")
    drivetrain.turn_for(LEFT,90,DEGREES)

    wait(2,MSEC)
    if distance.get_distance(MM)>dist and distance.get_distance(MM)<1500:
        brain.print("nothing to the left\n")
        wait(2,MSEC)
        step(length,MM)
        wait(2,MSEC)
        return 1
    else:
        wait(2,MSEC)
        drivetrain.turn_for(RIGHT,90,DEGREES)
        brain.print("Wall to the left\n")
        wait(2,MSEC)
        return 0
    
    

def main():
    drivetrain.set_drive_velocity(100,PERCENT)
    drivetrain.set_turn_velocity(100,PERCENT)
    brain.print("start\n")
    finish = 0
    
    while finish ==0 :
        wait(2,MSEC)
        
        A = check_left(100)
        if A==0:
            wait(2, MSEC)
            check_forward(100)
            wait(2,MSEC)
        

# VR threads — Do not delete
vr_thread(main())
