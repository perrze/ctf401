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
    "list_id_chall_reussi": [
        "Fl@g_!"
    ],
    "list_id_chall_try": [
        "Fl@g_!"
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

game1 = {
  "id_game": "365f2236-0ffc-496c-8260-e878dbd15a9c",
  "start_date": "2023-04-03T22:00:00.000Z",
  "end_date": "2023-04-04T22:00:00.000Z",
  "name": "1st game",
  "description": "This is our first game. please be kind",
  "logo": "/dev/null"
}


# Get data from DB :

def getPlayerById(id):
    for player in players:
        if id == (player['id_player']):
            return player
    return "No Player found", 400


# DB modification :
def addPlayer(verifiedPlayer):
    players.append(verifiedPlayer)
    # TODO get it working with a DB


# check values :
def uuidIsCorrect(uuid):
    regex_uuid = re.compile(r"^[0-9a-zA-Z]{8}(-[0-9a-zA-Z]{4}){3}-[0-9a-zA-Z]{12}$")
    if type(uuid) is not str:
        return False
    elif not regex_uuid.match(uuid):
        return False
    return True


def usernameIsCorrect(username):
    regex_username = re.compile(r"^[\w\d\-]{3,32}$")
    if type(username) is not str:
        return False
    elif not regex_username.match(username):
        return False
    return True


def requestIsCorrect(valid_key_list, rq):
    provided_key = []
    print("test")
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
    # TODO getPlayers, get data from DB


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

    return createdPlayer
    # TODO creation is working to test when DB is on


@app.route('/players/manage/<id>', methods=['GET', 'DELETE', 'PATCH', 'PUT'])
def managePlayers(id):
    if request.method == 'GET':
        player = getPlayerById(id)
        return jsonify(player)

    if request.method == 'DELETE':
        player = getPlayerById(id)
        players.remove(player)
        return jsonify(players)

    if request.method == 'PUT':
        player = getPlayerById(id)
    return 'coucou'
    # TODO managePlayers


@app.route('/players/challenges', methods=['POST'])
def getPlayersByChallenge():
    return players
    # TODO getPlayersByChallenge


@app.route('/players/team/<id>', methods=['GET'])
def getTeamByPlayer(id):
    return team1
    # TODO getTeamByPlayer


@app.route('/players/game/<id>', methods=['GET'])
def getGameByPlayer(id):
    return game1
    # TODO getGameByPlayer


if __name__ == '__main__':
    app.run()
