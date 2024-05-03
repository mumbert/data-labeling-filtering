import logging
import audeer
import audonnx
import numpy as np
import os
import audinterface

class emotionClassification():

    def __init__(self, file_list: list, features: list, sampling_rate: int = 16000):

        logging.info(f"* Initializing class instance of [{self.__class__.__name__}]")
        self.file_list = file_list
        self.features = features
        self.model_dimensions = ["arousal", "dominance", "valence"]
        self.sampling_rate = sampling_rate
        self.metadata = {}

        model_root = self.download_model()
        self.model = audonnx.load(model_root)

    def download_model(self) -> str:

        url = 'https://zenodo.org/record/6221127/files/w2v2-L-robust-12.6bc4a7fd-1.1.0.zip'
        cache_root = audeer.mkdir('cache/emotion')
        model_root = audeer.mkdir('model/emotion')

        if not os.path.exists(os.path.join(model_root, "model.onnx")):
            archive_path = audeer.download_url(url, cache_root, verbose=True)
            audeer.extract_archive(archive_path, model_root)
            os.remove(archive_path)

        return model_root   

    def __call__(self):

        logging.info(f"* Getting emotion dimensions for {self.features}")

        interface = audinterface.Feature(
            self.model.labels('logits'),
            process_func=self.model,
            process_func_args={
                'outputs': 'logits',
            },
            sampling_rate=self.sampling_rate,
            resample=True,    
            verbose=True,
        )
        emotion_dimensions_df = interface.process_files(self.file_list).round(2)
        logging.info("\n")
        emotion_dimensions_df = emotion_dimensions_df.reset_index()
        columns = ["file"] + self.features
        emotion_dimensions_df = emotion_dimensions_df[columns]
        emotion_dimensions_df.set_index("file", inplace = True)
        self.metadata = emotion_dimensions_df.to_dict('index')


