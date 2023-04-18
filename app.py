from flask import Flask, render_template, request, redirect, url_for
from python_scripts.utilities import read_json, predict_model, load_data, ohe_data

app = Flask(__name__)

data_loaded = load_data()

@app.route("/", methods=["GET", "POST"])
def search_page():
    if request.method == "GET":
        json_data, college_name_list = read_json()

        return render_template("search_page.html", facilities_list=sorted(json_data["Facilities_list"]),
                                genders_accepted_list=sorted(json_data["Genders Accepted"]),
                                universities_list=sorted(json_data["University"]), 
                                cities_list=sorted(json_data["City"]),
                                states_list=sorted(json_data["State"]),
                                college_type_list=sorted(json_data["College Type"]),
                                courses_list=sorted(json_data["Courses_list"]),
                                college_name_list=sorted(college_name_list))
    elif request.method == "POST":
        data = {'college_name': 'National Institute of Technology Rourkela '}
        # data = data.to_dict()

        model_params_dict = data_loaded['model_params_dict'].copy()
        if data['college_name'] != '':
            college = data_loaded['train_data'][data_loaded['train_data']['College Name'] == data['college_name']]
            print(college)
            college = ohe_data(college)
            for key, value in college.items():
                if key in model_params_dict:
                    model_params_dict[key] = value
        
        for key, value in data.items():
            if key in model_params_dict:
                model_params_dict[key] = value
        

        results = predict_model(data_loaded, model_params_dict)
        return redirect(url_for('results_page', content=results.to_dict()))



@app.route('/results', methods=["POST"])
def results_page():
    content = "results come here in a dictionary"
    return render_template("results_page.html", content=content)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)