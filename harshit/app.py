from flask import session
from shutil import move,copy,rmtree
import os
from subprocess import check_output,call
from flask import Flask, request, redirect, url_for, flash, render_template,send_file,make_response,Response
from werkzeug.utils import secure_filename
from conn import Grades, db
from sqlalchemy.exc import IntegrityError
import uuid
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine,inspect


Session = sessionmaker()

engine = create_engine('mysql://******:*******@personal281.cgqm4wyqzown.us-west-2.rds.amazonaws.com:3306/personal281')


UPLOAD_FOLDER = '/home/ubuntu/281_personal'
ALLOWED_EXTENSIONS = set(['zip'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


class SomeTest:
    def setUp(self, grades):
        # connect to the database
        self.connection = engine.connect()

        # begin a non-ORM transaction
        #self.trans = self.connection.begin()

        # bind an individual Session to the connection
        self.session = Session(bind=self.connection)
        print "session is now bound"
        insp = inspect(grades)
        print insp.persistent
        print insp.detached
        print insp.pending
        print insp.transient

        self.session.add(grades)
        print insp.pending
        for obj in self.session:
            print obj
        self.session.commit()
        self.session.flush()
        print insp.detached
        print insp.deleted
        self.session.close()
        self.connection.close()

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
            print 'inside parser directory'
            print ("current working directory is ", (check_output(['pwd'])))
            call(["java","-jar","202UmlParser.jar","umlparser","/home/ubuntu/281_personal/"+folder,"/home/ubuntu/281_personal/parser/"+folder])
            copy('/home/ubuntu/281_personal/parser/'+folder+'.png','/home/ubuntu/281_personal/static/')
            cd3 = os.chdir("/home/ubuntu/281_personal")
            print ("path before removal of folder ", (check_output(['pwd'])))
            rmtree("/home/ubuntu/281_personal/test1",ignore_errors=True)
            rmtree("/home/ubuntu/281_personal/test2",ignore_errors=True)
            rmtree("/home/ubuntu/281_personal/test3",ignore_errors=True)
            rmtree("/home/ubuntu/281_personal/test4",ignore_errors=True)
            return (folder+'.png',{'Access-Control-Allow-Origin':'*'})
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


@app.route('/grade', methods = (['POST','GET','OPTIONS']))
def grader():
    if request.method == 'OPTIONS':
            return ( '',200, \
                   { 'Access-Control-Allow-Origin': '*', \
                     'Access-Control-Allow-Headers':'Origin, X-Requested-With, Content-Type, Accept', \
                     'Access-Control-Allow-Methods': 'POST,GET'})


    if request.method == 'GET':
        resp = Response("Foo bar baz")
        return ('ok', {'Access-Control-Allow-Origin': '*'})

    try:
        x = request.get_json(force=True)
        grades = Grades(
            "harshit",
            "t-harshit",
            x['col1'],
            x['col2'],
            x['col3'],
            x['col4'],
            x['col5'],
            x['col6'],
            x['col7'],
            x['col8'],
            x['col9'],
            x['col10'],
            )
        s = SomeTest()
        s.setUp(grades)
        print "setUp() executed"
    # s.test_something(grades)
        print "added to server db"
    # db.session.add(grades)
            #db.session.commit()
        return ('Added remarks to DB',{'Access-Control-Allow-Origin':'*'})
    except IntegrityError:
                db.session.rollback()
                response = 'not ok'
                response.headers['Access-Control-Allow-Origin'] = '*'
                return response


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host="0.0.0.0", port=5000, debug=True)


