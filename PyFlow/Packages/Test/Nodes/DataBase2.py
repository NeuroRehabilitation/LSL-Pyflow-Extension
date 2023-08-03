from datetime import datetime

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


class DataBase2(NodeBase):
    def __init__(self, name):
        super(DataBase2, self).__init__(name)
        # ____Input____#
        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        # _____Output_____#
        self.N_Channels = self.createOutputPin('N_Channels', "IntPin")
        self.N_Sources = self.createOutputPin('N_Source', "IntPin")
        self.Lastvalues = self.createOutputPin('Last_Value', 'IntPin')
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
        data = self.Data.getData()
        self.N_Sources.setData(len(data))
        n_channels = 0
        lastvalues = []

        for source in data:
            n_channels += len(data[source])

            for channels in data[source]:
                if not data[source][channels]:
                    continue
                # print("Source = {} | Data = {} | Channels = {} | Number Channel = {}".format(source, data[source],
                # channels, n_channels))
                lastvalues.append(data[source][channels][-1])
                if channels == "DelayTest":
                    lastvalues[0] = data[source][channels][-1]
                    continue

        self.N_Channels.setData(n_channels)
        self.Lastvalues.setData(lastvalues)
