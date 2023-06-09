import json, requests, sqlite3, uuid, re
from time import time
from urllib.parse import quote_plus
from flask_cors import CORS
from flask import Flask, jsonify, request
from os import getenv, environ

conn = sqlite3.connect('./players.db', check_same_thread=False)
curs = conn.cursor()

app = Flask(__name__)
CORS(app)
if "CREDS_LOCATION" in environ:
    CREDS_LOCATION = getenv("CREDS_LOCATION")
else:
    CREDS_LOCATION = "players/creds.json"
if "BASE_URL" in environ:
    BASE_URL_USERS = getenv("BASE_URL")
else:
    BASE_URL_USERS = "http://localhost:5001"


# BASE_URL_USERS = "http://localhost:5001"
# BASE_URL_PLAYERS = "http://localhost:5002"

curs.execute('''CREATE TABLE IF NOT EXISTS players(id_player STRING PRIMARY KEY, id_user STRING, list_id_chall_success STRING, list_id_chall_try STRING, id_game STRING, username STRING)''')
conn.commit()

global receivedToken
receivedToken =""
global expireAt
expireAt = 0.0

""" These next function allow us to authenticate an user and check jwt token validity and rights."""

def connect_services_to_auth():
    global receivedToken
    global expireAt
    with open(CREDS_LOCATION) as f:
        creds = json.load(f)
        email = creds["email"]
        password = creds["password"]

    result = requests.get(BASE_URL_USERS + "/users/login?email=" + quote_plus(email) + "&password=" + quote_plus(password))
    if result.status_code == 200:
        jsonLoaded = json.loads(result.content)
        receivedToken = jsonLoaded["token"]
        expireAt = jsonLoaded["expire"]
        return True
    else:
        return False


def check_connected_to_auth():
    global receivedToken
    global expireAt
    if receivedToken == "" or expireAt <= time():
        temp = connect_services_to_auth()
        return temp
    else:
        return True


def check_if_user_access(request,role):
  token = None
  if "jwt" in request.headers:
      token = request.headers["jwt"]
  if not token:
      return False
  result = requests.post(BASE_URL_USERS+"/users/check/"+role,json={"token":token})
  if result.status_code==200:
    return True
  else:
    return False


key_player = ["id_player","id_user","list_id_chall_success","list_id_chall_try","id_game","username"]

player1 = {
    "id_player": '34afa4d7-2bcb-4290-9906-56ea3f0553eb',
    "id_user": 'f97c4650-4795-4232-9a62-85eb97be71aa',
    "list_id_chall_success": [
        "c554794d-f590-4d9e-8b46-9d83fb4ebab3"
    ],
    "list_id_chall_try": [
        "c554794d-f590-4d9e-8b46-9d83fb4ebab3"
    ],
    "id_game": '365f2236-0ffc-496c-8260-e878dbd15a9c',
    "username": "toto"
}

player2 = {
    "id_player": 'e795512c-db6c-4bbe-8a4c-544107d24f0f',
    "id_user": '71335eb2-4360-4515-bd7d-894da5e24e19',
    "list_id_chall_success": [
        "c554794d-f590-4d9e-8b46-9d83fb4ebab3"
    ],
    "list_id_chall_try": [
        "c554794d-f590-4d9e-8b46-9d83fb4ebab3"
    ],
    "id_game": '365f2236-0ffc-496c-8260-e878dbd15a9c',
    "username": 'titi'
}

player3 = {
    "id_player": '5d8422a8-8246-4f1c-a904-62d83cad9c0b',
    "id_user": '31a1d300-4224-4f5b-a1ab-94129f264cc6',
    "list_id_chall_success": [
        "e57b5f14-02e3-4e86-85cb-cef05a22eaf6",
        "35711541-3845-4c84-8a09-33f76194597e"
    ],
    "list_id_chall_try": [
        "e57b5f14-02e3-4e86-85cb-cef05a22eaf6",
        "35711541-3845-4c84-8a09-33f76194597e",
        "9db389de-4ebd-4c8c-b9c3-439a80831980"
    ],
    "id_game": '365f2236-0ffc-496c-8260-e878dbd15a9c',
    "username": 'tata'
}

