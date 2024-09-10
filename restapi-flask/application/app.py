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


class Users(Resource):
    def get(self):
        return jsonify(UserModel.objects())


class User(Resource):
    def validate_cpf(self, cpf):
        return (
            re.search(
                r"\d{3}\.\d{3}\.\d{3}-\d{2}",
                cpf,
            )
            != None
        )

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
        return {"message": "User does not exist in database"}, 400
