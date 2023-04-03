from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/players', methods=['GET'])
def getPlayers():
    return 'coucou'
    # TODO getPlayers


@app.route('/players/manage/<id>', methods=['GET', 'DELETE', 'PATCH', 'PUT'])
def managePlayers(id):
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
