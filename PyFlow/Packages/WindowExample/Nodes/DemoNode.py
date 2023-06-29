from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from PyQt5.QtWidgets import QApplication, QWidget
import sys
import multiprocessing

class DemoNode(NodeBase):
    def __init__(self, name):
        super(DemoNode, self).__init__(name)

        self.out = self.createOutputPin('out', 'IntPin')
    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('IntPin')

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
        self.out.setData(1)
        self.startWindow()

    #function that starts a new process
    def startWindow(self):
        p2 = multiprocessing.Process(target=WindowPage.openWindow, args=())
        p2.start()

##open a window in a new process
class WindowPage(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 300)
        self.setWindowTitle('Window')
        self.show()

    @staticmethod
    def openWindow():
        app = QApplication(sys.argv)
        w = WindowPage()
        sys.exit(app.exec_())