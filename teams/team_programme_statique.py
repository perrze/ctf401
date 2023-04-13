import uuid
from flask import *
import json
from collections import namedtuple
from types import SimpleNamespace as Namespace
import requests

dico = [
	{
		"description": "Apprenti",
		"id_game": "11",
		"id_team": "1",
		"members": ["1", "2", "3", "4", "5", "6", "7"],
		"name": "Apprenti",
	},
		   {
		"description": "champion",
		"id_game": "22",
		"id_team": "2",
		"members": ["1", "2", "3", "4", "5", "6", "7"],
		"name": "champion",
	},
	{
		"description": "alza",
		"id_game": "33",
		"id_team": "3",
		"members": ["1", "2", "3", "4", "5", "6", "7"],
		"name": "alza",
	}
]


app = Flask(__name__)


@app.route("/", methods=['GET'])
def Home():
	if request.method == 'GET':
		return "API Teams"


@app.route("/teams", methods=['GET'])
def getAllTeams():
	if request.method == 'GET':
		return jsonify({'200':"all team found",'info':dico})


@app.route("/teams", methods=["POST"])
def postTeam():
	if request.method == 'POST':
		rep = request.json
		id_team = uuid.uuid4()
		description = rep['description']
		member = rep["faire appel à l'API"]
		name = rep["name"]
		id_game = "faire appel à l'API"
		team = {"id_team": id_team, "description": description, "member": member, "name": name, "id_game": id_game}
		dico.append(team)
		return jsonify({'200':"team created"})


@app.route("/teams/<id_team>", methods=['GET'])
def getTeam(id_team):
	if request.method == 'GET':
		for team in dico:
			if id_team == team["id_team"]:
				return jsonify({'200':"team found",'info':team["id_team"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>", methods=["DELETE"])
def deleteTeam(id_team):
	if request.method == 'DELETE':
		for team in dico :
			if (team['id_challenge'] == id_team) :
				dico.remove(team)
				return jsonify({'200':"team deleted"})
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>", methods=["PATCH"])
def patchTeam(id_team):
	if request.method == 'PATCH':
		for team in dico :
			if (team['id_team'] == id_team) :
				response = request.get_json()
				for key, value in response.items():
					if key in team:
						team[key] = value
						return jsonify({'200':"team Modified"})
		return jsonify({'404':"ID not found"})


@app.route("/teams/name", methods=['GET'])
def getAllNameTeam():
	if request.method == 'GET':
		liste_name=[]
		for i in dico:
			l = i["name"]
			liste_name.append(l)
		return liste_name
		return jsonify({'200':"name of all team has found","name" : liste_name})


@app.route("/teams/name/<id_team>", methods=['GET'])
def getNameTeam(id_team):
	if request.method == 'GET':
		for team in dico:
			if id_team == team["id_team"]:
				return jsonify({'200':"name of this team has found",'info':team["name"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>", methods=['GET'])
def getMembersTeam(id_team):
	if request.method == 'GET':
		for team in dico :
			if id_team == team["id_team"]:
				return jsonify({'200':"member for this team found",'info':team["members"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>", methods=["DELETE"])
def deleteMemberTeam(id_team):
	if request.method == 'DELETE':
		for team in dico :
			if (team['id_challenge'] == id_team) :
				dico.remove(team)
				return jsonify({'200':"member of team deleted"})
		return jsonify({'404':"ID not found"})


@app.route("/teams/description/<id_team>", methods=['GET'])
def getDescriptionTeam(id_team):
	if request.method == 'GET':
		for team in dico :
			if id_team == team["id_team"]:
				return jsonify({'200':"description for this team has found",'info':team["description"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>/id_game", methods=['GET'])
def getWhenGame(id_team):
	if request.method == 'GET':
		for team in dico :
			if id_team == team["id_team"]:
				return jsonify({'200':"team found",'info':team["id_game"]})
		return jsonify({'404':"ID not found"})


if __name__ == '__main__':
	app.run(port=5000, debug="on")