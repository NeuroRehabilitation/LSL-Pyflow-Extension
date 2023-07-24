from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *

import numpy as np
from scipy.signal import find_peaks


class HeartRate(NodeBase):
    def __init__(self, name):
        super(HeartRate, self).__init__(name)
        self.inExec = self.createInputPin(DEFAULT_IN_EXEC_NAME, 'ExecPin', None, self.compute)
        self.Data = self.createInputPin('InData', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.outExec = self.createOutputPin(DEFAULT_OUT_EXEC_NAME, 'ExecPin')
        self.Send = self.createOutputPin('DataOut', 'AnyPin', structure=StructureType.Multi)
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
        return 'Data Management'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):

        data = self.Data.getData()
        ppg_features = data["Ppg"]

        sampling_rate = 200

        # Calculate heart rate at baseline
        baseline_heart_rate = self.calculate_heart_rate(ppg_features, sampling_rate)

        # Calculate heart rate deviation
        heart_rate_deviation = self.calculate_heart_rate_deviation(ppg_features, sampling_rate, baseline_heart_rate)

        print("Baseline Heart Rate:", baseline_heart_rate, "beats per minute\n")
        print("Heart Rate Deviation from Baseline:", heart_rate_deviation,"\n")


    def calculate_heart_rate(self,ppg_data, sampling_rate):
        # Find peaks in the PPG data
        peaks, _ = find_peaks(ppg_data, height=0)

        # Calculate time intervals between consecutive peaks
        time_intervals = np.diff(peaks) / sampling_rate

        # Calculate heart rate (beats per minute)
        heart_rate_bpm = 60 / np.mean(time_intervals)

        return heart_rate_bpm

    def calculate_heart_rate_deviation(self,ppg_data, sampling_rate, baseline_heart_rate):
        # Calculate the heart rate at each time point
        heart_rates = []
        for i in range(len(ppg_data) // sampling_rate):
            start_idx = i * sampling_rate
            end_idx = (i + 1) * sampling_rate
            heart_rate = self.calculate_heart_rate(ppg_data[start_idx:end_idx], sampling_rate)
            heart_rates.append(heart_rate)

        # Calculate the deviation from the baseline heart rate
        deviation = np.array(heart_rates) - baseline_heart_rate

        return deviation

