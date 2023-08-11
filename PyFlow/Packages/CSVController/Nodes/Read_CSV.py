from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import csv


class Read_CSV(NodeBase):
    def __init__(self, name):
        super(Read_CSV, self).__init__(name)
        self.FileName = self.createInputPin("FileName", 'StringPin')

        # _____Output_____#
        self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)




    @staticmethod
    def pinTypeHints():
        helper = NodePinsSuggestionsHelper()
        helper.addInputDataType('BoolPin')
        helper.addOutputDataType('BoolPin')
        helper.addInputStruct(StructureType.Single)
        helper.addOutputStruct(StructureType.Single)
        return helper

    @staticmethod
    def category():
        return 'Controllers'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        data = dict()
        filename = "default.csv"
        if self.FileName.getData() is not None:
            filename = self.FileName.getData() + ".csv"

        data = self.read_csv_file(filename)
        self.Send.setData(data)

    def read_csv_file_to_dict(self,filename):
        data_dict = {}
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for key, value in row.items():
                    data_dict[key] = value
        return data_dict
