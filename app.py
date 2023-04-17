from flask import Flask, render_template
from python_scripts.read_frontend_json import read_json

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def search_page():
    json_data = read_json()

    
    return render_template("search_page.html", facilities_list=sorted(json_data["Facilities_list"]),
                            genders_accepted_list=sorted(json_data["Genders Accepted"]),
                            universities_list=sorted(json_data["University"]), 
                            cities_list=sorted(json_data["City"]),
                            states_list=sorted(json_data["State"]),
                            college_type_list=sorted(json_data["College Type"]),
                            courses_list=sorted(json_data["Courses_list"]))


@app.route('/results')
def results_page():
    content = "results come here in a dictionary"
    return render_template("results_page.html", content=content)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)