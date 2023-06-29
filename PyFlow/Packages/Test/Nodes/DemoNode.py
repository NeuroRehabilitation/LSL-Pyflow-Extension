from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from pylsl import StreamInlet, resolve_streams
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

class DemoNode(NodeBase):
    def __init__(self, name):
        super(DemoNode, self).__init__(name)
        self.out = self.createOutputPin("OUT", 'ExecPin')
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
        self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)
        self.Info = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Single)
        self.Info.enableOptions(PinOptions.AllowAny)
        self.inlets = []
        self.bWorking = False
        self.headerColor = FLOW_CONTROL_COLOR

        self.start = time.time()
        self.counter=0

    def Tick(self, delta):
        super(DemoNode, self).Tick(delta)
        if self.bWorking:
            self.counter=self.counter+1
            if time.time()-self.start>1:
                print("loops in one second:"+str(self.counter))
                self.counter = 0
                self.start = time.time()

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addOutputDataType('AnyPin')
        helper.addOutputDataType('StringPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Multi)
        helper.addOutputStruct(StructureType.Array)
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

    def stop(self, *args, **kwargs):
        self.bWorking = False


    def start(self, *args, **kwargs):

        self.bWorking = True

    @staticmethod
    def category():
        return 'FlowControl'


