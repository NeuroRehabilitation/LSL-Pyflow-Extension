PACKAGE_NAME = 'EmteqPro'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.EmteqPro.Nodes.AcquisitionEmteq import AcquisitionEmteq
from PyFlow.Packages.EmteqPro.Nodes.SensorsEmteq import SensorsEmteq
from PyFlow.Packages.EmteqPro.Nodes.CalculationEmteq import CalculationEmteq
from PyFlow.Packages.EmteqPro.Nodes.CSVEmteq import CSVEmteq
from PyFlow.Packages.EmteqPro.Nodes.HeartRate import HeartRate

# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()


_NODES={
	AcquisitionEmteq.__name__:AcquisitionEmteq,
	SensorsEmteq.__name__:SensorsEmteq,
	CSVEmteq.__name__:CSVEmteq,
	HeartRate.__name__:HeartRate,
	CalculationEmteq.__name__:CalculationEmteq
}


class EmteqPro(IPackage):
	def __init__(self):
		super(EmteqPro, self).__init__()

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

