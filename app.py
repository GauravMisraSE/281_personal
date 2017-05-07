from flask import session
from shutil import move,copy,rmtree
import os
from subprocess import check_output
from flask import Flask, request, redirect, url_for, flash, render_template,send_file,make_response,Response
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/ubuntu/281_personal'
ALLOWED_EXTENSIONS = set(['zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods = (['POST','GET']))
def upload_file():
    if request.method == 'GET':
	return "Instance is healthy"
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "No file found"
            # return redirect(request.url)
        datafile = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if datafile.filename == '':
            flash('No selected file')
            return "No file found"
            #return redirect(request.url)
        if datafile and allowed_file(datafile.filename):
            filename = secure_filename(datafile.filename)
            datafile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print filename
            folder = filename.rsplit('.', 1)[0].lower()
            print ("folder name is",folder)
            print ("current working directory is ", (check_output(['pwd'])))
            make_folder = check_output(['mkdir', folder])
            print 'unzipping'
            out1 = check_output(['unzip', filename, '-d', folder])
            print 'unzipping done'
            cd2 = os.chdir("/home/ubuntu/281_personal/parser")
            check_output(['./umlparser.sh', '/home/ubuntu/281_personal/'+ folder + '/', folder])
            copy('/home/ubuntu/281_personal/parser/'+folder+'.png','/home/ubuntu/281_personal/static/')
	    cd3 = os.chdir("/home/ubuntu/281_personal")
	    rmtree("home/ubuntu/281_personal/test1",ignore_errors=True)
	    rmtree("home/ubuntu/281_personal/test2",ignore_errors=True)
	    rmtree("home/ubuntu/281_personal/test3",ignore_errors=True)
	    rmtree("home/ubuntu/281_personal/test4",ignore_errors=True)
	    rmtree("home/ubuntu/281_personal/test5",ignore_errors=True) 
            return (folder+'.png',{'Access-Control-Allow-Origin':'*'})
	    #return "http://52.10.23.13:5000/static/img/"+folder+".png"
	    #return filename.capitalize()
            #return render_template('diagram.html',img = folder+'.png')
            #return redirect(url_for('upload_file'))
            #return "file successfully saved"
        else:
            return "Unexpected file attached"


@app.route('/view/<string:imgname>', methods = (['GET']))
def getimage(imgname):
    #folder = imgname.rsplit('.', 1)[0].lower()
    #rmtree('/'+folder)
    url = '/home/ubuntu/281_personal/static/'+imgname
    #response = make_response(send_file(url))
    #response.headers.add("Access-Control-Allow-Origin", "*")
    #response = Response(response=send_file(url, mimetype='image/png'),status= 200, headers={'Access-Control-Allow-Origin': '*'}, mimetype='image/png')
    #return response  
    
    response = make_response(send_file(url, mimetype='image/png'))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response
    #return ((send_file(url, mimetype='image/png')),{'Access-Control-Allow-Origin':'*'})
    #response = Response(response = send_file(url),status = 200, {'Access-Control-Allow-Origin': '*'})
    #return send_file(url, mimetype='image/png'), 200, {'Access-Control-Allow-Origin': '*'}

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port=5000, debug=True)


