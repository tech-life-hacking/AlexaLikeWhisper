import pyaudio

class Microphone():
    def __init__(self):
        self.pa = pyaudio.PyAudio()
        device = self.pa.get_default_output_device_info()
        self.audio_stream = self.pa.open(
            rate=int(device['defaultSampleRate']),
            channels=1,
            format=pyaudio.paInt16,
            input=True)

    def initialize(self, rate, format, frame_length):
        # initialize
        self.audio_stream.stop_stream()
        self.audio_stream.close()
        self.audio_stream = self.pa.open(
            rate=rate,
            channels=1,
            format=format,
            input=True,
            frames_per_buffer=frame_length)

    def read(self, frame_length):
        return self.audio_stream.read(frame_length)