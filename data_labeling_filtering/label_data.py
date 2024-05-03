import os
import logging
import pandas as pd
import json
from data_labeling_filtering import utils
from data_labeling_filtering.wav_format import wavFormat
from data_labeling_filtering.wav_transcription import wavTranscription
from data_labeling_filtering.emotion_classification import emotionClassification
from data_labeling_filtering.gender_age_classification import genderAgeClassification
from data_labeling_filtering.dnsmos_local_new import dnsmos_new

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class labelData():

    def __init__(self, yaml_file: str) -> None:

        logging.info(f"* Initializing class instance of [{self.__class__.__name__}]")
        self.yaml_file = yaml_file
        self.config = utils.load_config(yaml_file = yaml_file)
        self.file_list = utils.get_file_list(folder = self.config["dataset"]["folder"], 
                                             pattern = "**/*.wav", 
                                             max_files = self.config["general"]["max_files"])
        self.output_metadata = {}

    def __call__(self) -> None:

        self.describe()
        self.format()
        self.transcribe()
        self.emotion()
        self.gender_age()
        self.dnsmos()
        self.write_output()

    def describe(self) -> None:

        if not self.do_step(step = "describe"):
            return

        describe_metadata = {}
        for file in self.file_list:
            file = str(file)
            id = os.path.basename(os.path.dirname(os.path.dirname(file)))
            metadata_features = {"file": file, "id": id}
            describe_metadata[file] = metadata_features

        self.update_output_metadata(new_metadata = describe_metadata)

    def format(self):

        if not self.do_step(step = "format"):
            return

        config = self.config["format"]

        format_metadata = wavFormat(file_list = self.file_list, features = config["metadata"])
        format_metadata()
        self.update_output_metadata(new_metadata = format_metadata.metadata)

    def transcribe(self):

        if not self.do_step(step = "transcribe"):
            return

        config = self.config["transcribe"]

        trans = wavTranscription(file_list = self.file_list, 
                                 features = config["metadata"],
                                 whisper_model = config["whisper_model"])
        trans()
        self.update_output_metadata(new_metadata = trans.metadata)

    def emotion(self):

        if not self.do_step(step = "emotion"):
            return

        config = self.config["emotion"]

        emotion_classification = emotionClassification(file_list = self.file_list, 
                                                       features = config["metadata"])
        emotion_classification()
        self.update_output_metadata(new_metadata = emotion_classification.metadata)

    def gender_age(self):

        if not self.do_step(step = "gender_age"):
            return

        config = self.config["gender_age"]

        gender_age_classification = genderAgeClassification(file_list = self.file_list, 
                                                         features = config["metadata"])
        gender_age_classification()
        self.update_output_metadata(new_metadata = gender_age_classification.metadata)

    def dnsmos(self):

        if not self.do_step(step = "dnsmos"):
            return

        config = self.config["dnsmos"]

        dnsmos_df = dnsmos_new(clips = self.file_list, 
                               personalized_MOS=False,
                               model_folder = "DNS-Challenge/DNSMOS/")
        print(dnsmos_df)

    def do_step(self, step) -> bool:

        if not self.config["steps"][step]:
            logging.info(f"* [SKIPPING] {step} step")
            return False
        else:
            logging.info(f"* [DOING] {step} step")
            return True

    def update_output_metadata(self, new_metadata: dict):

        for k, v in new_metadata.items():
            if k not in self.output_metadata.keys():
                self.output_metadata[k] = v
            else:
                self.output_metadata[k].update(new_metadata[k])

    def write_output_json(self):

        if self.config["output"]["json"]:
            output_json_folder = os.path.join(self.config["output"]["basefolder"], self.config["dataset"]["name"], "json")
            output_json_file = os.path.join(output_json_folder, "output.json")
            logging.info(f"* Generating output in json format in folder [{output_json_file}]")
            os.makedirs(output_json_folder, exist_ok = True)
            j = json.dumps(self.output_metadata, indent=4)
            with open(output_json_file, 'w') as f:
                print(j, file = f)

    def write_output_dataframe(self):

        if self.config["output"]["dataframe"]:
            output_dataframe_folder = os.path.join(self.config["output"]["basefolder"], self.config["dataset"]["name"], "dataframe")
            output_dataframe_file = os.path.join(output_dataframe_folder, "output.csv")
            logging.info(f"* Generating output in dataframe format in file [{output_dataframe_file}]")
            os.makedirs(output_dataframe_folder, exist_ok = True)
            pd.DataFrame.from_dict(self.output_metadata, orient = "index").to_csv(output_dataframe_file, index = False)

    def write_output(self):

        self.write_output_json()
        self.write_output_dataframe()
