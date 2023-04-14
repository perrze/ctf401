from flask import Flask, jsonify, request
import re, uuid, sqlite3, jwt, os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#if "BASE_URL" in os.environ:
#    BASE_URL=os.getenv("BASE_URL")
#else:
#    BASE_URL="http://localhost"

uuid_regex = r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[1-5][0-9a-fA-F]{3}-[89abAB][0-9a-fA-F]{3}-[0-9a-fA-F]{12}$'
datetime_regex = r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$'
not_empty_regex = r'^.+$'

def check_if_user_access(request,role):
    token = None
    if "jwt" in request.headers:
        token = request.headers["jwt"]
        if not token:
            return False
            result = requests.post("http://localhsot:5001/users/check/"+role,json={"token":token})
    if result.status_code==200:
        return True
    else:
        return False

@app.route("/")
def index():
	return "Welcome to API Games"


@app.route('/games')
def getGames():
	try:
		conn = sqlite3.connect('games.db')
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		c.execute('SELECT * FROM games')
		games = [dict(row) for row in c.fetchall()]
		conn.close()
		return jsonify(games)
	except sqlite3.Error as e:
		return jsonify(f"Database error: {e}", 500)
	except Exception as e:
		return jsonify(f"Error: {e}", 500)

@app.route('/games/<id_game>')
def getGameById(id_game):
	try:
		conn = sqlite3.connect('games.db')
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		c.execute('SELECT * FROM games WHERE id_game = ?', (id_game,))
		game = [dict(row) for row in c.fetchall()]
		conn.close()
		if game:
			return jsonify(game)
		else:
			return jsonify(f"Game with id {id_game} not found", 404)
	except sqlite3.Error as e:
		return jsonify(f"Database error: {e}", 500)
	except Exception as e:
		return jsonify(f"Error: {e}", 500)

@app.route('/games/<id_game>/dates')
def getGameByIdDates(id_game):
	try:
		conn = sqlite3.connect('games.db')
		conn.row_factory = sqlite3.Row
		c = conn.cursor()
		c.execute('SELECT date_start, date_end FROM games WHERE id_game = ?', (id_game,))
		game = [dict(row) for row in c.fetchall()]
		conn.close()
		if game:
			return jsonify(game)
		else:
			return jsonify(f"Game with id {id_game} not found", 404)
	except sqlite3.Error as e:
		return jsonify(f"Database error: {e}", 500)
	except Exception as e:
		return jsonify(f"Error: {e}", 500)

@app.route('/games/<id_game>/modify', methods=['PATCH'])
def update_game(id_game):
#    if not(check_if_user_access(request,"admin")):
#        return "Unauthorized", 401
	try:
		data = request.get_json()
		conn = sqlite3.connect('games.db')
		c = conn.cursor()
		c.execute('SELECT * FROM games WHERE id_game = ?', (id_game,))
		game = c.fetchone()
		if game:
			game_dict = dict(zip([column[0] for column in c.description], game))
			for key, value in data.items():
				if key in game_dict:
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
	except sqlite3.Error as e:
		return jsonify(f"Database error: {e}", 500)
	except Exception as e:
		return jsonify(f"Error: {e}", 500)

@app.route('/games/create', methods=['POST'])
def create_game():
#    if not(check_if_user_access(request,"admin")):
#        return "Unauthorized", 401
	try:
		data = request.get_json()
		id_game = str(uuid.uuid4())
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
		c.execute('INSERT INTO games (id_game, date_start, date_end, name_game, description, logo) VALUES (?, ?, ?, ?, ?, ?)', (id_game, date_start, date_end, name_game, description, logo))
		conn.commit()
		conn.close()
		return jsonify({'200':"Game created"})
	except sqlite3.Error as e:
		return jsonify(f"Database error: {e}", 500)
	except Exception as e:
		return jsonify(f"Error: {e}", 500)

@app.route('/games/<id_game>/delete', methods=['DELETE'])
def delete_game(id_game):
#    if not(check_if_user_access(request,"admin")):
#        return "Unauthorized", 401
	try:
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
	except sqlite3.Error as e:
		return jsonify(f"Database error: {e}", 500)
	except Exception as e:
		return jsonify(f"Error: {e}", 500)

@app.errorhandler(401)
def unauthorized(error):
	return jsonify(f"Unauthorized: {error}", 401)

@app.errorhandler(404)
def not_found(error):
	return jsonify(f"Not Found: {error}", 404)

@app.errorhandler(405)
def method_not_allowed(error):
	return jsonify(f"Method Not Allowed: {error}", 405)

@app.errorhandler(500)
def internal_server_error(error):
	return jsonify(f"Internal Server Error: {error}", 500)

if __name__ == '__main__':
	logging.basicConfig(level=logging.DEBUG)
	app.run(host="0.0.0.0")