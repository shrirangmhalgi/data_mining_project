import json

def read_json():
    json_file = open("./templates/json/filter_columns_data.json")
    data = json.load(json_file)
    
    return data


