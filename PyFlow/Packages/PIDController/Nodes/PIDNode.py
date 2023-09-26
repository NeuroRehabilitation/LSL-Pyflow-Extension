import json

from datetime import date, datetime
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

    def calculate(self, setpoint, input1, time_delta):
        error = setpoint - input1

        self.error_sum += error

        error_diff = error - self.last_error

        output = (self.kp * error) + (self.ki * self.error_sum) + (self.kd * (error_diff/time_delta))

        self.last_error = error

        return output


def save_json(file_name, data, time):
    dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
    filename = dt_string + "-" + file_name
    with open("Data/" + filename + ".txt", "a") as outfile:
        json.dump(data, outfile)
        outfile.write('\n')


class PIDNode(NodeBase):
    def __init__(self, name):
        super(PIDNode, self).__init__(name)

        self.default = None
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.ActionPin = self.createInputPin("Action", 'ExecPin', None, self.Action)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)

        self.Name = self.createInputPin('Name', 'StringPin')

        self.KP = self.createInputPin('KP', 'FloatPin')
        self.KI = self.createInputPin('KI', 'FloatPin')
        self.KD = self.createInputPin('KD', 'FloatPin')

        self.Timer = self.createInputPin('Timer', 'FloatPin')

        self.Default = self.createInputPin('Default', 'FloatPin')

        self.Max = self.createInputPin('Max', 'FloatPin')

        self.Min = self.createInputPin('Min', 'FloatPin')

        self.Setpoint = self.createInputPin('Set point', 'FloatPin')

        self.Performance = self.createInputPin('Performance', 'AnyPin', structure=StructureType.Multi)
        self.Performance.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Performance.disableOptions(PinOptions.SupportsOnlyArrays)

        # Output
        self.Result = self.createOutputPin("Result", "FloatPin")

        self.Control = self.createOutputPin("Control", "FloatPin")

        self.Info = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Multi)
        self.Info.enableOptions(PinOptions.AllowAny)

        self.now = datetime.now()

        self.Begin_Out = self.createOutputPin("Start", 'ExecPin')
        self.End_Out = self.createOutputPin("Stop", 'ExecPin')

        self.bWorking = None
        self.receivedNewValue = False
        self.pid = None
        self.startTimer = time.time()
        self.start = time.time()
        self.val = 0
        self.Difficulty = 0.0

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
        if self.bWorking and self.receivedNewValue:

            for performance in self.val:
                control = self.pid.calculate(self.Setpoint.getData(), performance, self.Timer.getData())

                max = self.Max.getData()
                min = self.Min.getData()

                self.default += control

                if max >= min:
                    if max < self.default:
                        self.default = max

                    elif min > self.default:
                        self.default = min
                else:
                    if max > self.default:
                        self.default = max

                    elif min < self.default:
                        self.default = min

                info = {"Time": time.time() - self.startTimer, "SetPoint": self.Setpoint.getData(),
                        "KP": self.KP.getData(),
                        "KI": self.KI.getData(), "KD": self.KD.getData(), "Timer": self.Timer.getData(),
                        "Performance": performance, "Output": control,
                        "Percentage": control,
                        "Difficulty": self.default}

                self.Info.setData(info)

                save_json(self.Name.getData(), info, self.now)

                self.Result.setData(self.default)
                self.Control.setData(control)
                self.start = time.time()
                self.receivedNewValue = False
        self.val = self.Performance.getData()

    def Action(self, *args, **kwargs):
        self.receivedNewValue = True
        self.val = self.Performance.getData()

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.End_Out.call()

    def start(self, *args, **kwargs):

        self.bWorking = True
        self.startTimer = time.time()
        self.default = self.Default.getData()
        kp = self.KP.getData()
        ki = self.KI.getData()
        kd = self.KD.getData()

        self.pid = PIDController(kp, ki, kd)
        self.val = self.Performance.getData()
        self.Begin_Out.call()
