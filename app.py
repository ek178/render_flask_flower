import json
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flowers.sqlite3'
app.config['SECRET_KEY'] = "random string"
CORS(app) 
db = SQLAlchemy(app)

# class Trees(db.Model):
#     id = db.Column('Tree_id', db.Integer, primary_key = True)
#     name = db.Column(db.String(100))
#     height=db.Column(db.String(20))

#     def __init__(self,name,height):
#         self.name = name
#         self.height = height

class Flower(db.Model):
    id = db.Column('flower_id',db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    color=db.Column(db.String(20))

    def __init__(self,name,color):
        self.name = name
        self.color = color


@app.route('/')
def home():
    return 'hello'

@app.route("/data/<ind>")
@app.route('/data/')
def open(ind=-1):
    if int(ind) > -1:
        flower=Flower.query.get(int(ind))
        return {"name":flower.name,"id":flower.id,"color":flower.color} 

    res=[]
    for flower in Flower.query.all():
        res.append({"id":flower.id,"name":flower.name,"color":flower.color})
    return res

@app.route('/new/', methods = ['GET','POST'])
def new():
    request_data = request.get_json()
    name= request_data["name"]
    color= request_data["color"]
 
    newFlower= Flower(name,color)
    db.session.add (newFlower)
    db.session.commit()
    return "a new rcord was create"

@app.route("/del/<ind>/", methods=['DELETE'])
def del_flower(ind=-1):
        flower=Flower.query.get(int(ind))
        if flower:
            db.session.delete(flower)
            db.session.commit()
            return f"the {flower.name} was deleted"
        return f"no such student"

@app.route("/upd/<ind>/", methods=['PUT'])
def upd_flower(ind=-1):
    if int(ind) > -1:
        data = request.json
        uname = (data["name"])
        uclolor = (data["color"])
        flower=Flower.query.get(int(ind))
        if flower:
            flower.name=uname
            flower.color=uclolor
            db.session.commit()
            return "flower updated"
        return "or none"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

