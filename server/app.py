#!/usr/bin/env python3

from models import db, Activity, Camper, Signup
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/campers', methods = ['GET', 'POST'])
def campers():
    
    if request.method == 'GET':
        campers = Camper.query.all()

        response = make_response(
            campers.to_dict(),
            200
        )
    
    elif request.method == 'POST':
        form_data = request.get_json()
        # print(form_data)

        try:
            new_camper_obj = Camper(
                name = form_data['name'],
                age = form_data['age']
            )

            db.session.add(new_camper_obj)
            db.session.commit()
            response = make_response(
                new_camper_obj.to_dict(),
                201
            )
        except ValueError:
            response = make_response(
                {"validation errors" : None},
                403
            )
            return response
        
    return response

@app.route('/campers/<int:id>', methods = ['GET', 'PATCH'])
def campers_by_id(id):
    camper = Camper.query.filter(Camper.id == id).first()

    if camper:

        if request.method == 'GET':
            response = make_response(
                camper.to_dict(rules = ('-signup', )),
                200
            )

        elif request.method == 'PATCH':
            form_data = request.get_json()
            # print(form_data)

            try:
                for attr in form_data:
                    setattr(camper, attr, form_data.get(attr))

                db.session.commit()

                response = make_response(
                    camper.to_dict(),
                    201
                )
            except ValueError:

                response = make_response(
                    {"validation errors"},
                    404
                )
                return response
    else:
        response = make_response(
            {"Camper not found" : None},
            404
        )

    return response

     
@app.route('/activities', methods = ['GET'])
def activities():
    activities = Activity.query.all()

    response = make_response(
        activities.to_dict(),
        200
    )

    return response

@app.route('/activities/<int:id>', models = ['DELETE'])
def activity_by_id(id):
    activity = Activity.query.filter(Activity.id == id).first()

    if activity:

        activity_signups = Signup.query.filter(Signup.activity_id == id).all()

        for activity_signup in activity_signups:
            # print(activity_signup)
            db.session.delete(activity_signup)
        
        db.session.delete(activity)
        db.session.commit()

        response = make_response(
            {},
            202
        )
    else:

        response = make_response(
            {"Activity not found"},
            404
        )
    
    return response

@app.route('/signups', methods = ['POST'])
def signups():
    form_data = request.get_json()
    # print(form_data)

    try:
        new_signup_obj = Signup(
            camper_id = form_data['camper_id'],
            activity_id = form_data['activity_id'],
            time = form_data['time']
        )

        db.session.add(new_signup_obj)
        db.session.commit()

        response = make_response(
            new_signup_obj.to_dict(),
            201
        )
    except ValueError:
        response = make_response(
            {"validation errors" : None},
            403
        )
        return response
        
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
