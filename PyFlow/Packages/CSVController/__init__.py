PACKAGE_NAME = 'CSVController'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.CSVController.Nodes.Read_CSV import Read_CSV
from PyFlow.Packages.CSVController.Nodes.Write_CSV import Write_CSV

# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

_NODES = {
    Read_CSV.__name__: Read_CSV,
    Write_CSV.__name__: Write_CSV,
}


class CSVController(IPackage):
    def __init__(self):
        super(CSVController, self).__init__()

    @staticmethod
    def GetExporters():
        return _EXPORTERS

    @staticmethod
    def GetFunctionLibraries():
        return _FOO_LIBS

    @staticmethod
    def GetNodeClasses():
        return _NODES

    @staticmethod
    def GetPinClasses():
        return _PINS

    @staticmethod
    def GetToolClasses():
        return _TOOLS
