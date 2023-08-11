PACKAGE_NAME = 'DDA'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.DDA.Nodes.DDA1 import DDA1
from PyFlow.Packages.DDA.Nodes.Skill import Skill
from PyFlow.Packages.DDA.Nodes.Difficulty import Difficulty

# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()


_NODES[DDA1.__name__] = DDA1
_NODES = {
    DDA1.__name__: DDA1,
    Skill.__name__: Skill,
	Difficulty.__name__: Difficulty
}

class DDA(IPackage):
	def __init__(self):
		super(DDA, self).__init__()

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

