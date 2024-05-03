import logging
import yaml
from pathlib import Path

def load_config(yaml_file: str) -> dict:

    try: 
        logging.info(f"* Loading config file: {yaml_file}")
        with open (yaml_file, 'r') as file:
            config = yaml.safe_load(file)
    except Exception as e:
        print(f"Error reading the config file: {yaml_file}")
        print(str(e))
        config = {}

    return config

def get_file_list(folder: str, pattern: str, max_files: int):

    logging.info(f"* Getting file list in folder: {folder}")

    file_list = list(Path(folder).glob(pattern))
    all_files = len(file_list)

    if max_files != -1:
        file_list = file_list[:max_files]
    
    logging.info(f"\t- {len(file_list)}/{all_files} files to process")

    return file_list