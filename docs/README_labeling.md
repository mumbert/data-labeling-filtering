# labeling

## Description

The class in charge to extract the metadata is named labelData in [label_data.py](../data_labeling_filtering/label_data.py) file. It integrates calling other classes to extract the corresponding metadata.

## Usage

In file [scripts/run_label_data.py](../scripts/run_label_data.py) there is a short example on how to run it. Basically, the configuration file is needed, and this is explained in the next sections.

```shell
from data_labeling_filtering.label_data import labelData

if __name__ == "__main__":

    yaml_file = "config/label_vox1.yaml"
    
    label_data = labelData(yaml_file = yaml_file)
    label_data()
    print(label_data.output_metadata)
```

In order to run this script:

```shell
cd data-labeling-filtering
poetry run python -W ignore scripts/run_label_data.py
```

And the result shown in the terminal is the following:

```shell
2024-05-02 22:35:37,112 * Initializing class instance of [labelData]
2024-05-02 22:35:37,113 * Loading config file: config/label_vox1.yaml
2024-05-02 22:35:37,114 * Getting file list in folder: data/vox1_test/wav/
2024-05-02 22:35:37,230         - 100/4874 files to process
2024-05-02 22:35:37,230 * [DOING] describe step
2024-05-02 22:35:37,230 * [DOING] format step
2024-05-02 22:35:37,230 * Initializing class instance of [wavFormat]
2024-05-02 22:35:37,230 * Getting files format
100%|█████████████████████████████████████████████████████████████████████| 100/100 [00:00<00:00, 5912.63it/s]
2024-05-02 22:35:37,253 * [DOING] transcribe step
2024-05-02 22:35:37,254 * Initializing class instance of [wavTranscription]
2024-05-02 22:35:38,081 * Transcribing files
100%|█████████████████████████████████████████████████████████████████████| 100/100 [02:34<00:00,  1.55s/it]
2024-05-02 22:38:12,624 * [DOING] emotion step
2024-05-02 22:38:12,627 * Initializing class instance of [emotionClassification]
2024-05-02 22:38:19,460 * Getting emotion dimensions for ['arousal', 'dominance', 'valence']
2024-05-02 22:43:13,918 * [DOING] gender_age step                                                   
2024-05-02 22:43:13,920 * Initializing class instance of [genderAgeClassification]
2024-05-02 22:43:16,507 * Getting gender and age for ['age', 'female', 'male', 'child', 'gender']
2024-05-02 22:45:20,714 * Generating output in json format in folder [output/labeling/vox1_test/json/output.json]
2024-05-02 22:45:20,719 * Generating output in dataframe format in file [output/labeling/vox1_test/dataframe/output.csv]
```


## Input

The inputs to the labeling class are:
- configuration YAML file: it specifies what metadata to extract
- dataset: folder containing speech files

### Configuration file

Here you can find an example of a [configuration file](../config/label_vox1.yaml). It can be stored in the configuration folder. Check the comments in some fields.

```shell
---
 general:
   max_files: 3 # --> -1 to process all files
 steps: # --> steps to do set to true
   describe: true
   format: true
   transcribe: true
   emotion: true
   gender_age: true
 dataset: # --> info about the dataset
   name: "vox1_test"
   folder: "data/vox1_test/wav/"
 format: # --> what metadata to extract in the metadata field of each step
   metadata: ["framerate", "nchannels", "sampwidth", "duration"]
 transcribe:
   metadata: ["text", "language"]
   whisper_model: "base"
 emotion:
   metadata: ["arousal", "dominance", "valence"]
 gender_age:
   metadata: ["age", "female", "male", "child", "gender"]
 output:
   basefolder: "output/labeling"
   json: true
   dataframe: true
```

### Dataset

