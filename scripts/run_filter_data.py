from data_labeling_filtering.filter_data import filterData

if __name__ == "__main__":

    yaml_file = "config/filter_vox1.yaml"
    
    filter_data = filterData(yaml_file = yaml_file)
    filter_data()