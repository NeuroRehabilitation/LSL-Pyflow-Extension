from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class DemoNode(NodeBase):
    def __init__(self, name):
        super(DemoNode, self).__init__(name)
        self.Sensor_Name = self.createInputPin('Name', 'StringPin')
        self.Data = self.createInputPin('InData', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.Send = self.createOutputPin('DataOut', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)

        self.LastValue = self.createOutputPin('LastValue', 'FloatPin')

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
        sensor_name = self.Sensor_Name.getData()
        if self.Data.getData() is not None:
            data = self.Data.getData()
            if len(data) != 0:

                if data.keys() is not None:

                    if sensor_name in data["QuestionsStream"]:
                        self.Send.setData(data["QuestionsStream"][sensor_name])
                        try:
                            if len(data["QuestionsStream"][sensor_name]) != 0:
                                # Value exists, you can work with it here
                                #print("Value exists:", last_item)
                                self.LastValue.setData(data["QuestionsStream"][sensor_name][-1])
                            else:
                                print("Value is None")
                        except KeyError:
                            print("Value does not exist")

