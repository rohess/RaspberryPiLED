import time
import numpy as np
import pyaudio
import config


class Microphone:

    def __init__(self):
        self.stream = None
        self.p = pyaudio.PyAudio()
        info = self.p.get_host_api_info_by_index(0)
        num_devices = info.get('deviceCount')
        for i in range(0, num_devices):
            if (self.p.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("Input Device id ", i, " - ", self.p.get_device_info_by_host_api_device_index(0, i).get('name'))

    def __del__(self):
        print("destructor")
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def start_stream(self, callback):
        frames_per_buffer = int(config.MIC_RATE / config.FPS)
        self.stream = self.p.open(format=pyaudio.paInt16,
                                  input_device_index=1,
                                  channels=1,
                                  rate=config.MIC_RATE,
                                  input=True,
                                  frames_per_buffer=frames_per_buffer)
        overflows = 0
        prev_ovf_time = time.time()
        while True:
            try:
                y = np.fromstring(self.stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
                y = y.astype(np.float32)
                callback(y)
            except IOError as err:
                overflows += 1
                if time.time() > prev_ovf_time + 1:
                    prev_ovf_time = time.time()
                    print("Error: ", err)
