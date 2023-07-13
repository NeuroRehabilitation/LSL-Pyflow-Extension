from PyFlow.Packages.LSLController.Nodes.LSL_Writer import LSL_Writer
from PyFlow.Packages.LSLController.Nodes.LSL_Writer2 import LSL_Writer2

PACKAGE_NAME = 'LSLController'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.LSLController.Nodes.LSL_Reader import LSL_Reader
from PyFlow.Packages.LSLController.Nodes.LSL_Reader2 import LSL_Reader2
from PyFlow.Packages.LSLController.Nodes.LSL_Reader3 import LSL_Reader3
from PyFlow.Packages.LSLController.Nodes.LSL_Reader4 import LSL_Reader4
# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()


_NODES={
	LSL_Reader.__name__:LSL_Reader,
	LSL_Reader2.__name__:LSL_Reader2,
	LSL_Reader3.__name__:LSL_Reader3,
	LSL_Reader4.__name__:LSL_Reader4,
	LSL_Writer.__name__:LSL_Writer,
	LSL_Writer2.__name__:LSL_Writer2
}


class LSLController(IPackage):
	def __init__(self):
		super(LSLController, self).__init__()

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