players = [player1, player2, player3]

team1 = {
    "id_team": "028ef291-4b15-4363-9fc9-444372676a44",
    "id_game": "365f2236-0ffc-496c-8260-e878dbd15a9c",
    "name": "Team A",
    "description": "Team A, our friends are Team B and Team C. Together we make Team ABC",
    "members": [
        "5d8422a8-8246-4f1c-a904-62d83cad9c0b",
        "e795512c-db6c-4bbe-8a4c-544107d24f0f"
    ]
}

teams = [team1]

game1 = {
    "id_game": "365f2236-0ffc-496c-8260-e878dbd15a9c",
    "start_date": "2023-04-03T22:00:00.000Z",
    "end_date": "2023-04-04T22:00:00.000Z",
    "name": "1st game",
    "description": "This is our first game. please be kind",
    "logo": "/dev/null"
}

games = [game1]

# Ajout de trois joueurs tests dans la base de données
player1['list_id_chall_success'] = str(player1['list_id_chall_success'])
player1['list_id_chall_try'] = str(player1['list_id_chall_try'])

player2['list_id_chall_success'] = str(player1['list_id_chall_success'])
player2['list_id_chall_try'] = str(player1['list_id_chall_try'])

player3['list_id_chall_success'] = str(player1['list_id_chall_success'])
player3['list_id_chall_try'] = str(player1['list_id_chall_try'])

curs.execute('''INSERT INTO players(id_player, id_user, list_id_chall_success, list_id_chall_try, id_game, username ) VALUES (:id_player, :id_user, :list_id_chall_success, :list_id_chall_try , :id_game , :username)''', player1)
curs.execute('''INSERT INTO players(id_player, id_user, list_id_chall_success, list_id_chall_try, id_game, username ) VALUES (:id_player, :id_user, :list_id_chall_success, :list_id_chall_try , :id_game , :username)''', player2)
curs.execute('''INSERT INTO players(id_player, id_user, list_id_chall_success, list_id_chall_try, id_game, username ) VALUES (:id_player, :id_user, :list_id_chall_success, :list_id_chall_try , :id_game , :username)''', player3)

# Get data from DB :

def getPlayerById(id):
    idPlayer = str(id)
    print(idPlayer)
    curs.execute('''SELECT * FROM players WHERE id_player = ?''', [idPlayer])
    player = curs.fetchall()
    p = {key_player[i]: player[0][i] for i in range(len(key_player))}
    p["list_id_chall_success"] = eval(p["list_id_chall_success"])
    p["list_id_chall_try"] = eval(p["list_id_chall_try"])
    if p is not None:
            return p
    # for player in players:
    #     if player['id_player'] == id:
    #         return player
    return "No Player found !", 405
    # TO DO getPlayerById : get it working with a DB

def getPlayerByUserId(id):
    idUser = str(id)
    print(idUser)
    curs.execute('''SELECT * FROM players WHERE id_user = ?''', [idUser])
    player = curs.fetchall()
    p = {key_player[i]: player[0][i] for i in range(len(key_player))}
    p["list_id_chall_success"] = eval(p["list_id_chall_success"])
    p["list_id_chall_try"] = eval(p["list_id_chall_try"])
    if p is not None:
        return p
    # for player in players:
    #     if player['id_player'] == id:
    #         return player
    return "No player found !", 405


def getPlayerByChallId(chall_id):
    tab_players = []
    players = getPlayers()
    chall = chall_id
    for player in players:
        id_chall = player['list_id_chall_success'][0]
        if id_chall == chall:
            tab_players.append(player)
    #     if chall_id in player["list_id_chall_success"]:
    #         tab_players.append(player)
    # if len(tab_players) == 0:
    #     return None
    return tab_players
    # TO DO getPlayerByChallId : get it working with a DB


