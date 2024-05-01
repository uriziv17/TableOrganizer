import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from werkzeug.utils import secure_filename
from Table import Table
from actions.relaxtionLabel.relaxtion import updatePersonsMatrix, setPersonsMatrix, findSitting

# TODO hide behind a lock
uid_counter = 1
app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/template')

app.config['UPLOAD_FOLDER'] = os.path.join('web', 'static', 'uploads')

THE_TABLE: Table = None
names_dict = {}
names_counter = 0
person_matrix = None
RESULT_PATH = "web/static/result.png"


@app.route('/')
def getHomePage():
    return render_template('index.html')


@app.route('/get-uid/')
def get_uid():
    global uid_counter
    uid_counter += 1
    return {'uid': uid_counter - 1}


@app.route('/upload_picture/', methods=['POST'])
def upload_picture():
    global THE_TABLE
    uploaded_picture = request.files.get('picture')
    if uploaded_picture and uploaded_picture.mimetype.startswith('image/'):
        try:
            # TODO: the html template is trying to search under static folder - fix the path!
            filename = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(uploaded_picture.filename))
            uploaded_picture.save(filename)
            THE_TABLE = Table(filename)
            return redirect(url_for('add_names')), 301
        except IOError:
            return "<p> internal server file error :( </p>"

    return "internal error."


@app.route('/table_details', methods=['GET'])
def table_details():
    global THE_TABLE
    #render_template('tableDetails.html', table=THE_TABLE)
    return redirect('/add_names/', 301)


def add_name_to_list(name):
    script = f"<script>addNameToList('{name}');</script>"
    return script


@app.route('/add_names/', methods=['GET', 'POST'])
def add_names():
    global names_counter
    if request.method == 'GET':
        return render_template('addNames.html')  # Render name collection page
    else:
        name = request.form.get('name')
        if name:
            if len(names_dict) + 1 > len(THE_TABLE.spots):
                print("there are to many guests for this table")
                names_dict.clear()
                return redirect('/add_names/', 301)
            names_dict[names_counter] = name  # Add name to dictionary
            print(f"Name added: {name}")

            # Call JavaScript function to add name to the list
            add_name_to_list(name)
            names_counter += 1
            print(names_dict)

        if 'done' in request.form:  # Check if "Done" button is pressed
            return redirect('/preferences', 301)  # Redirect to table details
        return redirect('/add_names/', 301)  # Redirect back to name collection page


@app.route('/preferences', methods=['GET'])
def get_preferences():
    global names_dict, person_matrix
    person_matrix = setPersonsMatrix(THE_TABLE)
    return render_template('addCons.html', names_dict=names_dict)  # Render seating preference page


@app.route('/preferences', methods=['POST'])
def set_preferences():
    global names_dict, person_matrix, RESULT_PATH
    p1index = int(request.form.get('name1'))
    p2index = int(request.form.get('name2'))
    preference = request.form.get('preference')

    error_message = ""

    if p1index == p2index:
        error_message = "Please select two diffrent names"

    isLike = 'like' == preference
    updatePersonsMatrix(person_matrix, p1index, p2index, isLike)
    if 'done' in request.form:
        sitting = findSitting(THE_TABLE, person_matrix)
        THE_TABLE.populate_spots(names_dict, sitting)
        resultImg = THE_TABLE.draw_sitting_arrangement(RESULT_PATH)
        return redirect('/result', 301)
    return render_template('addCons.html', names_dict=names_dict, error=error_message)


@app.route('/result', methods=['GET'])
def get_results():
    global RESULT_PATH
    return render_template("result.html", result_image_path=RESULT_PATH)


def main():
    app.run(debug=True)


if __name__ == '__main__':
    main()
