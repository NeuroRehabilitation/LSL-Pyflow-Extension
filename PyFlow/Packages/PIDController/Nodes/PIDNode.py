from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.error_sum = 0
        self.last_error = 0

    def calculate(self, setpoint, input1):
        error = setpoint - input1

        self.error_sum += error

        error_diff = error - self.last_error

        output = (self.kp * error) + (self.ki * self.error_sum) + (self.kd * error_diff)

        self.last_error = error

        return output


class PIDNode(NodeBase):
    def __init__(self, name):
        super(PIDNode, self).__init__(name)

        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)

        self.KP = self.createInputPin('KP', 'FloatPin')
        self.KI = self.createInputPin('KI', 'FloatPin')
        self.KD = self.createInputPin('KD', 'FloatPin')

        self.Timer = self.createInputPin('Timer', 'IntPin')

        self.Dif = self.createInputPin('Difficulty', 'IntPin')

        self.Setpoint = self.createInputPin('Setpoint', 'FloatPin')

        self.FeedBack = self.createInputPin('FeedBack', 'FloatPin')

        # Output
        self.NewDif = self.createOutputPin("New Difficulty", "IntPin")

        self.Result = self.createOutputPin("result", "FloatPin")

        self.Info = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Single)
        self.Info.enableOptions(PinOptions.AllowAny)

        self.out = self.createOutputPin("OUT", 'ExecPin')

        self.bWorking = None
        self.pid = None
        self.start = time.time()
        self.val = 0
        self.Difficulty = 0

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Generated from wizard'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def Tick(self, delta):
        super(PIDNode, self).Tick(delta)

        if self.bWorking:
            if time.time() - self.start >= 10:
                control = self.pid.calculate(self.Setpoint.getData(), self.val)

                self.Difficulty += int(control)

                if self.Difficulty < 1:
                    self.Difficulty = 1
                if self.Difficulty > 5:
                    self.Difficulty = 5

                print("Val =" + str(self.val))
                print("Control =" + str(control))
                print("Difficulty =" + str(self.Difficulty))

                info = {"Time": time.time(), "SetPoint": self.Setpoint.getData(), "KP": self.KP.getData(),
                        "KI": self.KI.getData(), "KD": self.KD.getData(), "Timer": self.Timer.getData(),
                        "FeedBack": self.FeedBack.getData(), "Output": control}

                self.Info.setData(info)

                self.NewDif.setData(self.Difficulty)
                self.val = self.FeedBack.getData()
                self.Result.setData(self.val)
                self.start = time.time()
                self.out.call()

    def stop(self, *args, **kwargs):
        self.bWorking = False

    def start(self, *args, **kwargs):
        self.bWorking = True

        self.Difficulty = self.Dif.getData()
        kp = self.KP.getData()
        ki = self.KI.getData()
        kd = self.KD.getData()

        self.pid = PIDController(kp, ki, kd)
        self.val = self.FeedBack.getData()
