from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# This creates an instance of the application
app = Flask(__name__)

# __file__ is equal to the file being executed
basedir = os.path.abspath(os.path.dirname(__file__))
breakpoint()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'crud.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)


# __name__ is a special name in Python. If it equals to '__main__',
# it means that program is being executed as the main program

@app.route("/")
def hello():
    return "hello world"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(150), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email


class UserSchema(ma.Schema):
    class Meta:
        # expose these to json
        fields = ("id", "username", "email")


# Control what you want to show in your json
user_schema = UserSchema(exclude=["email"])

users_schema = UserSchema(many=True)
users_emails_schema = UserSchema(many=True, exclude=["username"])


# Endpoint to create a new user
@app.route('/user', methods=["POST"])
def add_user():
    username = request.json["username"]
    email = request.json["email"]

    new_user = User(username, email)

    db.session.add(new_user)
    db.session.commit()

    all_users = User.query.all()

    return users_schema.jsonify(all_users)


@app.route('/users', methods=["GET"])
def get_users():
    all_users = User.query.all()

    return users_schema.jsonify(all_users)


@app.route('/users/emails', methods=["GET"])
def get_users_emails():
    users = User.query.all()

    return users_emails_schema.jsonify(users)


# <parameter> to be put inside the function
@app.route('/user/<id>', methods=["GET"])
def get_user_by_id(id):
    user = User.query.get(id)

        return user_schema.jsonify(user)


@app.route('/user/<id>', methods=["PUT"])
def update_user_by_id(id):
    user = User.query.get(id)

    username = request.json['username']
    email = request.json['email']

    user.username = username
    user.email = email

    db.session.add(user)
    db.session.commit()

    return user_schema.jsonify(user)


@app.route('/user/<id>', methods=["DELETE"])
def delete_user_by_id(id):
    user = User.query.get(id)

    db.session.delete(user)
    db.session.commit()
    users = User.query.all()

    return users_schema.jsonify(users)


if (__name__ == '__main__'):
    app.run(debug=True)
