from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class Difficulty1(NodeBase):
    def __init__(self, name):
        super(Difficulty1, self).__init__(name)
        self.Const = self.createInputPin('Performance', 'FloatPin')
        self.Name = self.createInputPin('Name', 'StringPin')

        self.Max = self.createInputPin('Max', 'IntPin')
        self.Min = self.createInputPin('Min', 'IntPin')

        self.LastLine = self.createInputPin('LastValue', 'FloatPin')

        # _____Output_____#
        self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)

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
        if (self.Const.getData() is not None) and (self.Name.getData() is not None) and (
                self.Max.getData() is not None) and (self.Min.getData() is not None):

            name = self.Data.getData()
            max = self.Max.getData()
            min = self.Min.getData()
            const = self.Const.getData()




