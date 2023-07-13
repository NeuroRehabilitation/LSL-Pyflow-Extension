from datetime import datetime

from ReceiveStreams import *
from PyFlow.Core import NodeBase
from PyFlow.Core.NodeBase import NodePinsSuggestionsHelper
from PyFlow.Core.Common import *
from pylsl import StreamInlet, resolve_streams, pylsl
from PyFlow.Packages.PyFlowBase.Nodes import FLOW_CONTROL_COLOR
#LSL_Writer

class LSL_Reader4(NodeBase):
        def __init__(self, name):
            super(LSL_Reader4, self).__init__(name)
            self.out = self.createOutputPin("OUT", 'ExecPin')
            self.beginPin = self.createInputPin("Begin", 'ExecPin', None, self.start)
            self.stopPin = self.createInputPin("Stop", 'ExecPin', None, self.stop)
            self.BufferWindow = self.createInputPin("Buffer", 'IntPin')
            self.Send = self.createOutputPin('Data', 'AnyPin', structure=StructureType.Single)
            self.Send.enableOptions(PinOptions.AllowAny)
            self.Info = self.createOutputPin('Info', 'AnyPin', structure=StructureType.Single)
            self.Info.enableOptions(PinOptions.AllowAny)
            self.inlets = []
            self.bWorking = False
            self.headerColor = FLOW_CONTROL_COLOR
            self.buffer_window = None
            self.data_queue, self.buffer_queue, self.info_queue = (
                multiprocessing.Queue(),
                multiprocessing.Queue(),
                multiprocessing.Queue(),
            )

            # List with the stream info
            self.streams_info = []

            # Dictionaries to organize the data of all the streams
            self.synced_dict, self.info_dict, self.timestamps = {}, {}, {}

            # Flag to check if buffers are synced, if it is the first buffer of data
            self.isSync, self.isFirstBuffer = False, True

            self.streams_receiver = None
            self.n_full_buffers = 0

            self.DataBase = dict()
            self.start = time.time()
            self.counter = 0

        def Tick(self, delta):
            super(LSL_Reader4, self).Tick(delta)
            if self.bWorking:
                if int(time.time()) - self.start >= 1:
                    self.start = time.time()
                    print("LSL Receiver2->Number of values in one second:" + str(self.counter))
                    self.counter = 0
                    self.out.call()
                stream_name, data = self.streams_receiver.data_queue.get()
                self.getBuffers(data, stream_name)
                print(stream_name + "->" + str(self.synced_dict))
                self.Send.getData(self.synced_dict)

        @staticmethod
        def keywords():
            return []

        @staticmethod
        def description():
            return "Description in rst format."

        def stop(self, *args, **kwargs):
            self.bWorking = False
            self.streams_receiver = None

        def start(self, *args, **kwargs):
            self.bWorking = True
            self.isSync=True
            self.buffer_window=self.BufferWindow.getData()
            # Start all the available streams
            self.streams_receiver = self.getStreams()

            # Get the information from the streams
            self.getStreamsInfo(self.streams_receiver)
            # For every streams available create and fill the dictionary synced_dict with:
            # Name of the stream, Maximum Size of the buffers, Number of channels filled with data
            for stream in self.streams_info:
                self.synced_dict[stream["Name"]] = self.createDict(stream)
                self.info_dict[stream["Name"]] = stream
                self.info_dict[stream["Name"]]["Max Size"] = self.getBufferMaxSize(stream["Name"])
                self.info_dict[stream["Name"]]["Number full arrays"] = 0
                self.DataBase[stream.info().name()] = self.getChannelInformation(stream)

            self.Info.setData(self.streams_info)


        def addDataToDict(self, key, data):
            for i, row in enumerate(self.DataBase[key]):
                self.DataBase[key][row].append(data[i])
            self.counter=self.counter+1

        def getChannelInformation(self,inlet):
            channels_dicts = dict()
            for i in range(inlet.info().channel_count()):
                # Get the channel number (e.g. 1)
                channel = i + 1

                # Get the channel type (e.g. ECG)
                sensor = channels.child_value("label")

                # Get the channel unit (e.g. mV)
                unit = channels.child_value("unit")

                # Store the information in the stream_channels dictionary
                channels = channels.next_sibling()
                channels_dicts[sensor] = []
            return channels_dicts


        @staticmethod
        def category():
            return 'FlowControl'

        def getStreams(self):
            """
            Function to instantiate class ReceiveStreams and start the process ReceiveStreams;

            :return: returns object of class ReceiveStreams();

            """
            streams_receiver = ReceiveStreams()
            streams_receiver.start()

            return streams_receiver

        def getStreamsInfo(self, streams_receiver) -> None:
            """
            Function to get information about the streams and pass that information to a Queue

            :param streams_receiver: object of class ReceiveStreams()

            """

            self.streams_info = streams_receiver.info_queue.get()
            self.info_queue.put(self.streams_info)

        def createDict(self, stream_info: dict) -> dict:
            """
            Function to create dictionary for each stream with the channels names. columns_labels are the channels names.

            :param stream_info: dictionary with information about the stream
            :type stream_info: dict
            :return: dictionary with all the channels from the stream
            :rtype: dict
            """
            columns_labels = ["Timestamps"]
            for key in stream_info["Channels Info"].keys():
                columns_labels.append(stream_info["Channels Info"][key][0])
            dict = {key: [] for key in columns_labels}

            return dict

        def getBuffers(self, data: tuple, stream_name: str) -> None:
            """

            :param data: data from the streams
            :type data: tuple
            :param stream_name: name of the streams
            :type stream_name: str

            """

            # If the data is not synchronized keep putting the timestamps from each stream on the dictionary self.timestamps
            if not self.isSync:
                self.timestamps[stream_name] = data[1]
            # In case of the data being synchronized
            else:
                if self.isFirstBuffer:  # In case it is the first buffer of data
                    self.fillData(
                        data, stream_name
                    )  # Fills the first buffer of data with data
                    if self.n_full_buffers == len(
                            self.synced_dict.keys()
                    ):  # If first buffer has reached the maximum size put flag isFirstBuffer to False
                        self.isFirstBuffer = False
                    else:
                        # If buffers are not full keep checking the size of the buffers
                        self.checkBufferSize(
                            self.info_dict[stream_name]["Max Size"],
                            stream_name,
                        )
                else:
                    # If it is not the first buffer (buffers are with max size)
                    # Start sliding window and put buffers on the Queue to send to process
                    self.slidingWindow(stream_name)
                    self.fillData(data, stream_name)
                    self.buffer_queue.put(self.synced_dict)

        def getBufferMaxSize(self, stream_name: str) -> int:
            """Set the maximum size of the buffer to fill with data

            :param stream_name: name of the stream
            :type stream_name: str
            :return: max buffer size - window*fs
            :rtype: int
            """

            return int(self.buffer_window * self.info_dict[stream_name]["Sampling Rate"])

        def fillData(self, data: tuple, stream_name: str) -> None:
            """Function to fill the dictionary synced_dict with the data from each stream

            :param data: data from the streams
            :type data: tuple -[(nseq,value),timestamp]
            :param stream_name: name of the stream
            :type stream_name: str
            """

            self.synced_dict[stream_name]["Timestamps"].append(data[1])
            for i, key in enumerate(self.synced_dict[stream_name].keys()):
                if key != "Timestamps":
                    self.synced_dict[stream_name][key].append(data[0][i - 1])

        def checkBufferSize(self, max_size: int, stream_name: str) -> None:
            """Check if buffers are synchronized and then check the size of the buffers for every stream

            :param max_size: maximum size of the buffer
            :type max_size:int
            :param stream_name: name of the stream
            :type stream_name: str
            """

            if self.isSync:
                if self.info_dict[stream_name]["Number full arrays"] == len(
                        self.synced_dict[stream_name].keys()
                ):
                    self.n_full_buffers += 1
                else:
                    for key in self.synced_dict[stream_name].keys():
                        if len(self.synced_dict[stream_name][key]) == max_size:
                            self.info_dict[stream_name]["Number full arrays"] += 1