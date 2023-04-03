from flask import Flask, jsonify, request

app = Flask(__name__)

player1 = {
    "id_player": '34afa4d7-2bcb-4290-9906-56ea3f0553eb',
    "id_user": 'f97c4650-4795-4232-9a62-85eb97be71aa',
    "list_id_chall_reussi": [
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
    "list_id_chall_reussi": [
        "Fl@g_!"
    ],
    "list_id_chall_try": [
        "Fl@g_!"
    ],
    "id_game": '365f2236-0ffc-496c-8260-e878dbd15a9c',
    "username": 'titi'
}

player3 = {
    "id_player": 'e795512c-db6c-4bbe-8a4c-544107dfffff',
    "id_user": '71335eb2-4360-4515-bd7d-894da5e24e19',
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

@app.route('/')
def hello_world():  # put application's code here
    return 'Welcome to the players API!'


@app.route('/players', methods=['GET'])
def getPlayers():
    return jsonify(players)
    # TODO getPlayers, get data from DB


@app.route('/players/create', methods=['POST'])
def createPlayers():
    createdPlayer = {}
    valid_key = ["id_user", "username", "id_game"]
    rq = request.get_json()
    tab_key=[]
    for key in rq:
        if key in valid_key:
            tab_key.append(key)
        else:
            return "Bad informations were given", 400
    # print(rq)
    return jsonify(tab_key)
    # TODO createPlayers, update the database


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
    # return somedata


@app.route('/players/challenges', methods=['POST'])
def getPlayersByChallenge():
    return 'coucou'
    # TODO getPlayersByChallenge


@app.route('/players/team/<id>', methods=['GET'])
def getTeamByPlayer(id):
    return 'coucou'
    # TODO getTeamByPlayer


@app.route('/players/game/<id>', methods=['GET'])
def getGameByPlayer(id):
    return 'coucou'
    # TODO getGameByPlayer


if __name__ == '__main__':
    app.run()

# Méthodes de récupération de données :

def getPlayerById(id):
    for player in players:
        if id == (player['id_player']):
            return player
    return "No Player found", 400
