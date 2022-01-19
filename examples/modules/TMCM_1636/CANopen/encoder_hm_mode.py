'''
Do a homing with CANopen using the TMCM-1636 module

Created on 15.05.2020

@author: JM, ED
'''

if __name__ == '__main__':
    pass

import PyTrinamic
from PyTrinamic.connections.ConnectionManager import ConnectionManager
from PyTrinamic.modules.TMCM1636.TMCM_1636 import TMCM_1636
import time

PyTrinamic.show_info()

" choose the right bustype before starting the script "
connectionManager = ConnectionManager(" --interface kvaser_CANopen", connection_type="CANopen")
network = connectionManager.connect()

node = network.addDs402Node(TMCM_1636.getEdsFile(), 1)
module = node

" this function initializes the DS402 state machine "
node.setup_402_state_machine()

" communication area "
objManufacturerDeviceName       = module.sdo[0x1008]
objManufacturerHardwareVersion  = module.sdo[0x1009]

print()
print("Module name:        %s" % objManufacturerDeviceName.raw)
print("Hardware version:   %s" % objManufacturerHardwareVersion.raw)

" manufacturer specific area "
objMaximumCurrent             = module.sdo[0x2003]
objSwitchParameter            = module.sdo[0x2005]
objCommutationMode            = module.sdo[0x2055]
objMotorPolePairs             = module.sdo[0x2056]

" ABN encoder settings "
objEncoderDirection           = module.sdo[0x2080][1]
objEncoderSteps               = module.sdo[0x2080][2]
objEncoderInitMode            = module.sdo[0x2080][3]

objDeviceDigitalInputs        = module.sdo[0x2702]

" profile specific area "
objControlWord              = module.sdo[0x6040]
objStatusWord               = module.sdo[0x6041]
objModeOfOperation          = module.sdo[0x6060]
objActualPosition           = module.sdo[0x6064]
objTargetTorque             = module.sdo[0x6071]
objTargetPosition           = module.sdo[0x607A]
objAcceleration             = module.sdo[0x6083]
objActualVelocity           = module.sdo[0x606C]
objDesiredVelocity          = module.sdo[0x60FF]
objVelocityActualValue      = module.sdo[0x606C]
objHomingMethod             = module.sdo[0x6098]
objHomingSpeedFast          = module.sdo[0x6099][1]
objHomingSpeedsSlow         = module.sdo[0x6099][2]
objHomingAcceleration       = module.sdo[0x609A]

"""
    Define all motor configurations for the TMCM-1636.

    The configuration is based on our standard BLDC motor (QBL4208-61-04-013-1024-AT).
    If you use a different motor be sure you have the right configuration setup otherwise the script may not work.
"""
objMotorPolePairs.raw              = 4
objMaximumCurrent.raw              = 1500
objCommutationMode.raw             = 3
objEncoderSteps.raw                = 4096
objEncoderDirection.raw            = 1

print("MotorPoles:               %d" % objMotorPolePairs.raw)
print("CommutationMode:          %d" % objCommutationMode.raw)
print("Encoder_StepsPerRotation: %d" % objEncoderSteps.raw)
print("Encoder_Direction:        %d" % objEncoderDirection.raw)
print()

" setup Homing Mode (HM) "

" setup homing speed "
objHomingSpeedFast.raw = 1000
objHomingSpeedsSlow.raw = 500

" setup homing acceleration "
objHomingAcceleration.raw = 500

" reset node from fault and set it to Operation Enable state "
node.reset_from_fault()

def startHM():

    timeout = time.time() + 15
    node.state = 'READY TO SWITCH ON'
    while node.state != 'READY TO SWITCH ON':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    timeout = time.time() + 15
    node.state = 'SWITCHED ON'
    while node.state != 'SWITCHED ON':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    if objModeOfOperation.raw != 6:
        objModeOfOperation.raw = 6
    print("MODE OF OPERATION SET TO: %d" % objModeOfOperation.raw)

    timeout = time.time() + 15
    node.state = 'OPERATION ENABLED'
    while node.state != 'OPERATION ENABLED':
        if time.time() > timeout:
            raise Exception('Timeout when trying to change state')
        time.sleep(0.001)

    print(node.state)

    return

def homingRunning():
    return (objStatusWord.raw & (1 << 10)) != 0

print("enable REF switches and use default polarity ")
objSwitchParameter.raw = 0

" select one of the homing methods "
objHomingMethod.raw = 17 
#objHomingMethod.raw = 18
#objHomingMethod.raw = 19
#objHomingMethod.raw = 21
#objHomingMethod.raw = 35

startHM()

" trigger the homing process "
node.controlword = 0x001F

while not homingRunning():
    print("Homing...")
    time.sleep(0.4)

print("Actual position: %d" % objActualPosition.raw)

node.controlword = 0x000F

network.close()
print("Ready.")