For this project the [voxCeleb1 test dataset](https://mm.kaist.ac.kr/datasets/voxceleb/) has been used which has the following folder structure:
- wav folder containing multiple speaker ids
- for each speaker ids, different sources
- for each source, multiple clips have been extracted into wav files

```shell
data
└── vox1_test
    └── wav
        ├── id10270 --> speaker id
        │   ├── 5r0dWxy17C8 --> source with clips for this speaker id
        │   │   ├── 00001.wav --> extracted wav clips
        │   │   ├── 00002.wav
        ...
        │   │   └── 00027.wav
        │   ├── 8jEAjG6SegY --> source with clips for the same speaker id
        │   │   ├── 00001.wav
        │   │   ├── 00002.wav
        ...
        │   │   └── 00038.wav
        ├── id10271
        │   ├── 1gtz-CUIygI
        │   │   ├── 00001.wav
        │   │   ├── 00002.wav
        ...
        │   │   └── 00021.wav
        │   ├── 37nktPRUJ58
        │   │   ├── 00001.wav
```

## Functions, labels and models

Metadata is extracted in different functions which instanciate different class. The following table provides this mapping, which is used in the configuration file. The classes that use a model to estimate metadata are also specified.

| function      | labels            | model |
| ------------- | ----------------- | ------------- |
| describe      | file, speaker id  | none |
| format        | framerate, nchannels, sampwidth, duration  | none |
| transcribe    | text, language  | [whisper](https://pypi.org/project/openai-whisper/) |
| emotion       | arousal, dominance, valence | [opensmile w2v2](https://github.com/audeering/w2v2-how-to) |
| gender_age    | age, female, male, child, gender | [opensmile w2v2 age gender](https://github.com/audeering/w2v2-age-gender-how-to) |

### Describe

This one simply gets the file path and the speaker id from the voxCeleb test dataset files.

### Format

Basic wav format data, consisting of framerate, nchannels, sampwidth,  and duration

### Transcription

Text corresponding to the utterance in the wav file.

### Emotion

The 3 values estimated are:
- arousal (the intensity of emotion provoked by a stimulus)
- dominance (the degree of control exerted by a stimulus)
- valence (the pleasantness of a stimulus) 

These values correspond to the [extended circumplex model of affect](https://en.wikipedia.org/wiki/Emotion_classification#:~:text=22%5D%5B23%5D-,PAD%20emotional%20state%20model,-%5Bedit%5D) in 3 dimensions or PAD emotional state model.

### Gender and age

Estimation of the female, male, and child probabilities. Gender metadata corresponds to the feature with higher probability.

## Output

The metadata can be written in 2 different output files, both contain the same information:
- json
- csv

### Json file

Single file containing a dictionary:
- keys: file paths
- values: the extracted metadata

Example:

```shell
    "data/vox1_test/wav/id10295/nt7dNRvlEHE/00005.wav": {
        "file": "data/vox1_test/wav/id10295/nt7dNRvlEHE/00005.wav",
        "id": "id10295",
        "framerate": 16000,
        "nchannels": 1,
        "sampwidth": 2,
        "duration": 4.8000625,
        "text": " Egyptian guy was telling me that Dubai is amazing. He said, but it's summer. Stay.",
        "language": "en",
        "arousal": 0.3700000047683716,
        "dominance": 0.47999998927116394,
        "valence": 0.6800000071525574,
        "age": 44,
        "female": -0.8799999952316284,
        "male": 4.570000171661377,
        "child": -2.7699999809265137,
        "gender": "male"
    },
```

### Csv file

Single file where:
- rows are indexed by the filename
- columns are the different metatada

```shell
file,id,framerate,nchannels,sampwidth,duration,text,language,arousal,dominance,valence,age,female,male,child,gender
data/vox1_test/wav/id10295/nt7dNRvlEHE/00005.wav,id10295,16000,1,2,4.8000625," Egyptian guy was telling me that Dubai is amazing. He said, but it's summer. Stay.",en,0.3700000047683716,0.47999998927116394,0.6800000071525574,44,-0.8799999952316284,4.570000171661377,-2.7699999809265137,male

```