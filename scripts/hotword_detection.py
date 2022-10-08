import pvporcupine

class WakeupWordDetection():
    def __init__(self, access_key, keyword_paths):
        # AccessKey obtained from Picovoice Console (https://console.picovoice.ai/)
        access_key = access_key
        self.handle = pvporcupine.create(access_key=access_key, keyword_paths=keyword_paths)

    def detect(self, pcm):
        return self.handle.process(pcm)