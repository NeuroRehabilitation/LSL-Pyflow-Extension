import numpy as np

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
import pandas as pd
import os


def append_to_csv(filename, data):
    # Read the existing CSV file
    try:
        existing_data = pd.read_csv(filename)
    except FileNotFoundError:
        existing_data = pd.DataFrame()

    # Append new data to the existing data
    new_data = existing_data.append(data, ignore_index=True)

    technologies = {
        'Courses': ["Spark", "PySpark", "Hadoop", "Python"],
        'Fee': [22000, 25000, np.nan, 24000],
        'Duration': ['30day', None, '55days', np.nan],
        'Discount': [1000, 2300, 1000, np.nan]}

    # Write the combined data to the CSV file
    new_data.to_csv(technologies, index=False)


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

            try:
                # Use the os.path.join() function to create a full file path
                file_path = os.path.join( '',filename)
                file_data = pd.read_csv(filename)
                append_to_csv(file_path, data)
                print(f"Data successfully written to '{file_path}'.")
            except PermissionError as e:
                print(f"Permission denied: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")