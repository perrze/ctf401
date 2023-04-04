from flask import Flask, jsonify


app = Flask(__name__)

games = [
{
  "id_game": "4a28ce6b-312b-4bb0-a394-0cd2d03ca31a","date_start": "2023-04-03T07:30:38.467Z","date_end": "2023-04-03T07:28:308.467Z","name_game": "The First","description": "The First Game Of the Year",  "logo": "/user/logo.png"
},
{
  "id_game": "5a28ce6b-312b-4bb0-a394-0cd2d03ca31a","date_start": "2022-04-03T07:28:38.467Z","date_end": "2022-04-03T07:28:38.467Z","name_game": "The Second","description": "The Second Game Of the Year","logo": "/user/logo2.png"
}
]

@app.route('/games')
def gamesAll():
        return jsonify(games)
        
        
@app.route('/games/<id_game>')
def gameInfo(id_game):
    for game in games:
        if game['id_game'] == id_game:
            return jsonify(game)
    return jsonify(f"Game with id {id_game} not found", 404)
    
    
@app.route('/games/<id_game>/dates')
def gameDates(id_game):
    for game in games:
        if game['id_game'] == id_game:
            return jsonify({"date_start": game["date_start"], "date_end": game["date_end"]})
    return jsonify(f"Game with id {id_game} not found", 404)
    


if __name__ == '__main__':
    app.run(debug=True)