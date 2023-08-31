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

    def calculate(self, setpoint, input1, input2):
        error = setpoint - (input1 + input2)
        self.error_sum += error
        error_diff = error - self.last_error

        output = (self.kp * error) + (self.ki * self.error_sum) + (self.kd * error_diff)

        self.last_error = error

        return output


class PIDNode(NodeBase):
    def __init__(self, name):
        super(PIDNode, self).__init__(name)
        self.bWorking = None
        self.pid = None
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)

        self.KP = self.createInputPin('KP', 'FloatPin')
        self.KI = self.createInputPin('KI', 'FloatPin')
        self.KD = self.createInputPin('KD', 'FloatPin')

        self.Setpoint1 = self.createInputPin('Setpoint1', 'FloatPin')
        self.Setpoint2 = self.createInputPin('Setpoint2', 'FloatPin')

        self.FeedBack1 = self.createInputPin('FeedBack1', 'FloatPin')
        self.FeedBack2 = self.createInputPin('FeedBack2', 'FloatPin')

        self.Result = self.createOutputPin("result", "FloatPin")

        self.out = self.createOutputPin("OUT", 'ExecPin')

        self.val = 0

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
            control = self.pid.calculate(self.Setpoint1.getData(), self.val, self.val)
            self.val += 0.02
            print("Val=" + str(self.val))
            print("Control=" + str(control))
            self.Result.setData(self.val)

            time.sleep(1)

    def stop(self, *args, **kwargs):
        self.bWorking = False

    def start(self, *args, **kwargs):
        self.bWorking = True

        kp = self.KP.getData()
        ki = self.KI.getData()
        kd = self.KD.getData()

        self.pid = PIDController(0.5, 0.2, 0.1)
        self.val = 1
