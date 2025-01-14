################################################################################
# Copyright © 2019 TRINAMIC Motion Control GmbH & Co. KG
# (now owned by Analog Devices Inc.),
#
# Copyright © 2023 Analog Devices Inc. All Rights Reserved. This software is
# proprietary & confidential to Analog Devices, Inc. and its licensors.
################################################################################

"""
Demonstration of the stallGuard feature of the TMC5160.
The sensorless stallGuard technology calculates the remaining available load for
a motor and detects incoming stalls. If such a stall is detected, the motor
driver will automatically stop to prevent damage and miscalculations.

This demo performs an interactive stallGuard initialization to set up the
sensitivity and thresholds. After that you are free to play around with this
feature.

All actions will be performed on all attached shields simultaneously, so you can
try it with multiple axes as well.
"""

import argparse
import os
import logging
import time
import sys

import msvcrt

from threading import Thread

import pytrinamic
from pytrinamic.connections.connection_manager import ConnectionManager
from pytrinamic.modules.tmc_eval_shield import TmcEvalShield
from pytrinamic.evalboards.TMC5160_shield import TMC5160_shield
from examples.evalboards.TMC5160_shield.StallGuard import StallGuard

parser = argparse.ArgumentParser(description='stallGuard demo')
parser.add_argument('-t', '--target-velocity', dest='velocity', action='store', nargs=1, type=int, default=[50000],
                    help='Target velocity for demonstration on all axes. Default: %(default)s.')
parser.add_argument('-a', '--acceleration', dest='acceleration', action='store', nargs=1, type=int, default=[1000],
                    help='Acceleration used for ramping to target velocity. Default: %(default)s.')
parser.add_argument('-c', '--current', dest='current', action='store', nargs=1, type=int, default=[5],
                    help='Current Scaler value while motor is running. Default: %(default)s.')
parser.add_argument('-e', '--threshold-velocity', dest='threshold', action='store', nargs=1, type=int, default=[1],
                    help='Velocity threshold, above which stallGuard is enabled. Default: %(default)s.')
parser.add_argument('-v', '--verbosity', dest='verbosity', action='store', nargs=1, type=int,
                    choices=[logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL],
                    default=[logging.INFO],
                    help=f'Verbosity level (default: %(default)s, {logging.DEBUG}: DEBUG, {logging.INFO}: INFO, {logging.WARNING}: WARNING, {logging.ERROR}: ERROR, {logging.CRITICAL}: CRITICAL)')

args = parser.parse_known_args()[0]
verbosity = args.verbosity[0]

logger = logging.getLogger(__name__)
logger.setLevel(verbosity)

consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(verbosity)
formatter = logging.Formatter("[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s")
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

pytrinamic.show_info()

logger.debug(f"Target velocity: {args.velocity[0]}")
logger.debug(f"Maximum acceleration: {args.acceleration[0]}")
logger.debug(f"Maximum current: {args.current[0]}")
logger.debug(f"StallGuard velocity threshold: {args.threshold[0]}")

myInterface = ConnectionManager().connect()

shields = TmcEvalShield(myInterface, TMC5160_shield).shields

# Initialize all attached shields
for shield in shields:
    logger.info(f"Initializing motor at shield {shield}.")

    logger.info("Rotating motor.")
    shield.set_axis_parameter(shield.AP.MaxCurrent, 0, args.current[0])
    shield.set_axis_parameter(shield.AP.MaxAcceleration, 0, args.acceleration[0])
    shield.rotate(0, args.velocity[0])

    StallGuard(shield, sys.argv, logger).calibrate_zero()

print("Initialization is done. You can now play around with applying loads and see if the motor stops.")
input("Press enter to continue ...")


def handle_key():
    while True:
        ch = msvcrt.getch()
        if ch == b'r':
            logger.info("Resetting stall for all shields.")
            for shield in shields:
                logger.info(f"Resetting stall for {shield}.")
                shield.set_axis_parameter(shield.AP.smartEnergyStallVelocity, 0, 0)
                time.sleep(1)
                shield.set_axis_parameter(shield.AP.smartEnergyStallVelocity, 0, args.threshold[0])
        elif ch == b'e':
            exit()


t = Thread(target=handle_key)
t.start()

# Loop over all attached shields
while True:
    status = ""
    for shield in shields:
        sgt = shield.getAxisParameter(shield.AP.LoadValue, 0)
        status = status + f"Shield: {shield}, SGT: {sgt}\n"
    status = status + """
    Keyboard shortcuts:
    'r': Reset stall on all motors.
    'e': Exit the demo."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(status)
    time.sleep(0.1)
    if not t.isAlive():
        break

# Demo exit, stop all motors
logger.info("Stopping all motors.")
for shield in shields:
    logger.info(f"Stopping motors for shield {shield}.")
    shield.stop(0)

myInterface.close()
