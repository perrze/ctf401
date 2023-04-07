from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

CHALLENGES = [
	{"id_challenge": "a682b3d6-50cd-4f26-91fd-2eb66c249301",
	"id_game": "a682b3d6-50cd-4f26-91fd-2eb66c249310",
	"tags": "easy, Réseaux, Sécurité",
	"nb_points": 300, "creator": "clasheureux",
	"name": "Analyser des paquets",
	"description": "Analyser des paquets pour trouver le flag !",
	"flag": "IUTSM", "status": True},
	{"id_challenge": "a682b3d6-50cd-4f26-91fd-2eb66c249302",
	"id_game": "a682b3d6-50cd-4f26-91fd-2eb66c249310",
	"tags": "hard, Systèmes",
	"nb_points": 500,
	"createur": "clasheureux2",
	"name": "Analyser des fichiers",
	"description": "Analyser des fichiers pour trouver le flag !",
	"flag": "IUTSM",
	"status": False},
	{"id_challenge": "a682b3d6-50cd-4f26-91fd-2eb66c249302",
	"id_game": "a682b3d6-50cd-4f26-91fd-2eb66c249311",
	"tags": "hard, Systèmes",
	"nb_points": 500,
	"createur": "clasheureux2",
	"name": "Décrypter un fichier",
	"description": "Décrypter le fichier pour trouver le flag !",
	"flag": "IUTSM",
	"files": "/user/file1.png",
	"status": False}]

@app.route("/")
def index():
	return "Welcome to API Challenges"

@app.route("/challenges", methods=['GET'])
def getChallenges():
	if request.method == 'GET':
		return jsonify(CHALLENGES)

@app.route("/challenges", methods=['POST'])
def createChallenge():
	if request.method == 'POST':
		response = request.get_json()
		id_chal = uuid.uuid4()
		level = response['level']
		category = response['category']
		nb_points = response['nb_points']
		creator = response['creator']
		name = response['name']
		description = response['description']
		flag = response['flag']
		status = response['status']
		challenge = {"id_challenge": id_chal, "level": level, "category": category, "nb_points": nb_points, "creator": creator, "name": name, "description": description, "flag": flag, "status": status}
		CHALLENGES.append(challenge)
		return jsonify({'200':"Challenge created"})

@app.route("/challenges/<id>", methods=['GET'])
def getChallengeByID(id):
	id_chal = id
	for challenge in CHALLENGES :
		if (challenge['id_challenge'] == id_chal) :
				return jsonify(challenge)
	return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>", methods=['PATCH'])
def modifyChallengeByID(id):
	id_chal = id
	for challenge in CHALLENGES :
		if (challenge['id_challenge'] == id_chal) :
			response = request.get_json()
			for key, value in response.items():
				if key in challenge:
					challenge[key] = value
					return jsonify({'200':"Challenge Modified"})
	return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>", methods=['DELETE'])
def deleteChallengeByID(id):
	id_chal = id
	for challenge in CHALLENGES :
		if (challenge['id_challenge'] == id_chal) :
			CHALLENGES.remove(challenge)
			return jsonify({'200':"Challenge deleted"})
	return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>/check_flag", methods=['GET'])
def checkChallengeResponse(id):
	id_chal = id
	for challenge in CHALLENGES :
		if (challenge['id_challenge'] == id_chal) :
			flag = request.args.get('flag')
			if (flag=="") :
				return jsonify({'405':'Invalid input'})
			if (challenge['flag']==flag):
				return jsonify({'response': flag, 'check': True})
			else :
				return jsonify({'response': flag, 'check': False})
	return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>/status", methods=['GET'])
def checkChallengeStatus(id):
	id_chal = id
	for challenge in CHALLENGES :
		if (challenge['id_challenge'] == id_chal) :
			if (challenge['status']==True):
				return jsonify({'isActive': True})
			else :
				return jsonify({'isActive': False})
	return jsonify({'404':"ID not found"})

@app.route("/challenges/games/<id_game>", methods=['GET'])
def getChallengesByGame(id_game):
	id = id_game
	result = []
	for challenge in CHALLENGES :
		if (challenge['id_game'] == id) :
			result.append(challenge)
	if not result:
		return jsonify({'404':"ID not found"})
	return jsonify(result)

@app.route("/challenges/games/<id_game>/<status>", methods=['GET'])
def getChallengesByStatus(id_game, status):
	id = id_game
	status_chal = status
	result = []
	for challenge in CHALLENGES :
		if (challenge['id_game'] == id):
			if (status_chal == 'active'):
				if (challenge['status']==True):
					result.append(challenge)
			elif (status_chal == 'inactive'):
				if (challenge['status']==False):
					result.append(challenge)
	if not result :
		return jsonify({'404':"Not found"})
	return jsonify(result)

@app.route("/challenges/games/<id_game>/tags", methods=['GET'])
def getChallengesByGameByTag(id_game):
	id = id_game
	result = []
	tag = request.args.get('tag')
	if (tag==""):
		return jsonify({'405': "Invalid input"})
	for challenge in CHALLENGES :
		if (challenge['id_game'] == id):
			if tag in challenge['tags'] :
				result.append(challenge)
	if not result:
		return jsonify({'404':"Not found"})
	return jsonify(result)

if __name__ == '__main__':
        app.run(debug=True)
