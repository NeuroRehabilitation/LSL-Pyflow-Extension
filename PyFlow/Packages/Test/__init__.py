PACKAGE_NAME = 'Test'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.Test.Nodes.DataBase import DataBase
from PyFlow.Packages.Test.Nodes.DataBase2 import DataBase2
from PyFlow.Packages.Test.Nodes.CreateDict import CreateDict
from PyFlow.Packages.Test.Nodes.CreateDict2 import CreateDict2

# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

_NODES={
	DataBase.__name__:DataBase,
	DataBase2.__name__:DataBase2,
	CreateDict.__name__:CreateDict,
	CreateDict2.__name__:CreateDict2
}

class Test(IPackage):
	def __init__(self):
		super(Test, self).__init__()

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

