from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
app = Flask(__name__, template_folder='template')

app.secret_key = 'secretKeyT'

@app.route('/')
def welcome():
    return render_template('welcome.html')
@app.route('/', methods=['POST'])
def upload_picture():
    uploaded_picture = request.files.get('picture')
    if uploaded_picture:
        if uploaded_picture.mimetype.startswith('image/'):
            uploaded_picture.save(f'/uploads{secure_filename(uploaded_picture.filename)}')
            return render_template('confirm.html', image_tablePicture='uploads/uploaded_picture')
        else:
            return "please upload an image!"
    else:
        return "please choose a picture!"
@app.route('/confirm/<tablePicture>', methods=["POST"])
def confirm(tablePicture):
    confirmation = request.form.get('confirmation')
    if confirmation == "yes":
        return f"image {tablePicture} has been confirmed!"
    else:
        return redirect(render_template('welcome.html'))
if __name__ == '__main__':
    app.run(debug=True)