from flask import Flask, request, jsonify
import uuid
import re
import sqlite3

app = Flask(__name__)

regex_int = r"^[1-9][0-9]+$"
regex_status = r"^(([Ff]alse)|([Tt]rue))$"
regex_list = r"^([a-zA-ZáàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ ]+, )*([ a-zA-ZáàâäãåçéèêëíìîïñóòôöõúùûüýÿæœÁÀÂÄÃÅÇÉÈÊËÍÌÎÏÑÓÒÔÖÕÚÙÛÜÝŸÆŒ]+)$"
regex_uuid = r"^[0-9a-zA-Z]{8}(-[0-9a-zA-Z]{4}){3}-[0-9a-zA-Z]{12}$"

@app.route("/")
def index():
	return "Welcome to API Challenges"

@app.route("/challenges", methods=['GET'])
def getChallenges():
	if request.method == 'GET':
		co_local_db = sqlite3.connect('db_challenges.db')
		c = co_local_db.cursor()
		c.execute('SELECT * FROM challenges')
		challenges = c.fetchall()
		#parcourir les résultats de la requête et créer un dictionnaire pour chaque ligne de la table
		column_names = [description[0] for description in c.description]
		result = [dict(zip(column_names, row)) for row in challenges]
		co_local_db.close()
		return jsonify(result)

@app.route("/challenges", methods=['POST'])
def createChallenge():
	if request.method == 'POST':
		response = request.get_json()
		id_chal = str(uuid.uuid4())
		id_game = response['id_game']
		tags = response['tags']
		nb_points = response['nb_points']
		creator = response['creator']
		name = response['name']
		description = response['description']
		flag = response['flag']
		status = response['status']
		if ((re.match(regex_status, str(status))) and (re.match(regex_int, str(nb_points))) and (re.match(regex_list, str(tags))) and creator.strip() and name.strip() and description.strip() and flag.strip()) :
			co_local_db = sqlite3.connect('db_challenges.db')
			c = co_local_db.cursor()
			c.execute('INSERT INTO challenges (id_challenge, id_game, tags, nb_points, creator, name, description, flag, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (id_chal, id_game, tags, nb_points, creator, name, description, flag, status))
			co_local_db.commit()
			co_local_db.close()
			return jsonify({'200':"Challenge created"})
		else :
			return jsonify({'404':"Challenge could not be created"})

@app.route("/challenges/<id>", methods=['GET'])
def getChallengeByID(id):
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_challenge=?', (id,))
	challenge = c.fetchone()
	co_local_db.close()
	if challenge :
		column_names = [description[0] for description in c.description]
		result = [dict(zip(column_names, challenge))]
		return jsonify(result)
	return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>", methods=['PATCH'])
def modifyChallengeByID(id):
	errors = []
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_challenge=?', (id,))
	challenge = c.fetchone()
	if challenge :
		column_names = [description[0] for description in c.description]
		response = request.get_json()
		for key, value in response.items():
			if key != 'id_challenge' :
				if key in column_names:
					if key=='nb_points':
						if (re.match(regex_int), str(value)):
							c.execute('UPDATE challenges SET nb_points = ? WHERE id_challenge=?', (value, id))
							co_local_db.commit()
						else:
							errors.append(f"Invalid value for {key}")
					elif key=='status':
						if (re.match(regex_status, str(value))):
							c.execute('UPDATE challenges SET status = ? WHERE id_challenge=?', (value, id))
							co_local_db.commit()
						else:
							errors.append(f"Invalid value for {key}")
					elif (key=='tags'):
						if (re.match(regex_list, str(value))):
							c.execute('UPDATE challenges SET tags = ? WHERE id_challenge=?', (value, id))
							co_local_db.commit()
						else:
							errors.append(f"Invalid value for {key}")
					elif (key=='id_game'):
						if (re.match(regex_uuid, str(value))):
							c.execute('UPDATE challenges SET id_game = ? WHERE id_challenge=?', (value, id))
						else:
							errors.append(f"Invalid value for {key}")
					else:
						if value.strip():
							c.execute(f'UPDATE challenges SET {key} = ? WHERE id_challenge=?', (value, id))
						else:
							errors.append(f"Empty value for {key}")
				else :
					errors.append(f"Invalid key : {key}")
			else :
				return jsonify({'404':"Impossible to change Challenge ID"})
		if errors :
			return jsonify({'405':"Invalid input", 'errors': errors})
		else :
			return jsonify({'200':"Challenge modified"})

@app.route("/challenges/<id>", methods=['DELETE'])
def deleteChallengeByID(id):
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_challenge=?', (id,))
	challenge = c.fetchone()
	if challenge :
		c.execute('DELETE FROM challenges WHERE id_challenge=?', (id,))
		co_local_db.commit()
		co_local_db.close()
		return jsonify({'200':"Challenge deleted"})
	else :
		return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>/check_flag", methods=['GET'])
def checkChallengeResponse(id):
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_challenge=?', (id,))
	challenge = c.fetchone()
	co_local_db.close()
	flag = request.args.get('flag')
	if (flag=="") :
		return jsonify({'405':'Invalid input'})
	if challenge:
		if (challenge[7]==flag):
			api_players = "/test/test"
			#faire un patch vers api_players pour envoyer token
			return jsonify({'check': True})
		else :
			#faire un patch vers api_players pour envoyer token
			return jsonify({'check': False})
	return jsonify({'404':"ID not found"})

@app.route("/challenges/<id>/status", methods=['GET'])
def checkChallengeStatus(id):
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_challenge=?', (id,))
	challenge = c.fetchone()
	co_local_db.close()
	if challenge:
		if (challenge[8]=="1"):
			return jsonify({'isActive': True})
		else :
			return jsonify({'isActive': False})
	return jsonify({'404':"ID not found"})

@app.route("/challenges/games/<id_game>", methods=['GET'])
def getChallengesByGame(id_game):
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_game=?', (id_game,))
	challenges = c.fetchall()
	column_names = [description[0] for description in c.description]
	result = [dict(zip(column_names, row)) for row in challenges]
	co_local_db.close()
	if not result:
		return jsonify({'404':"ID not found"})
	return jsonify(result)

@app.route("/challenges/games/<id_game>/<status>", methods=['GET'])
def getChallengesByStatus(id_game, status):
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	result = []
	if status=='active':
		c.execute('SELECT * FROM challenges WHERE id_game=? AND status=1', (id_game,))
		challenges = c.fetchall()
	elif status=='inactive':
		c.execute('SELECT * FROM challenges WHERE id_game=? AND status=0', (id_game,))
		challenges = c.fetchall()
	if not challenges :
		co_local_db.close()
		return jsonify({'404':"Not found"})
	column_names = [description[0] for description in c.description]
	result = [dict(zip(column_names, row)) for row in challenges]
	co_local_db.close()
	return jsonify(result)

@app.route("/challenges/games/<id_game>/tags", methods=['GET'])
def getChallengesByGameByTag(id_game):
	result = []
	tag = request.args.get('tag')
	if not tag:
		return jsonify({'405': "Invalid input"})
	co_local_db = sqlite3.connect('db_challenges.db')
	c = co_local_db.cursor()
	c.execute('SELECT * FROM challenges WHERE id_game=?', (id_game,))
	challenges = c.fetchall()
	for challenge in challenges :
		if tag in challenge[2]:
			result.append(challenge)
	column_names = [description[0] for description in c.description]
	results = [dict(zip(column_names, row)) for row in result]
	co_local_db.close()
	if not results:
		return jsonify({'404':"Not found"})
	return jsonify(results)

if __name__ == '__main__':
        app.run(debug=True)
