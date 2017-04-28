import os
from subprocess import check_output
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/gaurav/281_personal/'
ALLOWED_EXTENSIONS = set(['zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'datafile' not in request.files:
            flash('No file part')
            return "No file found"
            # return redirect(request.url)
        datafile = request.files['datafile']
        # if user does not select file, browser also
        # submit a empty part without filename
        if datafile.filename == '':
            flash('No selected file')
            return "No file found"
            #return redirect(request.url)
        if datafile and allowed_file(datafile.filename):
            filename = secure_filename(datafile.filename)
            print filename
            datafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            folder = filename.rsplit('.', 1)[0].lower()
            print folder
            make_folder = check_output(['mkdir', folder])
            out1 = check_output(['unzip', filename, '-d', folder])
            cd =  check_output(['cd', 'parser'])
            execute = check_output(['./umlparser.sh', '../', folder])
            return filename.capitalize()
            #return render_template('front.html')
            #return redirect(url_for('upload_file'))
            #return "file successfully saved"
        else:
            return "Unexpected file attached"
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
