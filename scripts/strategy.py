import scripts.hotword_detection as hotword_detection
import scripts.input as input
import scripts.recognition as recognition

import struct
import numpy as np
import scipy.io.wavfile
from abc import ABCMeta, abstractmethod

import torch

WHISPER_RATE = 44100
WHISPER_FRAME_LENGTH = 1024

class Strategy(metaclass=ABCMeta):
    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def recognize(self):
        pass

class WaitWakeupWord():
    def __init__(self, access_key, keyword_path):
        self.wakeup = hotword_detection.WakeupWordDetection(access_key, keyword_path)
        self.mike = input.Microphone()

    def initialize(self):
        self.mike.initialize(self.wakeup.handle.sample_rate, input.pyaudio.paInt16, self.wakeup.handle.frame_length)

    def read(self):
        audio = self.mike.read(self.wakeup.handle.frame_length)
        self.pcm = struct.unpack_from("h" * self.wakeup.handle.frame_length, audio)

    def recognize(self):
        result = self.wakeup.handle.process(self.pcm)
        if result >= 0:
            return False, "Wake"
        else:
            return False, "Sleep"

class WakeupWordDetected():
    def __init__(self, modelsize, recoding_time):
        self.frames = []
        self.counter = 0
        self.mike = input.Microphone()
        self.whis = recognition.Whisper(modelsize)
        self.recoding_time = int(WHISPER_RATE*recoding_time/WHISPER_FRAME_LENGTH)

    def initialize(self):
        self.frames = []
        self.counter = 0
        self.mike.initialize(WHISPER_RATE, input.pyaudio.paFloat32, WHISPER_FRAME_LENGTH)

    def read(self):
        self.counter += 1
        audio = self.mike.read(WHISPER_FRAME_LENGTH)
        d = np.frombuffer(audio, dtype=np.float32)
        self.frames = np.append(self.frames, d)

    def recognize(self):
        if self.counter == self.recoding_time:
            self.frames = np.array(self.frames).flatten()
            scipy.io.wavfile.write("temp.wav", WHISPER_RATE, self.frames)
            return True, self.whis.recognize()['text']
        else:
            return False, "On recording..."

class Recognizer:
    def __init__(self, access_key, keyword_path, modelsize, recoding_time):
        self.wakeup_word_detection = WaitWakeupWord(access_key, keyword_path)
        self.whisper = WakeupWordDetected(modelsize, recoding_time)
        self.strategy = self.wakeup_word_detection

    def change_recognizer(self, recognizer):
        if recognizer == 'WakeupWordDetection':
            self.strategy = self.wakeup_word_detection
        elif recognizer == 'Whisper':
            self.strategy = self.whisper
        else:
            pass

    def initialize(self):
        self.strategy.initialize()

    def read(self):
        self.strategy.read()

    def recognize(self):
        return self.strategy.recognize()