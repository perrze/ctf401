import uuid
from flask import *
import sqlite3


app = Flask(__name__)


@app.route("/", methods=['GET'])
def Home():
	if request.method == 'GET':
		return "API Teams"


@app.route("/teams", methods=['GET'])
def getAllTeams():
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		team=[]
		curs.execute('''SELECT * FROM teams''')
		resultats = curs.fetchall()
		for resultat in resultats:
			team.append(resultat)
		curs.close()
		conn.close()
		return jsonify({'200':"all team found",'info':team})


@app.route("/teams", methods=["POST"])
def postTeam():
	if request.method == 'POST':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		rep = request.json
		id_teams = uuid.uuid4()
		id_game = rep['id_game']
		name = rep["name"]
		description = rep['description']
		member = rep['member']
		team = {"id_teams": id_teams, "id_game": id_game, "name": name, "description": description, "member": member}
		curs.execute('''INSERT INTO teams(id_teams, id_game, name, description, member) VALUES (?,?,?,?,?)''', (id_teams,id_game,name,description,member))
		conn.commit()
		conn.close()
		return jsonify({'200':"team created"})


@app.route("/teams/<id_team>", methods=['GET'])
def getTeam(id_team):
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			conn.commit()
			conn.close()
			return jsonify({'200':"team found",'info':resultats[0]})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>", methods=["DELETE"])
def deleteTeam(id_team):
	if request.method == 'DELETE':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			curs.execute('''DELETE FROM teams WHERE id_teams=''' + id_team)
			conn.commit()
			conn.close()
			return jsonify({'200':"team deleted"})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>", methods=["PATCH"])
def patchTeam(id_team):
	if request.method == 'PATCH':
		errors = []
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats = curs.fetchall()
		if resultats:
			column_names = [description[0] for description in curs.description]
			response = request.get_json()
			for key, value in response.items():
				if key != 'id_challenge':
					if key in column_names:
						if key == 'name':
							if str(value):
								curs.execute('UPDATE team SET name = ? WHERE id_team=?', (value, id_team))
								conn.commit()
							else:
								errors.append(f"Invalid value for {key}")
						elif key == 'description':
							if str(value):
								curs.execute('UPDATE team SET description = ? WHERE id_team=?', (value, id_team))
								conn.commit()
							else:
								errors.append(f"Invalid value for {key}")
						elif (key == 'member'):
							if str(value):
								curs.execute('UPDATE team SET member = ? WHERE id_team=?', (value, id_team))
								conn.commit()
							else:
								errors.append(f"Invalid value for {key}")
					else:
						errors.append(f"Invalid key : {key}")
				else:
					return jsonify({'404':"ID not found"})
			if errors:
				return jsonify({'405': "Invalid input", 'errors': errors})
			else:
				return jsonify({'200': "team modified"})


@app.route("/teams/name", methods=['GET'])
def getAllNameTeam():
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		liste_name=[]
		curs.execute("SELECT name FROM teams")
		resultats = curs.fetchall()
		for resultat in resultats:
			liste_name.append(resultat)
		conn.commit()
		conn.close()
		return jsonify({'200':"name of all team has found","name" : liste_name})


@app.route("/teams/name/<id_team>", methods=['GET'])
def getNameTeam(id_team):
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			conn.commit()
			conn.close()
			return jsonify({'200':"team found",'info':resultats[0][2]})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>", methods=['GET'])
def getMembersTeam(id_team):
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			conn.commit()
			conn.close()
			return jsonify({'200':"team found",'info':resultats[0][4]})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>/<id_member>", methods=["DELETE"])
def deleteMemberTeam(id_team, id_member):
	if request.method == 'DELETE':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			curs.execute('''DELETE FROM teams WHERE member=''' + resultats[0][4][id_member])
			conn.commit()
			conn.close()
			return jsonify({'200':"team deleted"})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


@app.route("/teams/description/<id_team>", methods=['GET'])
def getDescriptionTeam(id_team):
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			conn.commit()
			conn.close()
			return jsonify({'200':"team found",'info':resultats[0][3]})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>/id_game", methods=['GET'])
def getWhenGame(id_team):
	if request.method == 'GET':
		conn = sqlite3.connect("./teams.db", check_same_thread=False)
		curs = conn.cursor()
		curs.execute('''SELECT * FROM teams WHERE id_teams=''' + id_team)
		resultats=curs.fetchall()
		if str(id_team) == str(resultats[0][0]):
			conn.commit()
			conn.close()
			return jsonify({'200':"team found",'info':resultats[0][1]})
		conn.commit()
		conn.close()
		return jsonify({'404':"ID not found"})


if __name__ == '__main__':
	app.run(port=5000, debug="on")