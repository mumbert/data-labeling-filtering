import os
import logging
from data_labeling_filtering import utils
import pandas as pd
import json

logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

class filterData():

    def __init__(self, yaml_file: str) -> None:

        logging.info(f"* Initializing class instance of [{self.__class__.__name__}]")
        self.yaml_file = yaml_file
        self.config = utils.load_config(yaml_file = yaml_file)
        self.metadata_pd = pd.DataFrame()

    def __call__(self):

        self.metadata_pd = self.load_input_file()
        self.output_metadata_pd = self.filter()
        self.write_output()

    def filter(self):

        logging.info(f"* Filtering using metadata")
        output_metadata_pd = self.filter_by_id(metadata_pd = self.metadata_pd)
        output_metadata_pd = self.filter_by_framerate(metadata_pd = output_metadata_pd)
        output_metadata_pd = self.filter_by_nchannels(metadata_pd = output_metadata_pd)
        output_metadata_pd = self.filter_by_sampwidth(metadata_pd = output_metadata_pd)
        output_metadata_pd = self.filter_by_durations(metadata_pd = output_metadata_pd)
        output_metadata_pd = self.filter_by_text(metadata_pd = output_metadata_pd)
        output_metadata_pd = self.filter_by_languages(metadata_pd = output_metadata_pd)

        return output_metadata_pd

    def filter_by_id(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["id"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by id: {self.config['filters']['id']}")
        mask = metadata_pd['id'].str.contains("|".join(self.config["filters"]["id"]))
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd

    def filter_by_framerate(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["framerate"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by framerate: {self.config['filters']['framerate']}")
        mask = metadata_pd['framerate'].isin(self.config["filters"]["framerate"])
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd
    
    def filter_by_nchannels(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["nchannels"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by nchannels: {self.config['filters']['nchannels']}")
        mask = metadata_pd['nchannels'].isin(self.config["filters"]["nchannels"])
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd

    def filter_by_sampwidth(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["sampwidth"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by sampwidth: {self.config['filters']['sampwidth']}")
        mask = metadata_pd['sampwidth'].isin(self.config["filters"]["sampwidth"])
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd
    
    def filter_by_durations(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["min_max_durations"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by durations: {self.config['filters']['min_max_durations']}")
        min_duration = self.config["filters"]["min_max_durations"][0]
        max_duration = self.config["filters"]["min_max_durations"][1]
        if max_duration == -1:
            max_duration = float('inf')

        mask = (metadata_pd['duration'] >= min_duration) & (metadata_pd['duration'] <= max_duration)
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd

    def filter_by_text(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["text"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by text: {self.config['filters']['text']}")
        mask = metadata_pd['text'].str.contains("|".join(self.config["filters"]["text"]))
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd

    def filter_by_languages(self, metadata_pd: pd.DataFrame) -> pd.DataFrame:

        if len(self.config["filters"]["languages"]) == 0:
            return metadata_pd

        logging.info(f"\t- Filtering by languages: {self.config['filters']['languages']}")
        mask = metadata_pd['language'].isin(self.config["filters"]["languages"])
        metadata_pd = metadata_pd[mask]
        logging.info(f"\t- {metadata_pd.shape[0]} filtered files")

        return metadata_pd
    
    def write_output_dataframe(self) -> None:

        if self.config["output"]["dataframe"]:
            output_dataframe_folder = os.path.join(self.config["output"]["basefolder"], self.config["dataset"]["name"], "dataframe")
            output_dataframe_file = os.path.join(output_dataframe_folder, "output.csv")
            logging.info(f"* Generating output in dataframe format in file [{output_dataframe_file}]")
            os.makedirs(output_dataframe_folder, exist_ok = True)
            self.output_metadata_pd.to_csv(output_dataframe_file, index = False)

    def write_output_json(self) -> None:

        if self.config["output"]["json"]:
            output_json_folder = os.path.join(self.config["output"]["basefolder"], self.config["dataset"]["name"], "json")
            output_json_file = os.path.join(output_json_folder, "output.json")
            logging.info(f"* Generating output in json format in file [{output_json_file}]")
            os.makedirs(output_json_folder, exist_ok = True)
            list_metadata = self.output_metadata_pd.to_dict(orient ='records')
            json_metadata = {}
            for json_data in list_metadata:
                json_metadata[json_data["file"]] = json_data
            j = json.dumps(json_metadata, indent=4)
            with open(output_json_file, 'w') as f:
                print(j, file = f)

    def write_output(self) -> None:

        self.write_output_json()
        self.write_output_dataframe()

    def load_input_file(self) -> pd.DataFrame:

        logging.info(f"* Loading input file: {self.config['input']['file']}")
        metadata_pd = pd.read_csv(self.config['input']['file'])
        logging.info(f"\t- {metadata_pd.shape[0]} files")

        return metadata_pd
