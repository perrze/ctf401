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
import sqlite3
import json
from urllib.parse import quote_plus

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
    },
    {
        "description": "Services users",
        "email": "services+users@ctf401.fr",
        "id_user": "0969eb87-27a6-4021-b170-729cb532a6c9",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    },
    {
        "description": "Services teams",
        "email": "services+teams@ctf401.fr",
        "id_user": "8212cbcd-6554-43f4-a18a-3fc3eb25bd07",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    },
    {
        "description": "Services challenges",
        "email": "services+challenges@ctf401.fr",
        "id_user": "c88049e2-88f4-41a2-b85d-9ca41d53bb4e",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    },
    {
        "description": "Services players",
        "email": "services+players@ctf401.fr",
        "id_user": "4d84a07f-f064-4385-9778-427a01394c4a",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    },
    {
        "description": "Services games",
        "email": "services+games@ctf401.fr",
        "id_user": "f686a569-ef6a-4c1a-9c37-99d38bd19483",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    },
    {
        "description": "Services website",
        "email": "services+website@ctf401.fr",
        "id_user": "04a92767-9786-4921-a238-766101e5cdf1",
        "password": "4c5ad97ad717574cbb7e73da27f72ba9",
        "roles": [
            "admin"
        ]
    }
]

jwtDB = {

}



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
    expire = time()+86400  # Now + 24h
    token = jwt.encode({"id_user": userid, 
                       "expire": expire}, SECRET_KEY, algorithm="HS256")
    return token,expire


def check_if_user_access(request, role):
    # TEMP DEACTIVATE DUE TO DEV
    # return True
    token = None
    if "jwt" in request.headers:
        token = request.headers["jwt"]
    if not token:
        
        return False
        # return True
    result = requests.post(BASE_URL+"/users/check/" +
                           role, json={"token": token})
    if result.status_code == 200:
        return True
    else:
        # TEMP DEACTIVATE DUE TO DEV
        return False
        # return True
    
global receivedToken
receivedToken=""
global expireAt
expireAt=0.0
def connect_services_to_auth():
    global receivedToken
    global expireAt
    with open(CREDS_LOCATION) as f:
        creds=json.load(f)
        email=creds["email"]
        password=creds["password"]
    
    result = requests.get(BASE_URL+"/users/login?email="+quote_plus(email)+"&password="+quote_plus(password))

    if result.status_code==200:
        jsonLoaded=json.loads(result.content)
        receivedToken=jsonLoaded["token"]
        expireAt=jsonLoaded["expire"]
        return True
    else:
        return False
    
def check_connected_to_auth():
    global receivedToken
    global expireAt
    if receivedToken=="" or expireAt<=time():

        connect_services_to_auth()
        return True
    else:
        return True

# ----------------------------------- Model ---------------------------------- #


def update_SQL_table(command):
    if typeSQL == "sqlite3":
        try:
            con = sqlite3.connect("users/users.db")
            cur = con.cursor()
            cur.execute(command)
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(str(e))
            logging.debug(str(e))
            return False
    return False


def get_SQL_result(command):
    if typeSQL == "sqlite3":
        try:
            con = sqlite3.connect("users/users.db")
            cur = con.cursor()
            res = cur.execute(command).fetchall()
            con.close()
            return res
        except Exception as e:
            print(str(e))
            logging.debug(str(e))
            return False


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
        res = get_SQL_result("SELECT email FROM users;")
        for emails in res:
            if email in emails:
                return False
        return True


def get_users_list():
    # Variables
    if variables:
        return usersDB
    else:
        res = get_SQL_result("SELECT * FROM users;")
        keys=["description","email","id_user","password","roles"]
        users=[]
        for user in res:
            userToAdd={keys[i] : user[i] for i in range(len(user))}
            userToAdd["roles"]=eval(userToAdd["roles"])
            users.append(userToAdd)
        # print(users)
        return users
        # return res


def add_user(user):
    # Variables
    if variables:
        usersDB.append(user)
    # Databse
    else:  
        firstPart="INSERT INTO users (" 
        secondPart="VALUES("
        for key in user:
            firstPart+="\""+key+"\","
            secondPart+="\""+str(user[key])+"\","
            
        firstPart=firstPart[:-1]+")\n"
        secondPart=secondPart[:-1]+");"
        print(firstPart+secondPart)
        update_SQL_table(firstPart+secondPart)
        
        


def get_properties_from_userid(userid):
    # Variables
    if variables:
        for user in usersDB:
            if user["id_user"] == userid:
                return user
        return False
    # Database
    else:
        query="SELECT * FROM users WHERE id_user='"+userid+"';"
        # print(query)
        result=get_SQL_result(query)
        # print(result)
        if result==[]:
            return False
        keys=["description","email","id_user","password","roles"]
        gettedUser=result[0]
        user={keys[i] : gettedUser[i] for i in range(len(gettedUser))}
        user["roles"]=eval(user["roles"])
        return user
        

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
        query="UPDATE users SET "
        for key in user:
            query+=key+"=\""+str(user[key])+"\","
            
        query=query[:-1]+" WHERE id_user='"+userid+"';"
        # print(query)
        update_SQL_table(query)
        


