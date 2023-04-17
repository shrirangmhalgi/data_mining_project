import json
import pandas as pd
import pickle

def load_data():
    # constants
    train_data = pd.read_csv("../data/train.csv")
    knn_model = pickle.load(open("./models/knn_model.sav", 'rb'))
    model_params_dict = json.load(open("./models/model_params_dict.json", 'r'))

    return {
        "train_data": train_data,
        "knn_model": knn_model,
        "model_params_dict": model_params_dict
    }

def read_json():
    json_file = open("./templates/json/filter_columns_data.json")
    data = json.load(json_file)
    
    return data

def predict_model(data_dict, data: dict):
    data = data['data']
    data = pd.DataFrame(data)
    distances, indices = data_dict['knn_model'].kneighbors(data) 
    return data_dict['train_data'][indices[0]]