def getPlayersByGameId(game_id):
    idGame = str(game_id)
    curs.execute('''SELECT * FROM players WHERE id_game = ?''', [idGame])
    game = curs.fetchall()
    listPlayers = []
    for player in game:
        p = {key_player[i]: player[i] for i in range(len(key_player))}
        p["list_id_chall_success"] = eval(p["list_id_chall_success"])
        p["list_id_chall_try"] = eval(p["list_id_chall_try"])
        listPlayers.append(p)
    if listPlayers is not None:
        return listPlayers
    # for player in players:
    #     if player['id_player'] == id:
    #         return player
    return "No Player found !", 404
    # TO DO getGameById get it working with a DB


# DB modification :
def addPlayer(verifiedPlayer):
    print(verifiedPlayer)
    id_player = verifiedPlayer['id_player']
    id_user = verifiedPlayer['id_user']
    list_id_chall_success = str(verifiedPlayer['list_id_chall_success'])
    list_id_chall_try = str(verifiedPlayer['list_id_chall_try'])
    id_game = verifiedPlayer['id_game']
    username = verifiedPlayer['username']
    curs.execute('''INSERT INTO players(id_player, id_user, list_id_chall_success, list_id_chall_try, id_game, username ) VALUES (:id_player, :id_user, :list_id_chall_success, :list_id_chall_try , :id_game , :username)''', (id_player, id_user, list_id_chall_success, list_id_chall_try, id_game, username))
    conn.commit()
    return True
    # TO DO addPlayer : get it working with a DB
    # TO DO return true if it's done false if not


def deletePlayer(player):
    print(player)
    listPlayer = list(player[0])
    print(listPlayer)
    id_player = listPlayer[0]
    curs.execute('''DELETE FROM players WHERE id_player = ?''', [id_player])
    conn.commit()
    return True
    # TO DO deletePlayer : get it working with a DB
    # TO DO return true if it's done false if not

def modifyPlayer(id_player, rowsToChange, valuesToChange):
    for row,value in rowsToChange, valuesToChange:
        curs.execute(f'''UPDATE players SET {row} = {value} WHERE id_player = {id_player} ''')
    conn.commit()
    player = getPlayerById(id_player)
    return player


# check values :

""" This function checks if the uuid macth the uuid shape to prevent mistreatment."""


def uuidIsCorrect(uuid):
    regex_uuid = re.compile(r"^[0-9a-fA-F]{8}(-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$")
    if type(uuid) is not str:
        return False
    elif not regex_uuid.match(uuid):
        return False
    return True


""" This function tests if the username matches the username's policies."""


def usernameIsCorrect(username):
    regex_username = re.compile(r"^[\w\-]{3,32}$")
    if type(username) is not str:
        return False
    elif not regex_username.match(username):
        return False
    return True


"""This function tests if the request has a valid shape based on two inputs, all the keys that should be present and 
the request data."""


def requestIsCorrect(valid_keys_list, rq):
    provided_keys = []
    try:
        for key in rq:
            if key not in valid_keys_list:
                return False
            provided_keys.append(key)
        if provided_keys is valid_keys_list:
            return False
        return True
    except KeyError:
        return False

"""This function is used for the 'patch' command. It takes the request made by the user and the list of every keys
expected. It returns the list of keys that will be modified and True if the list isn't empty and false if it is."""


def patchKeys(valid_keys_list, rq):
    provided_keys = []
    for key in rq:
        try:
            if (key in valid_keys_list) and (key not in provided_keys):
                provided_keys.append(key)
        except KeyError:
            pass
    if len(provided_keys) > 0:
        return provided_keys, True
    else:
        return provided_keys, False




# API
@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome to the players API!'


@app.route('/players', methods=['GET'])
def getPlayers():
    curs.execute('''SELECT * FROM players''')
    playersFromBdd = curs.fetchall()
    listPlayers = []
    for player in playersFromBdd:
        p = {key_player[i]: player[i] for i in range(len(key_player))}
        p["list_id_chall_success"] = eval(p["list_id_chall_success"])
        p["list_id_chall_try"] = eval(p["list_id_chall_try"])
        listPlayers.append(p)
    return listPlayers
    # TO DO getPlayers : get data from DB select * from players should do

