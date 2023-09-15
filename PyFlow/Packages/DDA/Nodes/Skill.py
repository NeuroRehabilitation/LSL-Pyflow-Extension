from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class Skill(NodeBase):
    def __init__(self, name):
        super(Skill, self).__init__(name)
        self.StreamName = self.createInputPin('StreamName', 'StringPin')
        self.Name = self.createInputPin('Name', 'StringPin')

        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.Send = self.createOutputPin('DataOut', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)

        self.LastValue = self.createOutputPin('LastValue', 'FloatPin')
        self.SLastValue = self.createOutputPin('SLastValue', 'FloatPin')

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
        if self.Data.getData() is not None:
            data = self.Data.getData()
            stream_name = self.StreamName.getData()
            name = self.Name.getData()
            if len(data) != 0:

                if data.keys() is not None:

                    if name in data[stream_name]:
                        self.Send.setData(data[stream_name][name])
                        try:
                            if len(data[stream_name][name]) != 0:
                                # Value exists, you can work with it here
                                # print("Value exists:", last_item)
                                self.LastValue.setData(data[stream_name][name][-1])
                                self.SLastValue.setData(data[stream_name][name][-2])
                            else:
                                print("Value is None")
                        except KeyError:
                            print("Value does not exist")
