import uuid
from flask import *
import json
from collections import namedtuple
from types import SimpleNamespace as Namespace
import requests

dico = {
	"1":
		{
			"description": "Apprenti",
			"id_game": "11",
			"id_team": "1",
			"members": ["1", "2", "3", "4", "5", "6", "7"],
			"name": "Apprenti",
		},

	"2":
		{
			"description": "champion",
			"id_game": "22",
			"id_team": "2",
			"members": ["1", "2", "3", "4", "5", "6", "7"],
			"name": "champion",
		},

	"3":
		{
			"description": "alza",
			"id_game": "33",
			"id_team": "3",
			"members": ["1", "2", "3", "4", "5", "6", "7"],
			"name": "alza",
		}

}

#(([0-9a-z]{8})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{4})-([0-9a-z]{12}))


app = Flask(__name__)


@app.route("/")
def Home():
	return "API Teams"


@app.route("/teams")
def getAllTeams():
	return dico



@app.route("/teams/<id_team>")
def getTeam(id_team):
	for team in dico :
		if str(id_team) == str(team):
			return jsonify({'200':"team found",'info':dico[id_team]})
	return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>", methods=["DELETE"])
def deleteTeam(id_team):
	return "deleteTeam"

@app.route("/teams/<id_team>", methods=["PATCH"])
def patchTeam(id_team):
	return "patchTeam"


@app.route("/teams/<id_team>", methods=["POST"])
def postTeam(id_team):
	return "postTeam"


@app.route("/teams/name")
def getAllNameTeam():
	liste_name=[]
	for i in dico:
		l =  dico[i]["name"]
		liste_name.append(l)
	print(liste_name)
	return jsonify({"name" : liste_name})


@app.route("/teams/name/<id_team>")
def getNameTeam(id_team):
	for team in dico :
		if str(id_team) == str(team):
			return jsonify({'200':"team found",'info':dico[id_team]["name"]})
	return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>")
def getMembersTeam(id_team):
	for team in dico :
		if str(id_team) == str(team):
			return jsonify({'200':"team found",'info':dico[id_team]["members"]})
	return jsonify({'404':"ID not found"})


@app.route("/teams/member/<id_team>", methods=["DELETE"])
def deleteMemberTeam(id_team):
	return "deleteMemberTeam"


@app.route("/teams/description/<id_team>")
def getDescriptionTeam(id_team):
	for team in dico :
		if str(id_team) == str(team):
			return jsonify({'200':"team found",'info':dico[id_team]["description"]})
	return jsonify({'404':"ID not found"})


@app.route("/teams/<id_team>/id_game")
def getWhenGame(id_team):
	for team in dico :
		if str(id_team) == str(team):
			return jsonify({'200':"team found",'info':dico[id_team]["id_game"]})
	return jsonify({'404':"ID not found"})


if __name__ == '__main__':
	app.run(port=8080, debug="on")