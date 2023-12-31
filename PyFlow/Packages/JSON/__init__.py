PACKAGE_NAME = 'JSON'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.JSON.Nodes.SaveJson import SaveJson
from PyFlow.Packages.JSON.Nodes.SaveJson2 import SaveJson2

# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()

_NODES[SaveJson.__name__] = SaveJson
_NODES = {
	SaveJson.__name__: SaveJson,
	SaveJson2.__name__: SaveJson2,
}

class JSON(IPackage):
	def __init__(self):
		super(JSON, self).__init__()

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

