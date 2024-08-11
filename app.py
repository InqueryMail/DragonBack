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
import uuid

app = Flask(__name__)
CORS(app)

games = {}

@app.route('/create_game', methods=['POST'])
def create_game():
    data = request.json
    player_name = data.get('playerName', 'Player 1')
    game_id = str(uuid.uuid4())
    games[game_id] = {
        'player1_name': player_name,
        'player2_name': None,
        'player1_ready': False,
        'player2_ready': False,
        'health_one': 100,
        'health_two': 100,
        'damage_one': 0,
        'damage_two': 0,
        'game_over': False,
        'winner': None
    }
    return jsonify({'game_id': game_id})

@app.route('/join_game/<game_id>', methods=['POST'])
def join_game(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'})
    data = request.json
    player_name = data.get('playerName', 'Player 2')
    game = games[game_id]
    if game['player2_name'] is not None:
        return jsonify({'error': 'Game is full'})
    game['player2_name'] = player_name
    return jsonify({'message': 'Joined game successfully', 'game_id': game_id})

@app.route('/game_state/<game_id>', methods=['GET'])
def game_state(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'})
    return jsonify(games[game_id])

@app.route('/set_player_ready/<game_id>/<player>', methods=['POST'])
def set_player_ready(game_id, player):
    if game_id not in games:
        return jsonify({'error': 'Game not found'})
    game = games[game_id]
    if player == 'player1':
        game['player1_ready'] = True
        return jsonify({'message': 'Player 1 is ready'})
    elif player == 'player2':
        game['player2_ready'] = True
        return jsonify({'message': 'Player 2 is ready'})
    else:
        return jsonify({'error': 'Invalid player'})

@app.route('/attack/<game_id>', methods=['POST'])
def attack(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'})
    data = request.json
    player = data.get('player')
    game = games[game_id]
    if game['game_over']:
        return jsonify({'error': 'Game is over'})
    if player == 'player1':
        # Implement attack logic for player 1
        pass
    elif player == 'player2':
        # Implement attack logic for player 2
        pass
    return jsonify({'message': 'Attack executed'})

@app.route('/special_move/<game_id>', methods=['POST'])
def special_move(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'})
    data = request.json
    player = data.get('player')
    game = games[game_id]
    if game['game_over']:
        return jsonify({'error': 'Game is over'})
    if player == 'player1':
        # Implement special move logic for player 1
        pass
    elif player == 'player2':
        # Implement special move logic for player 2
        pass
    return jsonify({'message': 'Special move executed'})

@app.route('/restart/<game_id>', methods=['POST'])
def restart_game(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'})
    # Implement game restart logic
    return jsonify({'message': 'Game restarted'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
