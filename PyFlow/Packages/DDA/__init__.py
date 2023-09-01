PACKAGE_NAME = 'DDA'

from collections import OrderedDict
from PyFlow.UI.UIInterfaces import IPackage

# Class based nodes
from PyFlow.Packages.DDA.Nodes.DDA1 import DDA1
from PyFlow.Packages.DDA.Nodes.Skill import Skill
from PyFlow.Packages.DDA.Nodes.Difficulty import Difficulty
from PyFlow.Packages.DDA.Nodes.Skill1 import Skill1
from PyFlow.Packages.DDA.Nodes.Difficulty1 import Difficulty1
from PyFlow.Packages.DDA.Nodes.TargetDifficulty import TargetDifficulty
from PyFlow.Packages.DDA.Nodes.Dif import Dif
# Factories

_FOO_LIBS = {}
_NODES = {}
_PINS = {}
_TOOLS = OrderedDict()
_PREFS_WIDGETS = OrderedDict()
_EXPORTERS = OrderedDict()


_NODES = {
    DDA1.__name__: DDA1,
    Skill.__name__: Skill,
    Difficulty.__name__: Difficulty,
    Skill1.__name__: Skill1,
    Difficulty1.__name__: Difficulty1,
    TargetDifficulty.__name__: TargetDifficulty,
    Dif.__name__: Dif
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
