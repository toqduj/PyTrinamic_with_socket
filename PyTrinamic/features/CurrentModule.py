# Created on: 06.07.2021
# Author: LK

from PyTrinamic.features.Feature import Feature, FeatureProvider
from PyTrinamic.features.Current import Current

class CurrentModule(Current, FeatureProvider):

    class __GROUPING(Current, FeatureProvider):

        def __init__(self, parent):
            self.parent = parent

        def get_current_run(self):
            return self.parent.get_axis_parameter(self.parent.APs.RunCurrent)

        def set_current_run(self, value):
            self.parent.set_axis_parameter(self.parent.APs.RunCurrent, value)

        def get_current_standby(self):
            return self.parent.get_axis_parameter(self.parent.APs.StandbyCurrent)

        def set_current_standby(self, value):
            self.parent.set_axis_parameter(self.parent.APs.StandbyCurrent, value)

        # Properties
        run = property(get_current_run, set_current_run)
        standby = property(get_current_standby, set_current_standby)

    def __init__(self):
        self.Current = self.__GROUPING(self)