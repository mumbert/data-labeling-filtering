import logging
import audeer
import audonnx
import numpy as np
import os
import audinterface

class genderAgeClassification():

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

        url = 'https://zenodo.org/record/7761387/files/w2v2-L-robust-6-age-gender.25c844af-1.1.1.zip'
        cache_root = audeer.mkdir('cache/gender_age/')
        model_root = audeer.mkdir('model/gender_age')

        if not os.path.exists(os.path.join(model_root, "model.onnx")):
            archive_path = audeer.download_url(url, cache_root, verbose=True)
            audeer.extract_archive(archive_path, model_root)
            os.remove(archive_path)

        return model_root   

    def __call__(self):

        logging.info(f"* Getting gender and age for {self.features}")

        outputs = ['logits_age', 'logits_gender']
        interface = audinterface.Feature(
            self.model.labels(outputs),
            process_func=self.model,
            process_func_args={
                'outputs': outputs,
                'concat': True,
            },
            sampling_rate=self.sampling_rate,
            resample=True,    
            verbose=True,
        )
        gender_age_dimensions_df = interface.process_files(self.file_list).round(2)
        logging.info("\n")
        gender_age_dimensions_df = gender_age_dimensions_df.reset_index()
        columns = ["file"] + self.features
        if "age" in columns:
            gender_age_dimensions_df["age"] = 100*gender_age_dimensions_df["age"]
            gender_age_dimensions_df["age"] = gender_age_dimensions_df["age"].astype(int)
        if "gender" in columns:
            gender_age_dimensions_df['gender'] = gender_age_dimensions_df.apply(self.assign_gender, axis=1)
        gender_age_dimensions_df = gender_age_dimensions_df[columns]
        gender_age_dimensions_df.set_index("file", inplace = True)

        self.metadata = gender_age_dimensions_df.to_dict('index')

    def assign_gender(self, row) -> str:

        if row["female"] > row["male"] and row["female"] > row["child"]:
            return "female"
        if row["male"] > row["female"] and row["male"] > row["child"]:
            return "male"
        if row["child"] > row["female"] and row["child"] > row["male"]:
            return "child"
        return "unknown"