from datetime import datetime

from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from pylsl import StreamInlet, resolve_streams, pylsl
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
#LSL_Writer
class LSL_Reader(NodeBase):
        def __init__(self, name):
            super(LSL_Reader, self).__init__(name)
            self.out = self.createOutputPin("OUT", 'ExecPin')
            self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
            self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
            self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Multi)
            self.Send.enableOptions(PinOptions.AllowAny)
            self.Info = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Single)
            self.Info.enableOptions(PinOptions.AllowAny)
            self.inlets = []
            self.bWorking = False
            self.headerColor = FLOW_CONTROL_COLOR
            self.start = time.time()
            self.counter = 0

        def Tick(self, delta):
            super(LSL_Reader, self).Tick(delta)
            self.data = []
            if self.bWorking:
                if time.time() - self.start > 1:
                    self.start = time.time()
                    print("Number of values in one second->" + str(self.counter))
                    self.start = time.time()
                    self.counter = 0

                for inlet in self.inlets:
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    sample, timestamp = inlet.pull_sample()
                    new_data = {inlet.info().name(): sample}
                    # self.data={inlet.info().name(), sample, timestamp}
                    #print("[" + str(current_time) + "] Data: " + str(new_data))
                    # print(self.data)
                    self.Send.setData(new_data)
                self.counter=self.counter+1


        @staticmethod
        def keywords():
            return []

        @staticmethod
        def description():
            return "Description in rst format."

        def stop(self, *args, **kwargs):
            self.bWorking = False

        def start(self, *args, **kwargs):

            self.bWorking = True
            streams = resolve_streams()
            stream_information = dict()
            for stream in streams:

                inlet = StreamInlet(stream)
                stream_channels = dict()
                channels = inlet.info().desc().child("channels").child("channel")

                for i in range(inlet.info().channel_count()):
                    # Get the channel number (e.g. 1)
                    channel = i + 1

                    # Get the channel type (e.g. ECG)
                    sensor = channels.child_value("label")

                    # Get the channel unit (e.g. mV)
                    unit = channels.child_value("unit")

                    # Store the information in the stream_channels dictionary
                    stream_channels.update({channel: [sensor, unit]})
                    channels = channels.next_sibling()

                inlet_info = {
                    "Name": inlet.info().name(),
                    "Type": inlet.info().type(),
                    "Channels": int(inlet.info().channel_count()),
                    "Sampling Rate": int(inlet.info().nominal_srate()),
                    "Channels Info": stream_channels,
                }
                stream_information[inlet.info().name()] = inlet_info
                #print(inlet_info)
                self.Info.setData(stream_information)
                #print(str(stream_information))
                self.inlets.append(inlet)

        @staticmethod
        def category():
            return 'FlowControl'