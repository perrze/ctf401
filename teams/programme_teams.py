import uuid
from flask import *
import json
from collections import namedtuple
from types import SimpleNamespace as Namespace
import requests

dico = {
	"231ACDvfd615":
		{
			"id_team": "231ACDvfd615",
			"name": "Apprenti",
			"member": [1, 2, 3, 4, 5, 6, 7],
			"description": "Apprenti 1",
			"id_game": "ergs5fd2636",
		},

	"89esfFGe444":
		{
			"id_team": "89esfFGe444",
			"name": "champion",
			"member": [1, 2, 3, 4, 5, 6, 7],
			"description": "Apprenti 2",
			"id_game": "ergs5fd2636",
		},

	"231AefsDv99":
		{
			"id_team": "231AefsDv99",
			"name": "alza",
			"member": [1, 2, 3, 4, 5, 6, 7],
			"description": "Apprenti 3",
			"id_game": "ergs5fd2636",
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
    s = dico[id_team]
    return s



@app.route("/teams/<id_team>", methods=["DELETE"])
def deleteTeam(id_team):
	for team in dico :
		if (team['id_team'] == id_team) :
			dico.remove(team)
			return jsonify({'200':"team deleted"})
	return jsonify({'404':"ID not found"})

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
	l =  dico[id_team]["member"]
	return jsonify({"name" : l })




@app.route("/teams/member/{id_team}")
def getMembersTeam(id_team):
	return "getMembersTeam"


@app.route("/teams/member/{id_team}", methods=["DELETE"])
def deleteMemberTeam(id_team):
	return "deleteMemberTeam" 


@app.route("/teams/description/{id_team}")
def getDescriptionTeam(id_team):
	return "getDescriptionTeam" 


@app.route("/teams/{id_team}/{id_game}")
def getWhenGame(id_team,id_game):
	return "getWhenGame"


if __name__ == '__main__':
	app.run(port=8080, debug="on")