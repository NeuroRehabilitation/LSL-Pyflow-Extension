from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyQt5.QtWidgets import QApplication, QWidget
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
import main2
import sys
import multiprocessing


class OpenWindow(NodeBase):
    def __init__(self, name):
        super(OpenWindow, self).__init__(name)
        self.out = self.createOutputPin("OUT", 'ExecPin')
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
        self.bWorking = False

        self.info = self.createInputPin('Info', 'AnyPin', structure=StructureType.Single)
        self.info.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.info.disableOptions(PinOptions.SupportsOnlyArrays)

        self.data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.data.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.q = multiprocessing.Queue()
        self.online = False
        self.Prosess = multiprocessing.Process(target=main2.Run, args=(self.q,))
        self.headerColor = FLOW_CONTROL_COLOR
        self.counter = 0
        self.start = time.time()

    def Tick(self, delta):
        super(OpenWindow, self).Tick(delta)
        if self.bWorking and self.online:
            if time.time() - self.start > 1:
                self.start = time.time()
                self.counter = 0
                self.q.put(self.data.getData())
            self.counter += 1


    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('ExecPin')
        helper.addInputDataType('FloatPin')
        helper.addOutputDataType('ExecPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.online = False
        self.Prosess.terminate()
        self.Prosess.join()
        self.Prosess = multiprocessing.Process(target=main2.Run, args=(self.q,))

    def start(self, *args, **kwargs):
        if self.bWorking:
            self.Prosess.terminate()
            self.Prosess.join()
            self.Prosess = multiprocessing.Process(target=main2.Run, args=(self.q,))

        self.bWorking = True
        self.Prosess.start()
        self.q.put(self.info.getData())
        while self.q.get() != 1:
            #print(self.info.getData())
            self.q.put(self.info.getData())
        self.online = True


    @staticmethod
    def category():
        return 'Window'

