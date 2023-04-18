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
        '''
        columns not used: ['College Name','Campus Size', 'Total Faculty',
                                        'Established Year', 'Courses', 'Facilities',
                                        'Country','Genders Accepted', 'University',
                                        'City', 'State', 'College Type', 'Courses_list',
                                        'Facilities_list']
        request.form = {'college_name': '', 'Genders Accepted': [],
                        'Total Student Enrollments': 1234, 'Rating': [1,2,3,4],
                        'University': [], 'City': [], 'State': [], 'Average Fees': 1234,
                        'Courses_list': [], 'Facilities_list': []
                    }
        '''
        data = {
            'college_name': request.form.getlist('college_name_list')[0].strip(),
            'Genders Accepted': request.form.getlist('genders_accepted_list'),
            'University': request.form.getlist('universities_list'),
            'City': request.form.getlist('cities_list'),
            'State': request.form.getlist('states_list'),
            'Courses_list': request.form.getlist('courses_list'),
            'Facilities_list': request.form.getlist('facilities_list')
        }
        # data = {'college_name': "National Institute of Technology Rourkela "}
        # print(f"{data}")
        # data = data.to_dict()

        model_params_dict = data_loaded['model_params_dict'].copy()
        if data['college_name'] != '':
            print('clg: ', data['college_name'])
            college = data_loaded['train_data'][data_loaded['train_data']['College Name'].str.strip() == data['college_name']]
            print(f"college = {college}")
            college = ohe_data(college)
            for key, value in college.items():
                if key in model_params_dict:
                    model_params_dict[key] = value
        
        for key, value in data.items():
            if key in data_loaded['ohe_prefix_dict']:
                ohe_prefix = data_loaded['ohe_prefix_dict'][key]
                for val in data_loaded['ohe_prefix_dict'][key]:
                    ohe_col = f"{ohe_prefix}{val}"
                    if ohe_col in model_params_dict:
                        model_params_dict[ohe_col] = 1
            else:
                if key in model_params_dict:
                    model_params_dict[key] = value
        

        results = predict_model(data_loaded, model_params_dict)
        return render_template("results_page.html", content=results.to_dict('records'))


@app.route('/results', methods=["GET", "POST"])
def results_page():
    # content = "results come here in a dictionary"
    return render_template("results_page.html")

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)