from flask import Flask, render_template, request, redirect, url_for
from python_scripts.utilities import load_data, read_json, predict_model

app = Flask(__name__)
data_dict = load_data()
json_data = read_json()

@app.route("/", methods=["GET", "POST"])
def search_page():

    return render_template("search_page.html", facilities_list=sorted(json_data["Facilities_list"]),
                            genders_accepted_list=sorted(json_data["Genders Accepted"]),
                            universities_list=sorted(json_data["University"]), 
                            cities_list=sorted(json_data["City"]),
                            states_list=sorted(json_data["State"]),
                            college_type_list=sorted(json_data["College Type"]),
                            courses_list=sorted(json_data["Courses_list"]))

@app.route('/predict', methods=["POST"])
def predict():
    if request.method == "POST":
        data = request.get_json()
        if 'type' in data:
            if data['type'] == 'college_search':
                params = data_dict['train_data_ohe'][data_dict['train_data_ohe']['College Name'] == data['college_name']].to_dict(orient='records')[0]
            elif data['type'] == 'college_filter':
                params = data['params']
        else:
            print("Error: type not found in data")
        
        model_params_dict = data_dict['model_params_dict'].copy()
        for key in params:
            if key in model_params_dict:
                model_params_dict[key] = params[key]
        
        results = predict_model(data_dict, model_params_dict)
        return results

@app.route('/search', methods=["POST"])
def search():
    data = request.get_json()
    train_dat = data_dict['train_data'].copy()
    for key in data:
        if key in train_dat:
            train_dat = train_dat[train_dat[key] == data[key]]
    return train_dat.to_dict(orient='records')


@app.route('/results')
def results_page():
    content = "results come here in a dictionary"
    return render_template("results_page.html", content=content)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)