def delete_user(userid):
    # Variables
    if variables:
        position = return_position_in_array_user(userid)
        usersDB.pop(position)
    # Database
    else:
        query="DELETE FROM users WHERE id_user = '"+userid+"';"
        update_SQL_table(query)

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
        query="SELECT roles FROM users WHERE id_user='"+userid+"';"
        result=get_SQL_result(query)
        if result==[]:
            return False
        roles=eval(result[0][0])
        if role in roles:
            return True
        else:
            return False


def check_connection(email, hashed):
    # Variables
    if variables:
        for user in usersDB:
            if user["email"] == email and user["password"] == hashed:
                return user["id_user"]
        return False
    # Database
    else:
        query="SELECT id_user FROM users WHERE email='"+email+"' AND password='"+hashed+"';"
        result=get_SQL_result(query)
        if result==[] or result==False:
            return False
        return result[0][0]


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
if "CREDS_LOCATION" in environ:
    CREDS_LOCATION = getenv("CREDS_LOCATION")
else:
    CREDS_LOCATION = "users/creds.json"
if "DB_TYPE" in environ:
    DB_TYPE=getenv("DB_TYPE")
else:
    DB_TYPE="sqlite3"
if "USE_VARIABLES" in environ:
    USE_VARIABLES = eval(getenv("USE_VARIABLES"))
else:
    USE_VARIABLES = True

variables = USE_VARIABLES
typeSQL = DB_TYPE

logging.debug("SECRET_KEY = "+SECRET_KEY)
app.config['SECRET_KEY'] = SECRET_KEY


# ------------------------------------- / ------------------------------------ #


@app.route('/users/alive')
def default():
    return "Welcome to /users API from ctf401", 200


# ---------------------------------- /users ---------------------------------- #

@app.route('/users')
def listUsers():
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    return jsonify(get_users_list()), 200


@app.route('/users/create', methods=['POST'])
def createUser():
    if not (check_if_user_access(request, "admin")):
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
    # print("Email: "+email)
    email=email.replace(" ","+")
    password = request.args.get('password')
    hashed = hash_password(password)
    if userid := check_connection(email, hashed):
        token,expire = encode_jwt(userid, app.config["SECRET_KEY"])
        return ({"token": token,"expire":expire}), 200
    else:
        return "Invalid username/password supplied", 401
    # return jsonify(jwt), 200


@app.route('/users/logout')
def logoutUser():
    # Nothing to do because no Database of token
    return 'successful operation', 200


@app.route('/users/<userid>', methods=['GET'])
def getUserById(userid):
    print()
    if not (check_if_user_access(request, "admin")) and not (check_if_user_access(request, userid)):
        return "Unauthorized", 401
    if not (check_uuid_is_well_formed(userid)):
        return 'Invalid id_user supplied', 400
    user = get_properties_from_userid(userid)
    if user:
        return jsonify(user), 200
    else:
        return 'User not found', 404


@app.route('/users/<userid>', methods=['PUT'])
def updateUser(userid):
    if not (check_if_user_access(request, "admin")) and not (check_if_user_access(request, userid)):
        return "Unauthorized", 401
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
    if not (check_if_user_access(request, "admin")) and not (check_if_user_access(request, userid)):
        return "Unauthorized", 401
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
    token = request.get_json()["token"]
    logging.debug("Token Received: "+token)
    try:
        data = jwt.decode(
            token, app.config["SECRET_KEY"], algorithms="HS256")
        expire = data["expire"]
        current_time = time()
        if current_time > expire:
            return "Token Expired", 401

        userid = data["id_user"]
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

@app.route("/users/check/id_user",methods=["POST"])
def checkUserid():
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    token = request.get_json()["token"]
    logging.debug("Token Received: "+token)
    try:
        data = jwt.decode(
            token, app.config["SECRET_KEY"], algorithms="HS256")
        expire = data["expire"]
        current_time = time()
        if current_time > expire:
            return "Token Expired", 401

        userid = data["id_user"]
        logging.debug("Data: "+str(data))
        if userid is None:
            return "Invalid Authentication token!", 401
        return jsonify({"id_user":userid}),200
    except Exception as e:
        return "Invalid Authentication token!", 401

# Example function for services who need auth contacting each others
# @app.route("/users/temp/testAccess")
# def testAccess():
#     if not(check_connected_to_auth()): # Check if well connected and validity of creds
#         return "Services unauthorized",401
#     else:
#         global receivedToken
#         # API call that need to be auth
#         callToAPI=requests.get(BASE_URL+"/users",headers={"jwt": receivedToken}).content
#         return callToAPI,200

# ---------------------------------------------------------------------------- #
#                                   Operations                                  #
# ---------------------------------------------------------------------------- #


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0")
