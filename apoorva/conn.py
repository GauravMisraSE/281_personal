from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://******:*******@personal281.cgqm4wyqzown.us-west-2.rds.amazonaws.com:3306/personal281'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Grades(db.Model):
    __tablename__ = 'tenant_data'
    record_id = db.Column('record_id', db.String(45), nullable=False, primary_key=True)
    tid = db.Column('tid', db.String(45), nullable=False, primary_key=True)
    tenant_table = db.Column('tenant_table', db.String(45))
    col1 = db.Column('col1', db.String(200))
    col2 = db.Column('col2', db.String(200))
    col3 = db.Column('col3', db.String(200))
    col4 = db.Column('col4', db.String(200))
    col5 = db.Column('col5', db.String(200))
    col6 = db.Column('col6', db.String(200))
    col7 = db.Column('col7', db.String(200))
    col8 = db.Column('col8', db.String(200))
    col9 = db.Column('col9', db.String(200))
    col10 = db.Column('col10', db.String(200))

    def __init__(self, tid, tenant_table, col1, col2, col3, col4, col5, col6, col7, col8, col9, col10):
        # initialize columns
        self.record_id = str(uuid.uuid1())
        self.tid = tid
        self.tenant_table = tenant_table
        self.col1 = col1
        self.col2 = col2
        self.col3 = col3
        self.col4 = col4
        self.col5 = col5
        self.col6 = col6
        self.col7 = col7
        self.col8 = col8
        self.col9 = col9
        self.col10 = col10
