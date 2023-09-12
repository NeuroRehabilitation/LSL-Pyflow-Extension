import json
import os
from datetime import datetime

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

def save_json(file_name, data, time):

    dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
    filename = file_name+"-"+dt_string
    with open("Data/"+ filename + ".txt", "a") as outfile:
        json.dump(data, outfile)
        outfile.write('\n')


class Skill1(NodeBase):
    def __init__(self, name):
        super(Skill1, self).__init__(name)

        self.StreamName = self.createInputPin('StreamName', 'StringPin')
        self.Name = self.createInputPin('Name', 'StringPin')

        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.SB = self.createInputPin('SuperBad', 'FloatPin')
        self.B = self.createInputPin('Bad', 'FloatPin')
        self.M = self.createInputPin('Medium', 'FloatPin')
        self.G = self.createInputPin('Good', 'FloatPin')
        self.SG = self.createInputPin('SuperGood', 'FloatPin')

        self.Target = self.createInputPin('Difficulty', 'FloatPin')
        self.startTimer = time.time()
        self.now = datetime.now()

        self.Performance = self.createOutputPin('Performance', 'FloatPin')

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

    def compute(self, *args, **kwargs):

        if self.Data.getData() is not None:
            data = self.Data.getData()
            if len(data) != 0:
                stream = self.StreamName.getData()
                name = self.Name.getData()

                if data is dict():

                    if data.keys() is not None:

                        if len(data[stream]) != 0:

                            lastvalue = data[stream][name][-1]
                            sb = self.SB.getData()
                            b = self.B.getData()
                            m = self.M.getData()
                            g = self.G.getData()
                            sg = self.SG.getData()

                            target = self.Target.getData()

                            if sb >= lastvalue:
                                target -= 2

                            if b >= lastvalue:
                                target -= 1

                            if m >= lastvalue:
                                print()

                            if g >= lastvalue:
                                target += 1

                            if sg >= lastvalue:
                                target += 2

                            if target > 5:
                                target = 5

                            if target < 1:
                                target = 1
                            info = {"Skill Name": name, "Skill Value": lastvalue, "Difficulty": self.Target.getData(), "Results": target, "Super Bad": sb, "Bad": b, "Medium": m, "Good": g, "Super Good": sg}
                            save_json(name, info,self.now)

                            self.Performance.setData(target)
                            print("please work im tired ")
                            self.outExec.call()
