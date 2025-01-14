################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

import pytrinamic
from pytrinamic.connections import ConnectionManager
from pytrinamic.modules import TMCM123x_0_1
import time

pytrinamic.show_info()
# This example is using PCAN, if you want to use another connection please change the next line.
connectionManager = ConnectionManager("--interface kvaser_tmcl")
with connectionManager.connect() as myInterface: 
    module = TMCM123x_0_1(myInterface)
    motor = module.motors[0]

    # Please be sure not to use a too high current setting for your motor.

    print("Preparing parameters")
    # preparing drive settings
    motor.drive_settings.max_current = 128
    motor.drive_settings.standby_current = 0
    motor.drive_settings.boost_current = 0
    motor.drive_settings.microstep_resolution = motor.ENUM.microstep_resolution_256_microsteps
    print(motor.drive_settings)


    # preparing linear ramp settings
    motor.max_acceleration = 51200
    motor.max_velocity = 51200

    # reset actual position
    motor.actual_position = 0

    print(motor.linear_ramp)

    # start rotating motor in different directions
    print("Rotating")
    motor.rotate(51200)
    time.sleep(5)

    # stop rotating motor
    print("Stopping")
    motor.stop()

    # read actual position
    print("ActualPostion = {}".format(motor.actual_position))
    time.sleep(2)
    
    # doubling moved distance
    print("Doubling moved distance")
    motor.move_by(motor.actual_position)

    # wait till  position_reached
    while not(motor.get_position_reached()):
        print("target position motor: " + str(motor.target_position) + " actual position motor: " + str(motor.actual_position))

    time.sleep(0.2)
    print("Furthest point reached")
    print("ActualPostion motor = {}".format(motor.actual_position))

    # short delay and move back to start
    time.sleep(2)
    print("Moving back to 0")
    motor.move_to(0)

    # wait until position 0 is reached
    while not(motor.get_position_reached()):
        print("target position motor: " + str(motor.target_position) + " actual position motor: " + str(motor.actual_position))

    print("Reached Position 0")
