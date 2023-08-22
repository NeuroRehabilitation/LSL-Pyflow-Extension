from datetime import datetime

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

class CreateDict2(NodeBase):
    def __init__(self, name):
        super(CreateDict2, self).__init__(name)
        # ____Input____#
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)

        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        #_____Output_____#
        self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('AnyPin')
        helper.addInputDataType('AnyPin')
        helper.addOutputDataType('AnyPin')
        helper.addInputStruct(StructureType.Array)
        helper.addInputStruct(StructureType.Array)
        helper.addOutputStruct(StructureType.Array)
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
            self.Send.setData(self.Data)
