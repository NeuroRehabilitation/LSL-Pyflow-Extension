PACKAGE_NAME = 'PIDController'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.PIDController.Nodes.PIDNode import PIDNode

# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

_NODES[PIDNode.__name__] = PIDNode


class PIDController(IPackage):
	def __init__(self):
		super(PIDController, self).__init__()

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

