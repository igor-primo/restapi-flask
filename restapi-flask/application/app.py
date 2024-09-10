from flask import Flask, jsonify
from flask_restful import Resource, reqparse
from flask_mongoengine import MongoEngine
from mongoengine import NotUniqueError
from .model import UserModel
import re

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "first_name", type=str, required=True, help="This field cannot be blank"
)
_user_parser.add_argument(
    "last_name", type=str, required=True, help="This field cannot be blank"
)
_user_parser.add_argument(
    "cpf", type=str, required=True, help="This field cannot be blank"
)
_user_parser.add_argument(
    "email", type=str, required=True, help="This field cannot be blank"
)
_user_parser.add_argument(
    "birth_date", type=str, required=True, help="This field cannot be blank"
)

app = Flask(__name__)


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def validate_cpf(self, cpf):
        if re.findall(
            "([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})",
            cpf,
        ):
            return True
        return False

    def post(self):
        data = _user_parser.parse_args()

        if not self.validate_cpf(data.cpf):
            return {"message": "CPF is invalid"}, 400

        try:
            response = UserModel(**data).save()
            return {"message": "User %s successfully created." % response.id}
        except NotUniqueError:
            return {"message": "CPF already exists in the database."}

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf)

        if response:
            return jsonify(response)
        return {"message": "User does not existe in database"}
