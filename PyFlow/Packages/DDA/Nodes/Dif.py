from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class Dif(NodeBase):
    def __init__(self, name):
        super(Dif, self).__init__(name)

        self.Input = self.createInputPin('Input', 'IntPin')
        self.Output = self.createOutputPin('Output', 'IntPin')



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
        self.Output.setData(self.Input.getData())


