from . import strategy
import time

class AlexaLikeWhisper():
    def __init__(self, access_key, keyword_path, modelsize, recoding_time=3):
        # initialize
        self.context = strategy.Recognizer(access_key, keyword_path, modelsize, recoding_time)
        self.context.initialize()

    def run(self):
        self.context.read()
        fin_flag, result = self.context.recognize()

        # get event
        if result == 'Wake':
            event = 'Whisper'
            self.context.change_recognizer(event)
            self.context.initialize()

        if fin_flag:
            event = 'WakeupWordDetection'
            self.context.change_recognizer(event)
            self.context.initialize()

        return result
