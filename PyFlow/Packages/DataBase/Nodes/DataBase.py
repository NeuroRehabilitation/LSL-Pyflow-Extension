from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class DataBase(NodeBase):
    def __init__(self, name):
        super(DataBase, self).__init__(name)
        #____Input____#
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.Data = self.createInputPin('data', 'AnyPin', structure=StructureType.Dict, constraint="2")
        self.Data.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.info = self.createInputPin('Info', 'AnyPin', structure=StructureType.Single)
        self.info.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.info.disableOptions(PinOptions.SupportsOnlyArrays)

        #____Output____#
        self.out = self.createOutputPin('out', 'BoolPin')

        # ________Data Collection________#
        self.Col = dict()
        self.Stream_Names = dict()
        self.Stream_Channels = dict()

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
        self.out.setData(True)
