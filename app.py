# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import random

# app = Flask(__name__)
# CORS(app)

# games = {}

# def create_game():
#     return {
#         "healthOne": 100,
#         "damageOne": 0,
#         "healthTwo": 100,
#         "damageTwo": 0,
#         "gameOver": False,
#         "winner": None
#     }

# @app.route('/create_game', methods=['POST'])
# def create_game_route():
#     game_id = str(random.randint(1000, 9999))  # Simple game ID generation
#     games[game_id] = create_game()
#     return jsonify({"game_id": game_id})

# @app.route('/join_game/<game_id>', methods=['POST'])
# def join_game(game_id):
#     if game_id not in games:
#         return jsonify({"error": "Game not found"}), 404
#     return jsonify({"game_id": game_id})

# @app.route('/attack/<game_id>', methods=['POST'])
# def attack(game_id):
#     if game_id not in games:
#         return jsonify({"error": "Game not found"}), 404
#     data = request.json
#     player = data['player']
#     damage = random.randint(1, 5)
#     game = games[game_id]
#     if player == 'player1':
#         game['damageOne'] = damage
#         game['healthTwo'] = max(game['healthTwo'] - damage, 0)
#         if game['healthTwo'] == 0:
#             game['gameOver'] = True
#             game['winner'] = 'Heet'
#     else:
#         game['damageTwo'] = damage
#         game['healthOne'] = max(game['healthOne'] - damage, 0)
#         if game['healthOne'] == 0:
#             game['gameOver'] = True
#             game['winner'] = 'Himesh'
#     return jsonify(game)

# @app.route('/special_move/<game_id>', methods=['POST'])
# def special_move(game_id):
#     if game_id not in games:
#         return jsonify({"error": "Game not found"}), 404
#     data = request.json
#     player = data['player']
#     special_damage = 25
#     game = games[game_id]
#     if player == 'player1':
#         game['damageOne'] = special_damage
#         game['healthTwo'] = max(game['healthTwo'] - special_damage, 0)
#         if game['healthTwo'] == 0:
#             game['gameOver'] = True
#             game['winner'] = 'Player 2'
#     else:
#         game['damageTwo'] = special_damage
#         game['healthOne'] = max(game['healthOne'] - special_damage, 0)
#         if game['healthOne'] == 0:
#             game['gameOver'] = True
#             game['winner'] = 'Player 1'
#     return jsonify(game)

# @app.route('/game_state/<game_id>', methods=['GET'])
# def get_game_state(game_id):
#     if game_id not in games:
#         return jsonify({"error": "Game not found"}), 404
#     return jsonify(games[game_id])

# @app.route('/restart/<game_id>', methods=['POST'])
# def restart_game(game_id):
#     if game_id not in games:
#         return jsonify({"error": "Game not found"}), 404
#     games[game_id] = create_game()
#     return jsonify(games[game_id])

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000)







from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

games = {}
player_states = {}

def create_game():
    return {
        "healthOne": 100,
        "damageOne": 0,
        "healthTwo": 100,
        "damageTwo": 0,
        "gameOver": False,
        "winner": None,
        "player1Ready": False,
        "player2Ready": False
    }

@app.route('/create_game', methods=['POST'])
def create_game_route():
    game_id = str(random.randint(1000, 9999))
    games[game_id] = create_game()
    player_states[game_id] = {'player1': False, 'player2': False}
    return jsonify({"game_id": game_id})

@app.route('/join_game/<game_id>', methods=['POST'])
def join_game(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    if player_states[game_id]['player2']:
        return jsonify({"error": "Game already has two players"}), 400

    player_states[game_id]['player2'] = True
    game = games[game_id]
    
    return jsonify({"message": "Second player joined the game", "game_state": game})

@app.route('/set_player_ready/<game_id>/<player>', methods=['POST'])
def set_player_ready(game_id, player):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    if player not in ['player1', 'player2']:
        return jsonify({"error": "Invalid player"}), 400

    player_states[game_id][player] = True
    game = games[game_id]

    if player_states[game_id]['player1'] and player_states[game_id]['player2']:
        return jsonify({"message": "Both players are ready. The game can start."})
    else:
        return jsonify({"message": f"{player} is now ready."})

@app.route('/attack/<game_id>', methods=['POST'])
def attack(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    if not (player_states[game_id]['player1'] and player_states[game_id]['player2']):
        return jsonify({"error": "Both players need to be ready to start the game"}), 400

    data = request.json
    player = data['player']
    damage = random.randint(1, 5)

    if player == 'player1':
        game['damageOne'] = damage
        game['healthTwo'] = max(game['healthTwo'] - damage, 0)
        if game['healthTwo'] == 0:
            game['gameOver'] = True
            game['winner'] = 'Heet'
    else:
        game['damageTwo'] = damage
        game['healthOne'] = max(game['healthOne'] - damage, 0)
        if game['healthOne'] == 0:
            game['gameOver'] = True
            game['winner'] = 'Himesh'

    return jsonify(game)

@app.route('/special_move/<game_id>', methods=['POST'])
def special_move(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    if not (player_states[game_id]['player1'] and player_states[game_id]['player2']):
        return jsonify({"error": "Both players need to be ready to start the game"}), 400

    data = request.json
    player = data['player']
    special_damage = 25

    if player == 'player1':
        game['damageOne'] = special_damage
        game['healthTwo'] = max(game['healthTwo'] - special_damage, 0)
        if game['healthTwo'] == 0:
            game['gameOver'] = True
            game['winner'] = 'Player 2'
    else:
        game['damageTwo'] = special_damage
        game['healthOne'] = max(game['healthOne'] - special_damage, 0)
        if game['healthOne'] == 0:
            game['gameOver'] = True
            game['winner'] = 'Player 1'

    return jsonify(game)

@app.route('/game_state/<game_id>', methods=['GET'])
def get_game_state(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    game = games[game_id]
    return jsonify({
        **game,
        "player1Ready": player_states[game_id]['player1'],
        "player2Ready": player_states[game_id]['player2']
    })

@app.route('/restart/<game_id>', methods=['POST'])
def restart_game(game_id):
    if game_id not in games:
        return jsonify({"error": "Game not found"}), 404

    if not games[game_id]['gameOver']:
        return jsonify({"error": "Game is not over yet"}), 400

    games[game_id] = create_game()
    player_states[game_id] = {'player1': False, 'player2': False}
    return jsonify(games[game_id])

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
