import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from Table import Table
from actions.relaxtionLabel.relaxtion import (
    updatePersonsMatrix,
    setPersonsMatrix,
    findSitting,
)
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FormField, SubmitField
from wtforms.validators import DataRequired

# TODO hide behind a lock
uid_counter = 1
app = Flask(__name__, static_folder="web/static", template_folder="web/template")

app.config["UPLOAD_FOLDER"] = os.path.join("web", "static", "uploads")

THE_TABLE: Table = None
names_dict = {}
names_counter = 0
person_matrix = None


class PairForm(FlaskForm):
    global names_dict
    name1 = SelectField(
        "Person 1",
        choices=[(i, name) for i, name in names_dict.items()],
        validators=[DataRequired()],
    )
    name2 = SelectField(
        "Person 2",
        choices=[(i, name) for i, name in names_dict.items()],
        validators=[DataRequired()],
    )
    like = SelectField(
        "Like", choices=[("yes", "Yes"), ("no", "No")], validators=[DataRequired()]
    )


class MainForm(FlaskForm):
    pairs = FormField(PairForm)
    submit = SubmitField("Submit")


num = 0


@app.route("/")
def getHomePage():
    return render_template("index.html")


@app.route("/get-uid/")
def get_uid():
    global uid_counter
    uid_counter += 1
    return {"uid": uid_counter - 1}


@app.route("/upload_picture/", methods=["POST"])
def upload_picture():
    global THE_TABLE
    uploaded_picture = request.files.get("picture")
    if uploaded_picture and uploaded_picture.mimetype.startswith("image/"):
        try:
            # TODO: the html template is trying to search under static folder - fix the path!
            filename = os.path.join(
                app.config["UPLOAD_FOLDER"], secure_filename(uploaded_picture.filename)
            )
            uploaded_picture.save(filename)
            THE_TABLE = Table(filename)
            return redirect("/add_names", 200)
        except IOError:
            return {"message": "<p> internal server file error :( </p>"}

    return "internal error."


@app.route("/table_details", methods=["GET"])
def table_details():
    global THE_TABLE
    # render_template('tableDetails.html', table=THE_TABLE)
    return redirect("/add_names", 200)


def add_name_to_list(name):
    script = f"<script>addNameToList('{name}');</script>"
    return script


@app.route("/add_names/", methods=["GET", "POST"])
def add_names():
    global names_counter
    if request.method == "GET":
        return render_template("addNames.html")  # Render name collection page
    else:
        name = request.form.get("name")
        if name:
            names_dict[names_counter] = name  # Add name to dictionary
            print(f"Name added: {name}")

            # Call JavaScript function to add name to the list
            add_name_to_list(name)
            names_counter += 1
            print(names_dict)

        if "done" in request.form:  # Check if "Done" button is pressed
            if len(names_dict) > len(THE_TABLE.spots):
                print("there are to many guests for this table")
                names_dict.clear()
                return redirect("/preferences")
            return redirect("/preferences", 200)  # Redirect to table details
        return redirect("/add_names")  # Redirect back to name collection page


@app.route("/preferences", methods=["GET", "POST"])
def preferences():
    global names_dict, person_matrix
    form = MainForm()
    if form.validate_on_submit():
        # Process the data
        pairs_data = [
            (pair["name1"], pair["name2"], pair["like"]) for pair in form.pairs.data
        ]
        # Here you can do something with the pairs_data, like saving to a database
        print(pairs_data)
        return f"Data received: {pairs_data}"
    return render_template("forms-test.html", form=form)
    # p1index = request.form.get('name1')
    # p2index = request.form.get('name2')
    # preference = request.form.get('preference')
    # print(p1index, " ", p2index, " ", preference)
    # if p1index == p2index:
    #     return render_template('addCons.html', names=names_dict.values(), error="Please select two diffrent names")
    # else:
    #     isLike = 'like' == preference
    #     updatePersonsMatrix(person_matrix, p1index, p2index, isLike)
    #     if 'done' in request.form:
    #         findSitting(THE_TABLE, person_matrix)


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
