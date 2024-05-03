import wave
import logging
from tqdm import tqdm

class wavFormat():

    def __init__(self, file_list: list, features: list):

        logging.info(f"* Initializing class instance of [{self.__class__.__name__}]")
        self.file_list = file_list
        self.features = features
        self.metadata = {}

    def __call__(self):
        
        logging.info(f"* Getting files format")
        for file in tqdm(self.file_list):
            file = str(file)
            metadata = self.get_wav_format(file)
            metadata_features = {"file": file}
            for feature in self.features:
                if feature == "duration":
                    metadata_features[feature] = getattr(metadata, "nframes") / float(getattr(metadata, "framerate"))
                else:
                    metadata_features[feature] = getattr(metadata, feature)
            self.metadata[file] = metadata_features

    @staticmethod
    def get_wav_format(wav: str):
        
        with wave.open(wav) as wav_file:
            metadata = wav_file.getparams()

        return metadata
