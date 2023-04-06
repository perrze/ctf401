from flask import Flask,request
import json
from collections import namedtuple
from types import SimpleNamespace as Namespace
import requests


app = Flask(__name__)


@app.route("/")
def Home():
	return "API Teams"


@app.route("/teams")
def getAllTeams():
	return "getAllTeams"


@app.route("/teams/{id_team}")
def getTeam(id_team):
	return "getTeam"


@app.route("/teams/{id_team}", methods=["DELETE"])
def deleteTeam(id_team):
	return "deleteTeam"

@app.route("/teams/{id_team}", methods=["PATCH"])
def patchTeam(id_team):
	return "patchTeam"


@app.route("/teams/{id_team}", methods=["PUT"])
def putTeam(id_team):
	return "putTeam"


@app.route("/teams/name")
def getAllNameTeam():
	return "getAllNameTeam"


@app.route("/teams/name/{id_team}")
def getNameTeam():
	return "getNameTeam"


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
	app.run(port=8080)