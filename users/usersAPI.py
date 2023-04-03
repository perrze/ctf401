#!/bin/python3
from flask import Flask,jsonify,request

# ---------------------------------------------------------------------------- #
#                                 Static Datas                                 #
# ---------------------------------------------------------------------------- #

user={
  "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
  "email": "john.doe@example.com",
  "username": "jdoe",
  "password": "2986b7f0cd0ba9827ace0810c8818825",
  "roles": [
    [
      "admin",
      "player"
    ]
  ],
  "description": "I am John Doe"
}

users=[
  {
    "id_user": "9e9fd408-0bc4-4c41-a3c0-c4e6a0e033d5",
    "email": "john.doe@example.com",
    "username": "jdoe",
    "password": "2986b7f0cd0ba9827ace0810c8818825",
    "roles": [
      [
        "admin",
        "player"
      ]
    ],
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

# ---------------------------------------------------------------------------- #
#                                   Functions                                  #
# ---------------------------------------------------------------------------- #





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
