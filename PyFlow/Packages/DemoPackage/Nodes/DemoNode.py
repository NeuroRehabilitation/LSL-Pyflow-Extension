import random
import multiprocessing
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from pylsl import StreamInlet, resolve_streams, pylsl, StreamInfo, StreamOutlet, local_clock
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR


# DemoNode
# LSL_Writer
class DemoNode(NodeBase):
    def __init__(self, name):
        super(DemoNode, self).__init__(name)
        self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
        self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
        self.streamName = self.createInputPin("Name", 'StringPin')
        self.streamType = self.createInputPin("Type", 'StringPin')
        self.streamID = self.createInputPin("ID", 'StringPin')
        self.Data = self.createInputPin('data', 'AnyPin', structure=StructureType.Dict, constraint="2")
        self.Data.enableOptions(
            PinOptions.AllowMultipleConnections | PinOptions.AllowAny | PinOptions.DictElementSupported)
        self.Data.disableOptions(PinOptions.SupportsOnlyArrays)

        self.Info_Stream = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Single)
        self.Info_Stream.enableOptions(PinOptions.AllowAny)
        self.Send = self.createOutputPin('DataOut', 'AnyPin', structure=StructureType.Multi)
        self.Send.enableOptions(PinOptions.AllowAny)

        self.q = multiprocessing.Queue()
        self.bWorking = False
        self.outlet = None
        self.info = None
        self.process = None
        self.headerColor = FLOW_CONTROL_COLOR
        self.On = False

    def Tick(self, delta):
        super(DemoNode, self).Tick(delta)
        if self.bWorking:
            if not self.On:
                if len(self.Data.getData()) >= 1:
                    self.info = StreamInfo(name=self.streamName.getData(), type=self.streamType.getData(),
                                           channel_count=len(self.Data.getData()),
                                           nominal_srate=250, channel_format='float32',
                                           source_id=self.streamID.getData())
                    self.process = multiprocessing.Process(target=generate_data_and_stream, args=(self.q))
                    self.process.start()
                    while self.q.get() != 1:
                        print("waiting")
                        self.q = self.info
                    Stream_Desc = {
                        "Name": self.streamName.getData(),
                        "Type": self.streamType.getData(),
                        "Channels": len(self.Data.getData()),
                        "Sampling Rate": 20,
                        "Channels Info": self.get_all_keys(self.Data.getData()),
                    }
                    self.Info_Stream.setData({self.streamName.getData(): Stream_Desc})
                    # self.outlet = StreamOutlet(self.info)

                    self.On = True
            else:
                if self.outlet is not None:
                    sample = list(self.Data.getData().values())
                    self.Send.setData({self.streamName.getData(): sample})
                    self.q.put(sample)

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.On = False
        self.process.terminate()

    def start(self, *args, **kwargs):
        self.bWorking = True

    @staticmethod
    def category():
        return 'FlowControl'


def get_all_keys(self, array_of_dicts):
    keys = dict()
    i = 0
    for key in array_of_dicts.keys():
        print("First ->" + str(array_of_dicts))
        keys.update({i: [key, ""]})
        i += 1
    return keys


def generate_data_and_stream(queue):
    # Create a stream outlet
    info = None
    while queue.get() != None:
        print("waiting")
        info = queue.get()

    outlet = StreamOutlet(info)
    queue.put(1)
    # Generate and send data in a continuous loop
    while True:
        # Replace the following line with your own data generation logic
        data = queue.get()

        # Get the current timestamp
        timestamp = local_clock()

        # Send the data with the timestamp
        outlet.push_sample(data, timestamp)

        # Put the data in the queue for the main process to access
        queue.put(data)
