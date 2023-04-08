import uuid
from flask import *
import json
from collections import namedtuple
from types import SimpleNamespace as Namespace
import requests

dico = [
	{"description": "Apprenti",
	"id_game": "11",
	"id_team": "1",
	"members": ["1", "2", "3", "4", "5", "6", "7"],
	"name": "Apprenti",},
	{"description": "champion",
	"id_game": "22",
	"id_team": "2",
	"members": ["1", "2", "3", "4", "5", "6", "7"],
	"name": "champion",},
	{"description": "alza",
	"id_game": "33",
	"id_team": "3",
	"members": ["1", "2", "3", "4", "5", "6", "7"],
	"name": "alza",}]

print(dico["description"])
#(([0-9a-z]{8})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{12}))


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
		rep = request.get_json()
		id_team = uuid.uuid4()
		description = rep['description']
		member = rep['member']
		name = rep['name']
		id_game = "faire appel à l'API"
		team = {"id_team": id_team, "description": description, "member": member, "nama": name, "id_game": id_game}
		dico.append(team)
		return jsonify({'200':"Challenge created"})



@app.route("/teams/<id_team>", methods=['GET'])
def getTeam(id_team):
	if request.method == 'GET':
		for team in dico :
			if str(id_team) == str(team):
				return jsonify({'200':"team found",'info':dico[id_team]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>", methods=["DELETE"])
def deleteTeam(id_team):
	if request.method == 'DELETE':
		return "deleteTeam"

@app.route("/teams/<id_team>", methods=["PATCH"])
def patchTeam(id_team):
	if request.method == 'PATCH':
		return "patchTeam"


@app.route("/teams/name", methods=['GET'])
def getAllNameTeam():
	if request.method == 'GET':
		liste_name=[]
		for i in dico:
			l =  dico["name"]
			liste_name.append(l)
		return jsonify({'200':"name of all team has found","name" : liste_name})


@app.route("/teams/name/<id_team>", methods=['GET'])
def getNameTeam(id_team):
	if request.method == 'GET':
		for team in dico :
			if str(id_team) == str(team):
				return jsonify({'200':"name of this team has found",'info':dico[id_team]["name"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>", methods=['GET'])
def getMembersTeam(id_team):
	if request.method == 'GET':
		for team in dico :
			if str(id_team) == str(team):
				return jsonify({'200':"member for this team found",'info':dico[id_team]["members"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>", methods=["DELETE"])
def deleteMemberTeam(id_team):
	if request.method == 'DELETE':
		return "deleteMemberTeam"


@app.route("/teams/description/<id_team>", methods=['GET'])
def getDescriptionTeam(id_team):
	if request.method == 'GET':
		for team in dico :
			if str(id_team) == str(team):
				return jsonify({'200':"description for this team has found",'info':dico[id_team]["description"]})
		return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>/id_game", methods=['GET'])
def getWhenGame(id_team):
	if request.method == 'GET':
		for team in dico :
			if str(id_team) == str(team):
				return jsonify({'200':"team found",'info':dico[id_team]["id_game"]})
		return jsonify({'404':"ID not found"})


if __name__ == '__main__':
	app.run(port=8080, debug="on")