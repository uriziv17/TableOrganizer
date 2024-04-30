import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from actions.indentifiers.indenty import sayHello
from Table import Table

# TODO hide behind a lock
uid_counter = 1

app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/template')

app.config['UPLOAD_FOLDER'] = os.path.join('web', 'static', 'uploads')

THE_TABLE = None

@app.route('/')
def getHomePage():
    sayHello()
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
            return redirect('/table_details', 200)
        except IOError:
            return "<p> internal server file error :( </p>"
    
    return "internal error."

@app.route('/table_details', methods=['GET'])
def table_details():
    global THE_TABLE
    return render_template('tableDetails.html', table=THE_TABLE)

def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()