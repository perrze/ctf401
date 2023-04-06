import re
import uuid

from flask import Flask, jsonify, request

app = Flask(__name__)

player1 = {
    "id_player": '34afa4d7-2bcb-4290-9906-56ea3f0553eb',
    "id_user": 'f97c4650-4795-4232-9a62-85eb97be71aa',
    "list_id_chall_success": [
        "Fl@g_!"
    ],
    "list_id_chall_try": [
        "Fl@g_!"
    ],
    "id_game": '365f2236-0ffc-496c-8260-e878dbd15a9c',
    "username": "toto"
}

player2 = {
    "id_player": 'e795512c-db6c-4bbe-8a4c-544107d24f0f',
    "id_user": '71335eb2-4360-4515-bd7d-894da5e24e19',
    "list_id_chall_success": [
        "Fl@g_!"
    ],
    "list_id_chall_try": [
        "Fl@g_!"
    ],
    "id_game": '365f2236-0ffc-496c-8260-e878dbd15a9c',
    "username": 'titi'
}

player3 = {
    "id_player": '5d8422a8-8246-4f1c-a904-62d83cad9c0b',
    "id_user": 'ada44e53-3374-450f-8b23-6cf9e914305b',
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


# Get data from DB :

def getPlayerById(id):
    for player in players:
        if id == (player['id_player']):
            return player
    return None
    # TODO get it working with a DB


def getPlayerByChallId(chall_id):
    tab_players = []
    for player in players:
        if chall_id in player["list_id_chall_success"]:
            tab_players.append(player)
    if len(tab_players) == 0:
        return None
    return tab_players
    # TODO get it working with a DB


def getGameById(game_id):
    for game in games:
        if game_id == game["id_game"]:
            return game
    return None
    # TODO get it working with a DB


# DB modification :
def addPlayer(verifiedPlayer):
    players.append(verifiedPlayer)
    return True
    # TODO get it working with a DB
    # TODO return true if it's done false if not


def deletePlayer(verifiedPlayer):
    players.remove(verifiedPlayer)
    return True
    # TODO get it working with a DB
    # TODO return true if it's done false if not


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
    regex_username = re.compile(r"^[\w\d\-]{3,32}$")
    if type(username) is not str:
        return False
    elif not regex_username.match(username):
        return False
    return True


"""This function tests if the request has a valid shape based on two inputs, all the keys that should be present and 
the request data."""


def requestIsCorrect(valid_key_list, rq):
    provided_key = []
    try:
        for key in rq:
            if key not in valid_key_list:
                return False
            provided_key.append(key)
        if provided_key is valid_key_list:
            return False
        return True
    except KeyError:
        return False


# API
@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome to the players API!'


@app.route('/players', methods=['GET'])
def getPlayers():
    return jsonify(players)
    # TODO getPlayers, get data from DB select * from players should do


@app.route('/players/create', methods=['POST'])
def createPlayers():
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
        return "Bad informations were given", 405

    if not uuidIsCorrect(rq['id_user']) or not uuidIsCorrect(rq['id_game']) or not usernameIsCorrect(rq['username']):
        return "Bad informations were given", 405

    createdPlayer['id_user'] = rq['id_user']
    createdPlayer['id_game'] = rq['id_game']
    createdPlayer['username'] = rq['username']
    addPlayer(createdPlayer)

    return createdPlayer, 200
    # TODO creation is working to test when DB is on


@app.route('/players/manage/<uuid>', methods=['GET', 'DELETE', 'PATCH', 'PUT'])
def managePlayers(uuid):
    if request.method == 'GET':
        player = getPlayerById(uuid)
        test_uuid = uuidIsCorrect(uuid)
        return jsonify(player)

    if request.method == 'DELETE':
        player = getPlayerById(uuid)
        test_uuid = uuidIsCorrect(uuid)
        deletePlayer(player)
        return jsonify(players)
    print('coucou')
    if request.method == 'PUT':
        print('coucou2')
        try:
            update_infos = request.get_json()
            print(update_infos)
        except KeyError:
            pass
        player = getPlayerById(uuid)
        test_uuid = uuidIsCorrect(uuid)
        update_infos = request.get_json()
        print(update_infos)
        player['id_game'] = update_infos['id_game']
        player['username'] = update_infos['username']
        player['list_id_chall_success'] = update_infos['success']
        player['list_id_chall_try'] = update_infos['try']
        return jsonify(player)
    return 'coucou'
    # TODO managePlayers


@app.route('/players/challenges', methods=['POST'])
def getPlayersByChallenge():
    valid_key = ["id_challenge", "id_game", "tags", "nb_points", "creator", "name", "description", "flag", "status",
                 "files"]
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

    # TODO function is working with python variable. To test with a DB


@app.route('/players/team/<id>', methods=['GET'])
def getTeamByPlayer(id):
    return team1
    # TODO getTeamByPlayer we have to wait for teams api to define object that are usable


@app.route('/players/game/<id>', methods=['GET'])
def getGameByPlayer(id):
    if not uuidIsCorrect(id):
        return "Bad informations were given", 405
    player = getPlayerById(id)
    if player is None:
        return "Player not found", 404
    game_id = player['id_game']
    game = getGameById(game_id)
    if game is None:
        return "No game found", 404
    return game, 200
    # TODO it's working, to test when DB is ready


if __name__ == '__main__':
    app.run()
