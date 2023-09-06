from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import statistics


class TargetDifficulty(NodeBase):
    def __init__(self, name):
        super(TargetDifficulty, self).__init__(name)
        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)
        self.Target = self.createOutputPin('Target', 'IntPin')


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

        data = self.Data.getData()
        #self.set_difficulty(int(statistics.median(data)))
        self.Target.setData(int(statistics.median(data)))

    def set_difficulty(self, skill_level):
        # You can define your own mapping of skill levels to difficulty settings
        # Here's a simple example:
        print("skill_level :"+str(skill_level))
        if skill_level <= 1:
            print("Super Easy")
        elif skill_level <= 2:
            print("Easy")
        elif skill_level <= 3:
            print("Medium")
        elif skill_level <= 4:
            print("Hard")
        else:
            print("SuperHard")

