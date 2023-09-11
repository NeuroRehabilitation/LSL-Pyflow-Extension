import json
import os

import numpy as np
import math

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

        output = (self.kp * error) + (self.ki * (self.error_sum / time_delta)) + (self.kd * (error_diff / time_delta))

        self.last_error = error

        return output


def save_json(file_name, data):
    print(os.getcwd())
    with open("Data/"+file_name + ".txt", "a") as outfile:
        json.dump(data, outfile)
        outfile.write('\n')


class PIDNode(NodeBase):
    def __init__(self, name):
        super(PIDNode, self).__init__(name)

        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)

        self.Name = self.createInputPin('Name', 'StringPin')

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

        self.Info = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Multi)
        self.Info.enableOptions(PinOptions.AllowAny)

        self.out = self.createOutputPin("OUT", 'ExecPin')

        self.bWorking = None
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

        if self.bWorking:
            if time.time() - self.start >= self.Timer.getData():
                control = self.pid.calculate(self.Setpoint.getData(), self.val, self.Timer.getData())

                self.Difficulty += control

                if self.Difficulty < 1:
                    self.Difficulty = 1
                if self.Difficulty > 5:
                    self.Difficulty = 5

                info = {"Time": time.time()-self.startTimer, "SetPoint": self.Setpoint.getData(), "KP": self.KP.getData(),
                        "KI": self.KI.getData(), "KD": self.KD.getData(), "Timer": self.Timer.getData(),
                        "FeedBack": self.FeedBack.getData(), "Output": control, "Difficulty": math.ceil(self.Difficulty), "Difficulty2": self.Difficulty, "Difficulty3": round(self.Difficulty)}
                print("Output = "+str(control))

                self.Info.setData(info)
                save_json(self.Name.getData()+"-"+str(self.startTimer), info)
                self.NewDif.setData(round(self.Difficulty))
                self.val = self.FeedBack.getData()
                self.Result.setData(self.val)
                self.start = time.time()


    def stop(self, *args, **kwargs):
        self.bWorking = False

    def start(self, *args, **kwargs):

        self.bWorking = True
        self.startTimer = time.time()
        self.Difficulty = self.Dif.getData()
        kp = self.KP.getData()
        ki = self.KI.getData()
        kd = self.KD.getData()

        self.pid = PIDController(kp, ki, kd)
        self.val = self.FeedBack.getData()
        self.out.call()

