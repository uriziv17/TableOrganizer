from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
from actions.indentifiers.indenty import sayHello

# TODO hide behind a lock
uid_counter = 1

app = Flask(__name__,
            static_folder='web/static',
            template_folder='web/template')

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
    uploaded_picture = request.files.get('picture')
    if uploaded_picture and uploaded_picture.mimetype.startswith('image/'):
        uploaded_picture.save(f'uploads//{secure_filename(uploaded_picture.filename)}')
        return redirect('/', 200)
    
    return "internal error."
    
def main():
    app.run(debug=True)

if __name__ == '__main__':
    main()