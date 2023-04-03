#!/bin/python3
from flask import Flask,jsonify,request
import re
import json
from uuid import uuid4

# ---------------------------------------------------------------------------- #
#                                 Static Datas                                 #
# ---------------------------------------------------------------------------- #
# ----------------------------------- Mock ----------------------------------- #
user={
  "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
  "email": "john.doe@example.com",
  "password": "2986b7f0cd0ba9827ace0810c8818825",
  "roles": 
    [
      "admin",
      "player"
    ]
  ,
  "description": "I am John Doe"
}

users=[
  {
    "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
    "email": "john.doe@example.com",
    "password": "2986b7f0cd0ba9827ace0810c8818825",
    "roles": 
      [
        "admin",
        "player"
      ]
    ,
    "description": "I am John Doe"
  }
]

jwt={
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
}

roles=[
  "admin",
  "player"
]

# --------------------------------- StaticDB --------------------------------- #
usersDB=[
  {
  "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
  "email": "john.doe@example.com",
  "password": "2986b7f0cd0ba9827ace0810c8818825",
  "roles": 
    [
      "admin",
      "player"
    ]
  ,
  "description": "I am John Doe"
},
  {
  "id_user": "026a5b74-06a1-4a27-acb8-e87683ea9fce",
  "email": "doe.john@example.com",
  "password": "2986b7f0cd0ba9827ace0810c8818825",
  "roles": 
    [
      "admin"
    ]
  ,
  "description": "I am John Doe"
},
  {
  "id_user": "fa3a4a70-2773-41ac-8c42-4d69f6c2ca6e",
  "email": "marvelous@example.com",
  "password": "2986b7f0cd0ba9827ace0810c8818825",
  "roles": 
    [
      "player"
    ]
  ,
  "description": "I am John Doe"
}
]


# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #

def check_user_is_well_formed(user):
  whatGood={"id_user":False,"email":False,"password":False,"roles":True,"description":False}
  uuidRegex=re.compile(r'^[0-9a-fA-F]{8}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{4}\b-[0-9a-fA-F]{12}$')
  emailRegex=re.compile(r"^(?P<identifiant>[\w\-\.\+]+)@(?P<operateur>[\w\-\.]+\.(?P<TLD>[a-z]+))$")
  descriptionRegex=re.compile(r"^[\w \-àâçéèêëîïôûùüÿñæœ.]*$")
  rolesList=["admin","player"]
  if (uuidRegex.match(user["id_user"])):
    whatGood["id_user"]=True
  if (emailRegex.match(user["email"])):
    whatGood["email"]=True
  if(descriptionRegex.match(user["description"])):
    whatGood["description"]=True
  for role in user["roles"]:
    if not(role in rolesList):
      whatGood["roles"]=False
  return whatGood


# ----------------------------------- Model ---------------------------------- #
def check_email_not_exist(email):
  # Variables
  print()
  # Database



# ---------------------------------------------------------------------------- #
#                                Flask Skeleton                                #
# ---------------------------------------------------------------------------- #

app= Flask(__name__)


# ------------------------------------- / ------------------------------------ #

@app.route('/')
def default():
    return "Welcome to /users API from ctf401",200


# ---------------------------------- /users ---------------------------------- #

@app.route('/users')
def listUsers():
    return jsonify(users),200

@app.route('/users', methods=['POST'])
def createUser():
  try:
    data=request.get_json()
  except:
    return 'Bad JSON',400
  keyAllowed=["email","password","roles","description"]
  for key in data:
    if not(key in keyAllowed):
      return 'Bad JSON',400
  id_user=uuid4()
  userToBeCreated=data
  userToBeCreated["id_user"]=id_user
  
  return jsonify(user),200

@app.route('/users/login')
def loginUser():
    return jsonify(jwt),200

@app.route('/users/logout')
def logoutUser():
    return 'successful operation',200

@app.route('/users/<userid>', methods=['GET'])
def getUserById(userid):
    return jsonify(user),200

@app.route('/users/<userid>', methods=['PUT'])
def updateUser(userid):
    return jsonify(user),200

@app.route('/users/<userid>', methods=['PATCH'])
def updatePatchUser(userid):
    return jsonify(user),200

@app.route('/users/<userid>', methods=['DELETE'])
def deleteUser(userid):
    return 'successful operation',200

@app.route('/users/<userid>/roles')
def getUserRoleById(userid):
    return jsonify(roles),200


# ---------------------------------------------------------------------------- #
#                                   Oprations                                  #
# ---------------------------------------------------------------------------- #


if __name__=="__main__":
    app.run(host="0.0.0.0")
