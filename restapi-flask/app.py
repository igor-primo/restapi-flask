from flask import Flask, jsonify
from flask_restful import Resource, Api, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
import re

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('first_name', type=str, required=True, help='This field cannot be blank')
_user_parser.add_argument('last_name', type=str, required=True, help='This field cannot be blank')
_user_parser.add_argument('cpf', type=str, required=True, help='This field cannot be blank')
_user_parser.add_argument('email', type=str, required=True, help='This field cannot be blank')
_user_parser.add_argument('birth_date', type=str, required=True, help='This field cannot be blank')

app = Flask(__name__)
api = Api(app)

app.config['MONGODB_SETTINGS'] = {
    "db": "users",
    "host": "mongodb",
    "port": 27017,
    "username": "admin",
    "password": "admin"
}
db = MongoEngine(app)

class UserModel(db.Document):
    cpf = db.StringField(required=True, unique=True)
    email = db.StringField(required=True)
    first_name = db.StringField(required=True, max_length=50)
    last_name = db.StringField(required=True, max_length=50)
    birth_date = db.DateTimeField(required=True)

class Users(Resource):
    def get(self):
        return {'message': 'user 1'}

class User(Resource):
    def validate_cpf(self, cpf):
        if re.findall("([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})", cpf):
            return True
        return False

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data.cpf):
            return {'message': 'CPF is invalid'}, 400

        try:
            response = UserModel(**data).save()
            return {'message': 'User %s successfully created.' % response.id}
        except NotUniqueError:
            return {'message': 'CPF already exists in the database.'}

api.add_resource(Users, '/users')
api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")