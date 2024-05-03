# filtering

## Description

The class in charge to filter the metadata is named filterData in [filter_data.py](../data_labeling_filtering/filter_data.py) file. 

## Usage

In file [scripts/run_filter_data.py](../scripts/run_filter_data.py) there is a short example on how to run it. Basically, the configuration file is needed, and this is explained in the next sections.

```shell
from data_labeling_filtering.filter_data import filterData

if __name__ == "__main__":

    yaml_file = "config/filter_vox1.yaml"
    
    filter_data = filterData(yaml_file = yaml_file)
    filter_data()
```

In order to run this script:

```shell
cd data-labeling-filtering
poetry run python -W ignore scripts/run_filter_data.py
```

And the result shown in the terminal is the following:

```shell
2024-05-02 22:52:46,911 * Initializing class instance of [filterData]
2024-05-02 22:52:46,911 * Loading config file: config/filter_vox1.yaml
2024-05-02 22:52:46,913 * Loading input file: output/labeling/vox1_test/dataframe/output.csv
2024-05-02 22:52:46,917         - 100 files
2024-05-02 22:52:46,917 * Filtering using metadata
2024-05-02 22:52:46,917         - Filtering by id: ['id102*']
2024-05-02 22:52:46,923         - 100 filtered files
2024-05-02 22:52:46,923         - Filtering by framerate: [16000]
2024-05-02 22:52:46,925         - 100 filtered files
2024-05-02 22:52:46,925         - Filtering by nchannels: [1]
2024-05-02 22:52:46,925         - 100 filtered files
2024-05-02 22:52:46,925         - Filtering by sampwidth: [2]
2024-05-02 22:52:46,925         - 100 filtered files
2024-05-02 22:52:46,925         - Filtering by durations: [5.0, -1]
2024-05-02 22:52:46,926         - 66 filtered files
2024-05-02 22:52:46,926         - Filtering by text: ['you', 'looking']
2024-05-02 22:52:46,927         - 24 filtered files
2024-05-02 22:52:46,927         - Filtering by languages: ['en']
2024-05-02 22:52:46,927         - 24 filtered files
2024-05-02 22:52:46,925 * Generating output in dataframe format in file [output/filtering/vox1_test/json/output.json]
2024-05-02 22:52:46,927 * Generating output in dataframe format in file [output/filtering/vox1_test/dataframe/output.csv]
```

## Input

The inputs to the labeling class are:
- configuration YAML file: it specifies the filter to apply and their values
- dataset: folder containing speech files

### Configuration file

Here you can find an example of a [configuration file](../config/filter_vox1.yaml). It can be stored in the configuration folder. Check the comments in some fields.

```shell
---
 filters:
   id: ["id102*"] # speakers ids to select, can be used as regular expression
   framerate: [16000]
   nchannels: [1]
   sampwidth: [2] 
   min_max_durations: [5.0, -1] # tuple with the min duration and max duration, -1 means inf
   text: ["you", "looking"] # substrings that should contain the text
   languages: ["en"] # languages include
 dataset:
   name: "vox1_test"
 input:
   file: "output/labeling/vox1_test/dataframe/output.csv" # this file will be loaded
 output:
   basefolder: "output/filtering" # location where the output file will be saved
   json: false
   dataframe: true
```

### Generated metadata

It will load the input file of the generated metadata and its content will be filtered.

## Output

The metadata can be written in 2 different output files, both contain the same information:
- json
- csv

Their format is the same as specified in the labeling process.
