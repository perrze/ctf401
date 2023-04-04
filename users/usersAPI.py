#!/bin/python3
from flask import Flask, jsonify, request
import re
from uuid import uuid4
import logging
import hashlib
import jwt
from os import getenv, environ
from time import time
import requests
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

# jwt = {
#     "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
# }

roles = [
    "admin",
    "player"
]

hasAccess = {
    "hasAccess": True
}

# --------------------------------- StaticDB --------------------------------- #
usersDB = [
    {
        "description": "I am John Doe",
        "email": "admin@ctf401.fr",
        "id_user": "b94f1662-04f7-4150-9d99-afa21bc8ec0e",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    },
    {
        "description": "I am John Doe",
        "email": "player@ctf401.fr",
        "id_user": "31a1d300-4224-4f5b-a1ab-94129f264cc6",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "player"
        ]
    },
    {
        "description": "I am John Doe",
        "email": "player+admin@ctf401.fr",
        "id_user": "f7d972ec-fbcb-4be3-a1f6-64dd28f1b449",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "player",
            "admin"
        ]
    }
]

jwtDB = {

}

variables = True

# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #


def check_user_is_well_formed(user, verifyPassword=True):
    notBad = True
    whatGood = {"id_user": True, "email": True,
                "password": True, "roles": True, "description": True}
    uuidRegex = re.compile(
        r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$')
    emailRegex = re.compile(
        r"^(?P<identifiant>[\w\-\.\+]+)@(?P<operateur>[\w\-\.]+\.(?P<TLD>[a-z]+))$")
    descriptionRegex = re.compile(r"^[\w \-àâçéèêëîïôûùüÿñæœ.]*$")
    passwordRegex = re.compile(
        r"^(?=[^a-z]*[a-z])(?=[^A-Z]*[A-Z])(?=\D*\d)(?=[^!\^#%@?°€$£*-]*[!\^#%&@?°€$£*-])[A-Za-z0-9!\^#%@?°€$£*-]{8,128}$")
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
    if verifyPassword:  # Used for Patch because hash not matching
        if not (passwordRegex.match(user["password"])):
            logging.debug('Password regex False')
            notBad = False
            whatGood["password"] = False
    return [notBad, whatGood]


def check_uuid_is_well_formed(userid):
    uuidRegex = re.compile(
        r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$')
    if uuidRegex.match(userid):
        return True
    else:
        return False


def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()


def encode_jwt(userid, SECRET_KEY):
    expire = time()+86400  # Now + 40h
    tokenid = str(uuid4())
    token = jwt.encode({"id_user": userid, "id_token": tokenid,
                       "expire": expire}, SECRET_KEY, algorithm="HS256")
    return token

def check_if_user_access(request,role):
  token = None
  if "jwt" in request.headers:
      token = request.headers["jwt"]
  if not token:
      return False
  result = requests.post(BASE_URL+"/users/check/"+role,json={"token":token})
  if result.status_code==200:
    return True
  else:
    return False

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


def get_users_list():
    # Variables
    if variables:
        return usersDB
    else:
        print()


def add_user(user):
    # Variables
    if variables:
        usersDB.append(user)
    # Databse
    else:
        print()


def get_properties_from_userid(userid):
    # Variables
    if variables:
        for user in usersDB:
            if user["id_user"] == userid:
                return user
        return False
    # Database
    else:
        print()


def return_position_in_array_user(userid):
    for i in range(len(usersDB)):
        if usersDB[i]["id_user"] == userid:
            return i


def modify_user(userid, user):
    # Variables
    if variables:
        position = return_position_in_array_user(userid)
        usersDB[position] = user
    # Database
    else:
        print()


def delete_user(userid):
    # Variables
    if variables:
        position = return_position_in_array_user(userid)
        usersDB.pop(position)
    # Database
    else:
        print()


def add_jwt_db(token, tokenid):
    # Variables
    if variables:
        jwtDB[tokenid] = token
    # Database
    else:
        print()


def remove_jwt_db(tokenid):
    # Variables
    if variables:
        jwtDB.pop(tokenid)
    # Database
    else:
        print()


def check_user_has_role(userid, role):
    # Variables
    if variables:
        for user in usersDB:
            if user["id_user"] == userid:
                if role in user["roles"]:
                    return True
                else:
                    return False
        return False
    # Database
    else:
        print()


def check_connection(email, hashed):
    # Variables
    if variables:
        for user in usersDB:
            if user["email"] == email and user["password"] == hashed:
                return user["id_user"]
        return False
    # Database
    else:
        print()


# ---------------------------------------------------------------------------- #
#                                Flask Skeleton                                #
# ---------------------------------------------------------------------------- #
app = Flask(__name__)
if "SECRET_KEY" in environ:
    SECRET_KEY = getenv("SECRET_KEY")
else:
    SECRET_KEY = 'this is a secret'
if "BASE_URL" in environ:
  BASE_URL = getenv("BASE_URL")
else:
  BASE_URL = "http://10.0.0.5:5000"
logging.debug("SECRET_KEY = "+SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY


# ------------------------------------- / ------------------------------------ #


@app.route('/')
def default():
    return "Welcome to /users API from ctf401", 200


# ---------------------------------- /users ---------------------------------- #

@app.route('/users')
def listUsers():
    return jsonify(get_users_list()), 200


@app.route('/users/create', methods=['POST'])
def createUser():
    if not(check_if_user_access(request,"admin")):
      return "Unauthorized", 401
    try:
        data = request.get_json()
    except:
        return 'Bad JSON', 400
    keyAllowed = ["email", "password", "roles", "description"]
    if len(data) != 4:
        return 'Bad JSON', 400
    for key in data:
        if not (key in keyAllowed):
            return 'Bad JSON', 400
    id_user = str(uuid4())
    userToBeCreated = data
    userToBeCreated["id_user"] = id_user
    result = check_user_is_well_formed(userToBeCreated)

    if not (check_email_not_exist(userToBeCreated["email"])):
        logging.debug('Email exist True')
        result[0] = False
        result[1]["email"] = False

    if result[0]:
        userToBeCreated["password"] = hashlib.md5(
            userToBeCreated["password"].encode()).hexdigest()
        add_user(userToBeCreated)
        # print(usersDB)
        return jsonify(userToBeCreated), 200
    else:
        logging.debug(' Was Bad')
        return jsonify(result[1]), 409


@app.route('/users/login')
def loginUser():
    email = request.args.get('email')
    password = request.args.get('password')
    hashed = hash_password(password)
    if userid := check_connection(email, hashed):
        token = encode_jwt(userid, app.config["SECRET_KEY"])
        return ({"token": token}), 200
    else:
        return "Invalid username/password supplied", 401
    # return jsonify(jwt), 200


@app.route('/users/logout')
def logoutUser():
    # Nothing to do because no Database of token
    return 'successful operation', 200


@app.route('/users/<userid>', methods=['GET'])
def getUserById(userid):
    if not (check_uuid_is_well_formed(userid)):
        return 'Invalid id_user supplied', 400
    user = get_properties_from_userid(userid)
    if user:
        return jsonify(user), 200
    else:
        return 'User not found', 404


@app.route('/users/<userid>', methods=['PUT'])
def updateUser(userid):
    try:
        data = request.get_json()
    except:
        return 'Bad JSON', 400
    keyAllowed = ["id_user", "email", "password", "roles", "description"]
    if len(data) != 5:
        return 'Bad JSON', 400
    for key in data:
        if not (key in keyAllowed):
            return 'Bad JSON', 400
    if not (check_uuid_is_well_formed(userid)):
        return 'Invalid id_user supplied', 400
    user = get_properties_from_userid(userid)
    if user:
        if (data["id_user"] != user["id_user"]):
            return 'Do not modify id_user', 400
        notBad, whatGood = check_user_is_well_formed(data)
        if (notBad):
            data["password"] = hash_password(data["password"])
            for key in data:
                user[key] = data[key]
            modify_user(userid, data)
            return jsonify(user), 200
        else:
            return jsonify(whatGood), 409

    else:
        return 'User not found', 404


@app.route('/users/<userid>', methods=['PATCH'])
def updatePatchUser(userid):
    try:
        data = request.get_json()
    except:
        return 'Bad JSON', 400
    keyAllowed = ["id_user", "email", "password", "roles", "description"]
    if len(data) > 5:
        return 'Bad JSON', 400
    for key in data:
        if not (key in keyAllowed):
            return 'Bad JSON', 400

    if not (check_uuid_is_well_formed(userid)):
        return 'Invalid id_user supplied', 400
    user = get_properties_from_userid(userid)
    if user:
        try:
            if (data["id_user"] != user["id_user"]):
                return 'Do not modify id_user', 400
        except:
            logging.debug("No id_user given")
        for key in data:
            user[key] = data[key]
        verifyPassword = True
        if not ("password" in data):
            verifyPassword = False
        notBad, whatGood = check_user_is_well_formed(
            user, verifyPassword=verifyPassword)
        if (notBad):
            if verifyPassword:
                user["password"] = hash_password(data["password"])
            modify_user(userid, user)
            return jsonify(user), 200
        else:
            return jsonify(whatGood), 409
    else:
        return 'User not found', 404


@app.route('/users/<userid>', methods=['DELETE'])
def deleteUser(userid):
    if not (check_uuid_is_well_formed(userid)):
        return 'Invalid id_user supplied', 400
    user = get_properties_from_userid(userid)
    if user:
        delete_user(userid)
        return 'successful operation', 200
    else:
        return 'User not found', 404


@app.route('/users/<userid>/roles')
def getUserRoleById(userid):
    if not (check_uuid_is_well_formed(userid)):
        return 'Invalid id_user supplied', 400
    user = get_properties_from_userid(userid)
    if user:
        roles = {"roles": user["roles"]}
        return jsonify(roles), 200
    else:
        return 'User not found', 404


@app.route('/users/check/<access>', methods=["POST"])
def checkUser(access):
    token=request.get_json()["token"]
   
    logging.debug("Token Received: "+token)
    print(token)
    # with open("./test","w") as f:
    #   f.write(token)
    try:
      data = jwt.decode(
          token, app.config["SECRET_KEY"], algorithms="HS256")
      # data = jwt.decode(token, 'this is a secret', algorithms="HS256")
      expire = data["expire"]
      current_time = time()
      if current_time > expire:
          # remove_jwt_db(tokenid)
          return "Token Expired", 401

      userid = data["id_user"]
      # tokenid=data["id_token"]
      logging.debug("Data: "+str(data))
      if userid is None:
          return "Invalid Authentication token!", 401
      if check_uuid_is_well_formed(access):
          if access == userid:
              return jsonify({"hasAccess": True}), 200
          return jsonify({"hasAccess": False}), 401
      if check_user_has_role(userid, access):
          return jsonify({"hasAccess": True}), 200
      else:
          return jsonify({"hasAccess": False}), 401
    except Exception as e:
        return "Invalid Authentication token!", 401


# ---------------------------------------------------------------------------- #
#                                   Oprations                                  #
# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0")
