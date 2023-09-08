from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class Skill1(NodeBase):
    def __init__(self, name):
        super(Skill1, self).__init__(name)
        self.StreamName = self.createInputPin('StreamName', 'StringPin')
        self.Name = self.createInputPin('Name', 'StringPin')

        self.SE = self.createInputPin('SuperEasy', 'FloatPin')
        self.E = self.createInputPin('Easy', 'FloatPin')
        self.M = self.createInputPin('Medium', 'FloatPin')
        self.H = self.createInputPin('Hard', 'FloatPin')
        self.SH = self.createInputPin('SuperHard', 'FloatPin')

        self.Target = self.createInputPin('Difficulty', 'FloatPin')

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

        target = self.Target.getData()

        if target == 1:
            self.Performance.setData(self.SE.getData())

        elif target == 2:
            self.Performance.setData(self.E.getData())

        elif target == 3:
            self.Performance.setData(self.M.getData())

        elif target == 4:
            self.Performance.setData(self.H.getData())

        elif target == 5:
            self.Performance.setData(self.SH.getData())
