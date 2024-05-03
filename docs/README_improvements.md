# Future improvements

## Description

In this section we can find a list of future improvements from different perspectives:
- metadata
- input files
- output files
- code
- performance

## Metadata

Other metadata features can be included, such as:
- speaker embeddings:
  - by using the [resemblyzer](https://github.com/resemble-ai/Resemblyzer) project, demo 01 more concretely
- diarization: 
  - using the [pyannote](https://github.com/pyannote/pyannote-audio) project we can estimate when the different speakers are present in the speech signal,
  - by using this information the amount of different speakers can be estimated
- Audio events (e.g. laughter, crowd cheers, music) along with their timestamps

## Input

The current project should be tested with other speech datasets to test how the different metadata labels behave depending content. 

## Output

At this stage 2 different output formats are provided. JSON and CSV files have been used. In an AWS setup, uploading the metadata to a dynamobDB table could be really convenient.

## Code

Code can be improved from the following perspectives:
- refactor: for instance, in the filtering class some functions share part of the code

## Performance

The performance improvements that can improve the project speed and usability could be:
- parallelization: to speed up the metadata estimation
- dockerization: to provide a ready-to-use Dockerfile