from pytrinamic.evalboards import TMCLEval
from pytrinamic.ic import TMC2590
from pytrinamic.features import MotorControlModule
from pytrinamic.helpers import TMC_helpers


class TMC2590_eval(TMCLEval):
    """
    This class represents a TMC2590 Evaluation board.

    Communication is done over the TMCL commands writeDRV and readDRV. An
    implementation without TMCL may still use this class if these two functions
    are provided properly. See __init__ for details on the function
    requirements.
    """
    
    def __init__(self, connection, module_id=1):
        """
        Parameters:
            connection:
                Type: class
                A class that provides the necessary functions for communicating
                with a TMC2590. The required functions are
                    connection.writeDRV(registerAddress, value, moduleID)
                    connection.readDRV(registerAddress, moduleID, signed)
                for writing/reading to register of the TMC2590.
            module_id:
                Type: int, optional, default value: 1
                The TMCL module ID of the TMC2590. This ID is used as a
                parameter for the writeDRV and readDRV functions.
        """
        TMCLEval.__init__(self, connection, module_id)
        self.motors = [self.MotorTypeA(self, 0)]
        self.ics = [TMC2590()]

    # Use the driver controller functions for register access

    def write_register(self, register_address, value):
        return self._connection.write_drv(register_address, value, self._module_id)

    def read_register(self, register_address, signed=False):
        return self._connection.read_drv(register_address, self._module_id, signed)

    def write_register_field(self, field, value):
        return self.write_register(field[0], TMC_helpers.field_set(self.read_register(field[0]),
                                   field[1], field[2], value))

    def read_register_field(self, field):
        return TMC_helpers.field_get(self.read_register(field[0]), field[1], field[2])

    # Motion control functions

    def rotate(self, motor, value):
        self._connection.rotate(motor, value)
    
    def stop(self, motor):
        self._connection.stop(motor)
    
    def move_to(self, motor, position, velocity=None):
        if velocity and velocity != 0:
            # Set maximum positioning velocity
            self.motors[motor].set_axis_parameter(self.motors[motor].AP.MaxVelocity, velocity)
        self._connection.move(motor, position, self._module_id)

    class MotorTypeA(MotorControlModule):
        def __init__(self, eval_board, axis):
            MotorControlModule.__init__(self, eval_board, axis, self.AP)

        class AP:
            TargetPosition                 = 0
            ActualPosition                 = 1
            TargetVelocity                 = 2
            ActualVelocity                 = 3
            MaxVelocity                    = 4
            MaxAcceleration                = 5
            MaxCurrent                     = 6
            StandbyCurrent                 = 7
            PositionReachedFlag            = 8
            MeasuredSpeed                  = 29
            StepDirSource                  = 50
            StepDirFrequency               = 51
            MicrostepResolution            = 140
            Intpol                         = 160
            DoubleEdgeSteps                = 161
            ChopperBlankTime               = 162
            ConstantTOffMode               = 163
            DisableFastDecayComparator     = 164
            ChopperHysteresisEnd           = 165
            ChopperHysteresisStart         = 166
            TOff                           = 167
            SEIMIN                         = 168
            SECDS                          = 169
            smartEnergyHysteresis          = 170
            SECUS                          = 171
            smartEnergyHysteresisStart     = 172
            SG2FilterEnable                = 173
            SG2Threshold                   = 174
            SLPH                           = 175
            SLPL                           = 176
            ShortToGroundProtection        = 177
            VSense                         = 179
            smartEnergyActualCurrent       = 180
            smartEnergyStallVelocity       = 181
            smartEnergyThresholdSpeed      = 182
            SDOFF                          = 183
            RandomTOffMode                 = 184
            LoadValue                      = 206
            DrvStatusFlags                 = 208
            PowerDownDelay                 = 214
            RawMode                        = 214