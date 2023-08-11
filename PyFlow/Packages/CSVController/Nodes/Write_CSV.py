from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import csv


def write_dict_to_csv(data_dict, filename):
    # Extract the keys from the dictionary to use as header in CSV

    fieldnames = data_dict.keys()

    # Open the CSV file in write mode
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for row_data in data_dict.values():
            writer.writerow(row_data)


class Write_CSV(NodeBase):
    def __init__(self, name):
        super(Write_CSV, self).__init__(name)
        # ____Input____#
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.FileName = self.createInputPin("FileName", 'StringPin')

        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')

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

        if self.Data.getData() is not None:
            data = self.Data.getData()

            filename = "default.csv"
            if self.FileName.getData() is not None:
                filename = self.FileName.getData() + ".csv"

            write_dict_to_csv(data, filename)
            print(f"Data successfully written to '{filename}'.")
