import random
import time

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from pylsl import StreamInlet, resolve_streams, pylsl, StreamInfo, StreamOutlet
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR

#DemoNode
# LSL_Writer
class LSL_Writer(NodeBase):
    def __init__(self, name):
        super(LSL_Writer, self).__init__(name)
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

        self.bWorking = False
        self.outlet = None
        self.info = None
        self.headerColor = FLOW_CONTROL_COLOR
        self.On = False

        self.start_time = time.time()
        self.counter = 0

    def Tick(self, delta):
        super(LSL_Writer, self).Tick(delta)
        if self.bWorking:
            if not self.On:
                timevar = time.time()
                if len(self.Data.getData()) >= 1:
                    stream_name = self.streamName.getData()
                    stream_type = self.streamType.getData()
                    channel_count = len(self.Data.getData())
                    stream_desc = {
                        "Name": stream_name,
                        "Type": stream_type,
                        "Channels": channel_count,
                        "Sampling Rate": 20,
                        "Channels Info": self.get_all_keys(self.Data.getData()),
                    }
                    self.info = StreamInfo(
                        name=stream_name,
                        type=stream_type,
                        channel_count=channel_count,
                        nominal_srate=250,
                        channel_format='float32',
                        source_id=self.streamID.getData()
                    )
                    self.Info_Stream.setData({stream_name: stream_desc})
                    #self.outlet = StreamOutlet(self.info)
                    self.On = True
                    print("Time Consumed : ",(time.time()-timevar))
            else:
                timevar = time.time()
                #if self.outlet is not None:
                sample = list(self.Data.getData().values())
                if time.time() - self.start_time > 1:
                    self.start_time = time.time()
                    print("Number of Data sent in one second:", self.counter)
                    self.counter = 0
                self.counter += 1
                    #self.Send.setData({self.streamName.getData(): sample})
                    # self.outlet.push_sample(sample)
                print("Time Consumed : ", (time.time() - timevar))

    def get_all_keys(self, array_of_dicts):
        keys = dict()
        i = 0
        for key in array_of_dicts.keys():
            keys.update({i: [key, ""]})
            i += 1

        return keys

    @staticmethod
    def keywords():
        return []

    @staticmethod
    def description():
        return "Description in rst format."

    def stop(self, *args, **kwargs):
        self.bWorking = False
        self.On = False

    def start(self, *args, **kwargs):
        self.bWorking = True

    @staticmethod
    def category():
        return 'FlowControl'