@app.route('/players/jwt', methods=['GET'])
def getPlayersByJWT():
    token = {'jwt': request.args['jwt']}
    print(token)
    try:    # Temp !!!
        url = BASE_URL_USERS + "/users/check/jwt"
        rq = requests.get(url, headers=token)
        if not rq.status_code == 200:
            return "Unauthorized", 401
        id_user = rq.json()["id_user"]
        print(id_user)
        player = getPlayerByUserId(id_user)
        if player is None:
            return "No player found", 404
        return player
    except requests.exceptions.InvalidSchema:
        return "Internal Server Error",500



@app.route('/players/create', methods=['POST'])
def createPlayers():
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    createdPlayer = {
        "id_player": str(uuid.uuid4()),
        "id_user": "",
        "list_id_chall_success": [],
        "list_id_chall_try": [],
        "id_game": "",
        "username": ""
    }
    valid_key = ["id_user", "username", "id_game"]
    rq = request.get_json()

    if not requestIsCorrect(valid_key, rq):
        return "Bad informations were given !", 405

    if not uuidIsCorrect(rq['id_user']) or not uuidIsCorrect(rq['id_game']) or not usernameIsCorrect(rq['username']):
        return "Bad informations were given", 405

    createdPlayer['id_user'] = rq['id_user']
    createdPlayer['id_game'] = rq['id_game']
    createdPlayer['username'] = rq['username']
    addPlayer(createdPlayer)

    return createdPlayer, 200
    # TODO createPlayers : creation is working to test when DB is on


@app.route('/players/manage/<uuid>', methods=['GET'])
def managePlayersGet(uuid):
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    if not uuidIsCorrect(uuid):
        return "Bad id were given !", 405
    player = getPlayerById(uuid)
    return jsonify(player)


@app.route('/players/manage/<uuid>', methods=['DELETE'])
def delPlayer(uuid):
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    print(uuid)
    if not uuidIsCorrect(uuid):
        return "Bad id wer given !", 405
    player = getPlayerById(uuid)
    deletePlayer(player)
    return getPlayers()


@app.route('/players/manage/<uuid>', methods=['PUT'])
def putPlayer(uuid):
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    valid_keys = ["id_game", "username", "list_id_chall_success", "list_id_chall_try"]
    try:
        update_infos = request.get_json()

        if (not requestIsCorrect(valid_keys, update_infos)) and (not uuidIsCorrect(uuid)):
            return "Bad information were given !", 405

        player = getPlayerById(uuid)
        print(player)
        id_game = update_infos['id_game']
        username = update_infos['username']
        list_id_chall_success = str(update_infos["list_id_chall_success"])
        list_id_chall_try = str(update_infos["list_id_chall_try"])
        curs.execute('''UPDATE players SET id_game = ? , username = ? , list_id_chall_success = ? , list_id_chall_try = ? WHERE id_player = ? ''', (id_game, username, list_id_chall_success, list_id_chall_try, uuid))
        conn.commit()
        return getPlayerById(uuid)
    except KeyError:
        return "Bad keys were given !", 405


@app.route('/players/manage/<uuid>', methods=['PATCH'])
def patchPlayer(uuid):
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401
    print(uuid)
    valid_keys = ['id_game', 'username', 'list_id_chall_success', 'list_id_chall_try']
    update_infos = request.get_json()
    player = getPlayerById(uuid)
    id_player = str(uuid)
    if (not uuidIsCorrect(uuid)) or (not patchKeys(valid_keys, update_infos)[1]):
        return "Bad keys were given !", 405
    print(player)
    for field in patchKeys(valid_keys, update_infos)[0]:
        print(field)
        newValue = str(update_infos[field])
        curs.execute('''UPDATE players SET %s = ? WHERE id_player = ? ''' % field, (newValue, id_player))
    print(player)
    return getPlayerById(uuid)

    #return 'coucou'
    # TODO managePlayers


