import logging
import whisper
from tqdm import tqdm

class wavTranscription():

    def __init__(self, file_list: list, features: list, whisper_model: str):

        logging.info(f"* Initializing class instance of [{self.__class__.__name__}]")
        self.file_list = file_list
        self.features = features
        self.metadata = {}
        self.model = whisper.load_model(whisper_model)

    def __call__(self):

        logging.info(f"* Transcribing files")
        for file in tqdm(self.file_list):
            file = str(file)
            result = self.model.transcribe(file)
            metadata_features = {"file": file}
            for feature in self.features:
                metadata_features[feature] = result[feature]
            self.metadata[file] = metadata_features
