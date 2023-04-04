#!/bin/python3
from flask import Flask, jsonify, request
import re
import json
from uuid import uuid4
import logging
import hashlib
# ---------------------------------------------------------------------------- #
#                                 Static Datas                                 #
# ---------------------------------------------------------------------------- #
# ----------------------------------- Mock ----------------------------------- #
user = {
    "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
    "email": "john.doe@example.com",
    "password": "2986b7f0cd0ba9827ace0810c8818825",
    "roles":
    [
        "admin",
        "player"
    ],
    "description": "I am John Doe"
}

users = [
    {
        "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
        "email": "john.doe@example.com",
        "password": "2986b7f0cd0ba9827ace0810c8818825",
        "roles":
        [
            "admin",
            "player"
        ],
        "description": "I am John Doe"
    }
]

jwt = {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}

roles = [
    "admin",
    "player"
]

# --------------------------------- StaticDB --------------------------------- #
usersDB = [
    {
        "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
        "email": "john.doe@example.com",
        "password": "2986b7f0cd0ba9827ace0810c8818825",
        "roles":
        [
            "admin",
            "player"
        ],
        "description": "I am John Doe"
    },
    {
        "id_user": "026a5b74-06a1-4a27-acb8-e87683ea9fce",
        "email": "doe.john@example.com",
        "password": "2986b7f0cd0ba9827ace0810c8818825",
        "roles":
        [
            "admin"
        ],
        "description": "I am John Doe"
    },
    {
        "id_user": "fa3a4a70-2773-41ac-8c42-4d69f6c2ca6e",
        "email": "marvelous@example.com",
        "password": "2986b7f0cd0ba9827ace0810c8818825",
        "roles":
        [
            "player"
        ],
        "description": "I am John Doe"
    }
]

variables=True

# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #

def check_user_is_well_formed(user):
    notBad = True
    whatGood = {"id_user": True, "email": True,
                "password": True, "roles": True, "description": True}
    uuidRegex = re.compile(
        r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$')
    emailRegex = re.compile(
        r"^(?P<identifiant>[\w\-\.\+]+)@(?P<operateur>[\w\-\.]+\.(?P<TLD>[a-z]+))$")
    descriptionRegex = re.compile(r"^[\w \-àâçéèêëîïôûùüÿñæœ.]*$")
    passwordRegex = re.compile(r"^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!\^#%@?°€$£*-]*[!\^#%&@?°€$£*-])[A-Za-z0-9!\^#%@?°€$£*-]{8,128}$")
    rolesList = ["admin", "player"]
    if not (uuidRegex.match(user["id_user"])):
        logging.debug(' UUID regex False')
        notBad = False
        whatGood["id_user"] = False
    if not (emailRegex.match(user["email"])):
        logging.debug(' Email regex False')
        notBad = False
        whatGood["email"] = False
    if not (descriptionRegex.match(user["description"])):
        logging.debug(' Description regex False')
        notBad = False
        whatGood["description"] = False
    for role in user["roles"]:
        if not (role in rolesList):
            logging.debug(' Roles regex False')
            notBad = False
            whatGood["roles"] = False
    if not (passwordRegex.match(user["password"])):
      logging.debug('Password regex False')
      notBad=False
      whatGood["password"] = False
    return [notBad, whatGood]


# ----------------------------------- Model ---------------------------------- #
def check_email_not_exist(email):
    # Variables
    if (variables):
      for user in usersDB:
        # print("USER EMAIL" + user["email"])
        # print("ADDING EMAIL" + email)
        if user["email"] == email:
            return False
      return True
    # Database
    else:
      print()
      
def add_user_to_db(user):
  # Variables
  if variables:
    usersDB.append(user)
  # Databse  
  else:
    print()


# ---------------------------------------------------------------------------- #
#                                Flask Skeleton                                #
# ---------------------------------------------------------------------------- #

app = Flask(__name__)


# ------------------------------------- / ------------------------------------ #

@app.route('/')
def default():
    return "Welcome to /users API from ctf401", 200


# ---------------------------------- /users ---------------------------------- #

@app.route('/users')
def listUsers():
    return jsonify(users), 200


@app.route('/users/create', methods=['POST'])
def createUser():
    try:
        data = request.get_json()
    except:
        return 'Bad JSON', 400
    keyAllowed = ["email", "password", "roles", "description"]
    for key in data:
        if not (key in keyAllowed):
            return 'Bad JSON', 400
    id_user = str(uuid4())
    userToBeCreated = data
    userToBeCreated["id_user"] = id_user
    result = check_user_is_well_formed(userToBeCreated)

    if not(check_email_not_exist(userToBeCreated["email"])):
        logging.debug('Email exist True')
        result[0] = False
        result[1]["email"] = False

    if result[0]:
        userToBeCreated["password"]=hashlib.md5(userToBeCreated["password"].encode()).hexdigest()
        add_user_to_db(userToBeCreated)
        # print(usersDB)
        return jsonify(userToBeCreated), 200
    else:
        logging.debug(' Was Bad')
        return jsonify(result[1]), 409


@app.route('/users/login')
def loginUser():
    return jsonify(jwt), 200


@app.route('/users/logout')
def logoutUser():
    return 'successful operation', 200


@app.route('/users/<userid>', methods=['GET'])
def getUserById(userid):
    return jsonify(user), 200


@app.route('/users/<userid>', methods=['PUT'])
def updateUser(userid):
    return jsonify(user), 200


@app.route('/users/<userid>', methods=['PATCH'])
def updatePatchUser(userid):
    return jsonify(user), 200


@app.route('/users/<userid>', methods=['DELETE'])
def deleteUser(userid):
    return 'successful operation', 200


@app.route('/users/<userid>/roles')
def getUserRoleById(userid):
    return jsonify(roles), 200


# ---------------------------------------------------------------------------- #
#                                   Oprations                                  #
# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0")
