import numpy as np

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *


class CalculationEmteq(NodeBase):
    def __init__(self, name):
        super(CalculationEmteq, self).__init__(name)
        #Inputs
        self.Data = self.createInputPin('Data', 'AnyPin', structure=StructureType.Multi)
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        #Outputs
        self.Focus = self.createOutputPin('Focus', 'IntPin')

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
        return 'Calculation'

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def compute(self, *args, **kwargs):
        data = self.Data.getData()
        emg_features = 0;
        ppg_features = data["PPG"]
        # Assuming you have 'emg_features' and 'ppg_features' as numpy arrays
        valence_estimation, arousal_estimation = self.estimate_valence_arousal(emg_features, ppg_features)

        print("Estimated Valence:", valence_estimation)
        print("Estimated Arousal:", arousal_estimation)

    def estimate_valence_arousal(self,emg_features, ppg_features):
        # Define thresholds for valence and arousal estimation
        valence_threshold = 0.5  # Adjust this value based on your data and requirements
        arousal_threshold = 0.5  # Adjust this value based on your data and requirements

        # Calculate the average of facial EMG features
        avg_emg = np.mean(emg_features)

        # Calculate the average of PPG sensor features
        avg_ppg = np.mean(ppg_features)

        # Estimate valence based on facial EMG features
        if avg_emg >= valence_threshold:
            valence = 'Positive'
        else:
            valence = 'Negative'

        # Estimate arousal based on PPG sensor features
        if avg_ppg >= arousal_threshold:
            arousal = 'High'
        else:
            arousal = 'Low'

        return valence, arousal
