import whisper

class Whisper():
    def __init__(self, loaded_model):
        # Parameter on whisper
        self.model = whisper.load_model(loaded_model)
        print('Finished loading model')

    def recognize(self):
        return self.model.transcribe("temp.wav", language="ja")