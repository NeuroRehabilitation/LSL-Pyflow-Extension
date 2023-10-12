import json
from datetime import datetime

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR



class DemoNode(NodeBase):
    def __init__(self, name):
        super(DemoNode, self).__init__(name)
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.actionPin = self.createInputPin("Action", 'ExecPin', None, self.action)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)

        self.Name = self.createInputPin('Name', 'StringPin')

        self.data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.startTimer = time.time()
        self.now = datetime.now()
        self.bWorking = None


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

    def action(self, *args, **kwargs):
        if self.bWorking:
            data = self.data.getData()
            for value in data["Emteq"]:
                self.save_json(self.name, value, self.now)

    def start(self, *args, **kwargs):
        self.bWorking = True
        self.name = self.Name.getData()
        self.startTimer = time.time()

    def stop(self, *args, **kwargs):
        self.bWorking = False

    def save_json(self,file_name, data, time):
        dt_string = time.strftime("%d-%m-%Y_%H-%M-%S")
        filename = dt_string + "-" + file_name
        with open("Data/" + filename + ".txt", "a") as outfile:
            json.dump(data, outfile)
            outfile.write('\n')