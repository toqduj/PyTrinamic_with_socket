
import sys
import time
import runpy

import pytest


sys.path.insert(0, '../../../..')
from pytrinamic2.connections.connection_manager import ConnectionManager  # noqa: E402
from pytrinamic2.modules import TMCM_1617  # noqa: E402


class MockTmclInterface:
    def __init__(self):
        self._position_reached_toggle = True
        self._digital_input_toggle = True

    def __enter__(self):
        return self

    def __exit__(self, exitType, value, traceback):
        del exitType, value, traceback

    def setAxisParameter(self, type, axis, value, module_id):
        pass

    def axisParameter(self, type, axis, module_id, signed):
        if type == TMCM_1617.Motor0.AP.PositionReachedFlag:
            self._position_reached_toggle ^= True
            if self._position_reached_toggle:
                return 1
            else:
                return 0
        else:
            return 0

    def moveTo(self, axis, position, module_id):
        pass

    def rotate(self, axis, velocity, module_id):
        pass

    def digitalInput(self, x, module_id):
        self._digital_input_toggle ^= True
        if self._digital_input_toggle:
            return 1
        else:
            return 0


@pytest.mark.parametrize('example_script_path', [
    f'../TMCM_1617/TMCL/encoder_position_mode.py',
    f'../TMCM_1617/TMCL/hall_digital_input.py',
    f'../TMCM_1617/TMCL/hall_position_mode.py',
])
def test(monkeypatch, example_script_path):

    def mock_init(self, _=None):
        pass

    def mock_connect(self):
        return MockTmclInterface()

    def mock_sleep(_):
        pass

    monkeypatch.setattr(ConnectionManager, '__init__', mock_init)
    monkeypatch.setattr(ConnectionManager, 'connect', mock_connect)
    monkeypatch.setattr(time, 'sleep', mock_sleep)

    runpy.run_path(example_script_path)
