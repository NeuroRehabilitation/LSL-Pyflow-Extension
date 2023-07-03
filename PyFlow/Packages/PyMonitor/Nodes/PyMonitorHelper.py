from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
import main2
import sys
import multiprocessing


class PyMonitorHelper(NodeBase):
    def __init__(self, name):
        super(PyMonitorHelper, self).__init__(name)

        self.Data = self.createInputPin('InData', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions( PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.Send = self.createOutputPin('OutData', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)

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
       print("hello")



