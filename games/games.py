from flask import Flask, jsonify, request
import re, uuid, sqlite3
import os

app = Flask(__name__)

#if "BASE_URL" in os.environ:
#    BASE_URL=os.getenv("BASE_URL")
#else:
#    BASE_URL="http://localhost"



uuid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
datetime_regex = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
not_empty_regex = r'^.+$'

#def check_if_user_access(request,role):
#  token = None
#  if "jwt" in request.headers:
#      token = request.headers["jwt"]
#  if not token:
#      return False
#  result = requests.post(BASE_URL+":5001/users/check/"+role,json={"token":token})
#  if result.status_code==200:
#    return True
#  else:
#    return False

#if not(check_if_user_access(request,"admin")):
#      return "Unauthorized", 401

games = [
{
  "id_game": "4a28ce6b-312b-4bb0-a394-0cd2d03ca311","date_start": "2022-04-04 07:30:30","date_end": "2023-04-04 07:30:30","name_game": "The First","description": "The First Game Of the Year",  "logo": "/user/logo.png"
},
{
  "id_game": "4a28ce6b-312b-4bb0-a394-0cd2d03ca312","date_start": "2023-05-05 07:20:00","date_end": "2023-05-06 07:20:00","name_game": "The Second","description": "The Second Game Of the Year","logo": "/user/logo2.png"
},
{
  "id_game": "4a28ce6b-312b-4bb0-a394-0cd2d03ca313","date_start": "2023-04-05 07:00:00","date_end": "2024-04-06 08:00:00","name_game": "The Third","description": "The Third Game Of the Year","logo": "/user/logo3.png"
}
]

@app.route("/")
def index():
	return "Welcome to API Games"


@app.route('/games')
def getGames():
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games')
    games = c.fetchall()
    conn.close()
    return jsonify(games)

        
@app.route('/games/<id_game>')
def getGameById(id_game):
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games WHERE id_game = ?', (id_game,))
    game = c.fetchall()
    conn.close()
    return jsonify(game)
    #return jsonify(f"Game with id {id_game} not found", 404)
    

@app.route('/games/<id_game>/dates')
def getGameByIdDates(id_game):
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games WHERE id_game = ?', (id_game,))
    game = c.fetchall()
    conn.close()
    return jsonify({"date_start": game["date_start"], "date_end": game["date_end"]})
    #return jsonify(f"Game with id {id_game} not found", 404)

    
@app.route('/games/<id_game>/modify', methods=['PATCH'])
def update_game(id_game):
    #data = request.get_json()
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games WHERE id_game = ?', (id_game,))
    game = c.fetchall()
    if game:
        for key, value in data.items():
            if key in game:
                if key == 'id_game':
                    if not re.match(uuid_regex, str(value)):
                        return jsonify(f"UUID is not valid", 400)
                elif key == 'date_start' or key == 'date_end':
                    if not re.match(datetime_regex, value):
                        return jsonify(f"The date and time format is not valid", 400)
                elif key == 'name_game' or key == 'description' or key == 'logo':
                    if not re.match(not_empty_regex, value):
                        return jsonify(f"Variables must not be empty", 400)
                c.execute(f'UPDATE games SET {key} = ? WHERE id_game = ?', (value, id_game))
        conn.commit()
        conn.close()
        return jsonify({'200':"Game Modified"})
    else:
        conn.close()
        return jsonify(f"Game with id {id_game} not found", 404)

	
@app.route('/games/create', methods=['POST'])
def create_game():
    #data = request.get_json()
    id_game = uuid.uuid4()
    date_start = data['date_start']
    date_end = data['date_end']
    name_game = data['name_game']
    description = data['description']
    logo = data['logo']

    if not re.match(uuid_regex, str(id_game)):
        return jsonify(f"UUID is not valid", 400)

    if not re.match(datetime_regex, date_start) or not re.match(datetime_regex, date_end):
        return jsonify(f"The date and time format is not valid", 400)

    if not re.match(not_empty_regex, name_game) or not re.match(not_empty_regex, description) or not re.match(not_empty_regex, logo):
        return jsonify(f"Variables must not be empty", 400)

    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('INSERT INTO games (id_game, date_start, date_end, name_game, description, logo) VALUES (?, ?, ?, ?, ?, ?)', (str(id_game), date_start, date_end, name_game, description, logo))
    conn.commit()
    conn.close()
    return jsonify({'200':"Game created"})


@app.route('/games/<id_game>/delete', methods=['DELETE'])
def delete_game(id_game):
    conn = sqlite3.connect('games.db')
    c = conn.cursor()
    c.execute('SELECT * FROM games WHERE id_game = ?', (id_game,))
    game = c.fetchone()
    if game:
        c.execute('DELETE FROM games WHERE id_game = ?', (id_game,))
        conn.commit()
        conn.close()
        return jsonify({'200':"Game Deleted"})
    else:
        conn.close()
        return jsonify(f"Game with id {id_game} not found", 404)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run(host="0.0.0.0")