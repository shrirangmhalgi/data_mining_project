import json
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors
import ast

def load_data():
    # constants
    train_data = pd.read_csv("./data/proccessed_indian_universities.csv").drop(columns=['Unnamed: 0'])
    train_data['Facilities_list'] =[ast.literal_eval(x) for x in train_data['Facilities_list'] ]
    train_data['Courses_list'] =[ast.literal_eval(x) for x in train_data['Courses_list'] ]
    # knn_model = pickle.load(open("./data/models/knnpickle_file.pkl", 'rb'))
    # model_params_dict = json.load(open("./data/models/final_param_out.json", 'r'))

    engg_colleges = train_data.copy()
    ohe_prefix_dict = {
        'Facilities_list': 'facility_',
        'Courses_list': 'course_',
        'University': 'uni_',
        'City': 'city_',
        'State': 'state_',
        'College Type': 'ctype_',
        'Genders Accepted': 'gender_',
    }
    for col, pre in ohe_prefix_dict.items():
        # Apply one-hot encoding on the list in the row
        college_before = list(engg_colleges.columns)
        engg_colleges = pd.concat([engg_colleges,
                                   pd.get_dummies(engg_colleges[col].apply(pd.Series).stack()).sum(level=0)
                                   ], axis=1)
        engg_colleges.columns = [f'{pre}{i}' if i not in college_before else f'{i}' for i in engg_colleges.columns]

    engg_colleges = engg_colleges.drop(['College Name','Campus Size', 'Total Faculty',
                                        'Established Year', 'Courses', 'Facilities',
                                        'Country','Genders Accepted', 'University',
                                        'City', 'State', 'College Type', 'Courses_list',
                                        'Facilities_list'],
                                        axis = 1)
    engg_colleges = engg_colleges.fillna(0)

    neigh = NearestNeighbors(n_neighbors=5, algorithm='brute')
    neigh.fit(engg_colleges)

    model_params_dict = {}
    for col in engg_colleges.columns:
        model_params_dict[col] = 0

    return {
        "train_data": train_data,
        "knn_model": neigh,
        "model_params_dict": model_params_dict,
        'ohe_prefix_dict': ohe_prefix_dict
    }

def read_json():
    json_file = open("./templates/json/filter_columns_data.json")
    data = json.load(json_file)
    college_name_list = json.load(open('./templates/json/all_colleges_names.json'))["college_names"]
    
    return data, college_name_list

def predict_model(data_dict, data: dict):
    data = pd.DataFrame(data)
    distances, indices = data_dict['knn_model'].kneighbors(data)
    return data_dict['train_data'].iloc[indices[0]]

def ohe_data(data: pd.DataFrame):
    data_df = data.copy()
    print(data_df)
    ohe_prefix_dict = {
        'Facilities_list': 'facility_',
        'Courses_list': 'course_',
        'University': 'uni_',
        'City': 'city_',
        'State': 'state_',
        'College Type': 'ctype_',
        'Genders Accepted': 'gender_',
    }
    for col, pre in ohe_prefix_dict.items():
        # Apply one-hot encoding on the list in the row
        college_before = list(data_df.columns)
        data_df = pd.concat([data_df,
                          pd.get_dummies(data_df[col].apply(pd.Series).stack()).sum(level=0)
                          ], axis=1)
        data_df.columns = [f'{pre}{i}' if i not in college_before else f'{i}' for i in data_df.columns]
        data_df.drop(columns=[col], inplace=True)
    print('in ohe_data', data_df)
    return data_df

