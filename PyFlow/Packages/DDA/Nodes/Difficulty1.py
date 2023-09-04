from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class Difficulty1(NodeBase):
    def __init__(self, name):
        super(Difficulty1, self).__init__(name)

        self.Name = self.createInputPin('Name', 'StringPin')

        self.Value = self.createInputPin('Value', 'IntPin')

        self.SE = self.createInputPin('SuperEasy', 'FloatPin')
        self.E = self.createInputPin('Easy', 'FloatPin')
        self.M = self.createInputPin('Medium', 'FloatPin')
        self.H = self.createInputPin('Hard', 'FloatPin')
        self.SH = self.createInputPin('SuperHard', 'FloatPin')


        # _____Output_____#
        self.Difficulty = self.createOutputPin('Difficulty', 'IntPin')
        self.OutName = self.createOutputPin('Name', 'StringPin')

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
        value = self.Value.getData()
        difficulty = 5

        if value == 1:
            difficulty = self.SE.getData()
        elif value == 2:
            difficulty = self.E.getData()
        elif value == 3:
            difficulty = self.M.getData()
        elif value == 4:
            difficulty = self.H.getData()
        else:
            difficulty = self.SH.getData()

        self.OutName.setData(self.Name.getData())
        self.Difficulty.setData(difficulty)










