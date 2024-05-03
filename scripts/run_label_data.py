from data_labeling_filtering.label_data import labelData

if __name__ == "__main__":

    yaml_file = "config/label_vox1.yaml"
    
    label_data = labelData(yaml_file = yaml_file)
    label_data()
    print(label_data.output_metadata)