@app.route('/players/challenges', methods=['POST'])
def getPlayersByChallenge():
    valid_key = ["id_challenge"]
    rq = request.get_json()
    if not requestIsCorrect(valid_key, rq):
        return "Bad informations were given", 405
    id_chall = rq['id_challenge']
    if not uuidIsCorrect(id_chall):
        return "Bad informations were given", 405
    tab_players = getPlayerByChallId(id_chall)
    if tab_players is None:
        return "No successful challenges found", 404
    return tab_players, 200

    # TODO getPlayersByChallenges :  function is working with python variable. To test with a DB

@app.route('/players/addchallenges', methods=['POST'])
def addChallenges():
    if not (check_if_user_access(request, "admin")):
        return "Unauthorized", 401

    valid_keys = ["id_player","id_chall","success"]
    rq = request.get_json()

    if not requestIsCorrect(valid_keys, rq):
        return "Bad informations were given", 405

    if (not uuidIsCorrect(rq["id_player"])) or (not uuidIsCorrect(rq["id_chall"])):
        return "Bad informations were given", 405

    player = getPlayerById(rq["id_player"])
    if player is None:
        return "Player not found",404

    if rq["success"]:
        rowsToChange = ["list_id_chall_success","list_id_chall_try"]

        list_id_chall_success = player["list_id_chall_success"]
        list_id_chall_success.append(rq["id_chall"])
        list_id_chall_try = player["list_id_chall_try"]
        list_id_chall_try.append(rq["id_chall"])

        valuesToChange = [list_id_chall_success,list_id_chall_try]

        player = modifyPlayer(rq["id_player"], rowsToChange, valuesToChange)
    else:
        rowToChange = ["list_id_chall_success"]

        list_id_chall_try = player["list_id_chall_try"]
        list_id_chall_try.append(rq["id_chall"])

        valueToChange = [list_id_chall_try]

        player = modifyPlayer(rq["id_player"], rowToChange, valueToChange)

    return player,200



@app.route('/players/team/<id>', methods=['GET'])
def getTeamByPlayer(id):
    return team1
    # TODO getTeamByPlayer : we have to wait for teams api to define object that is usable


@app.route('/players/game/<id>', methods=['GET'])
def getGameByPlayer(id):
    if not uuidIsCorrect(id):
        return "Bad informations were given", 405
    player = getPlayerById(id)
    if player is None:
        return "Player not found", 404
    game_id = player['id_game']
    game = getPlayersByGameId(game_id)
    if game is None:
        return "No game found", 404
    return game, 200
    # TODO getGameByPlayer : it's working, to test when DB is ready



#--------------------------------------------------------------------------------------------------------------#
#                                                   SQLite3                                                    #
#--------------------------------------------------------------------------------------------------------------#

# id_player_test = str(uuid.uuid4())
# id_game_test = str(uuid.uuid4())
# id_user_test = str(uuid.uuid4())
#
# curs.execute('''INSERT INTO players VALUES (?, ?, '[]', '[]', ?, 'test')''', (id_player_test, id_user_test, id_game_test))
# conn.commit()

# curs.execute('''SELECT * FROM players''')
# result = curs.fetchall()
# print(result)

# userToDelete = str(input("Veuillez entrer le nom de l'utilisateur a supprimer : "))
#
# curs.execute('''DELETE FROM players WHERE username = ?''', [userToDelete])
# conn.commit()
#
# field = str(input("Veuillez entrer le champ à mettre à jour : "))
# value = str(input(f"Veuillez entrer la nouvelle valeur de {field} : "))
#
# condToTest = str(input("Veuillez entrer la paramètre selon lequel va être fait la modification : "))
# expectedResult = str(input(f"Veuillez entrer la valeur attendue pour {condToTest} : "))
#
# curs.execute('''UPDATE players SET %s = ? WHERE %s = ? ''' % (field, condToTest), (value, expectedResult))       #A mettre dans une boucle for pour effectuer toutes les modifs de clés qu'on veut
# conn.commit()
#
#
#
# curs.execute('''SELECT * FROM players''')
# result = curs.fetchall()
# print(result)

if __name__ == '__main__':
    app.run(host="0.0.0.0")
