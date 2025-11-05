from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# Game state storage (in production, use database)
game_states = {}

@app.route('/')
def index():
    """Halaman utama game"""
    return render_template('index.html')

@app.route('/api/game/state', methods=['GET'])
def get_game_state():
    """Mendapatkan state game player"""
    player_id = request.args.get('player_id', 'default')
    if player_id in game_states:
        return jsonify(game_states[player_id])
    else:
        # State awal
        initial_state = {
            'player_id': player_id,
            'current_scene': 'ship',  # 'ship' atau 'harbor'
            'health': 100,
            'coins': 500,
            'inventory': {
                'spices': {}
            },
            'ship_position': {'x': 0, 'y': 0},
            'harbor_position': {'x': 0, 'y': 0},
            'story_progress': 0,
            'visited_islands': []
        }
        game_states[player_id] = initial_state
        return jsonify(initial_state)

@app.route('/api/game/state', methods=['POST'])
def save_game_state():
    """Menyimpan state game player"""
    player_id = request.json.get('player_id', 'default')
    game_states[player_id] = request.json
    return jsonify({'success': True, 'message': 'Game state disimpan'})

@app.route('/api/game/buy-spice', methods=['POST'])
def buy_spice():
    """Membeli spice di harbor"""
    data = request.json
    player_id = data.get('player_id', 'default')
    spice_name = data.get('spice_name')
    quantity = data.get('quantity', 1)
    price = data.get('price', 0)
    
    if player_id not in game_states:
        return jsonify({'success': False, 'message': 'Player tidak ditemukan'}), 404
    
    state = game_states[player_id]
    
    total_cost = price * quantity
    if state['coins'] < total_cost:
        return jsonify({'success': False, 'message': 'Uang tidak cukup'}), 400
    
    state['coins'] -= total_cost
    if spice_name not in state['inventory']['spices']:
        state['inventory']['spices'][spice_name] = 0
    state['inventory']['spices'][spice_name] += quantity
    
    game_states[player_id] = state
    return jsonify({'success': True, 'state': state})

@app.route('/api/game/change-scene', methods=['POST'])
def change_scene():
    """Mengubah scene (ship ke harbor atau sebaliknya)"""
    data = request.json
    player_id = data.get('player_id', 'default')
    new_scene = data.get('scene')
    
    if player_id not in game_states:
        return jsonify({'success': False, 'message': 'Player tidak ditemukan'}), 404
    
    game_states[player_id]['current_scene'] = new_scene
    return jsonify({'success': True, 'scene': new_scene, 'state': game_states[player_id]})

@app.route('/api/game/buy-food', methods=['POST'])
def buy_food():
    """Membeli makanan di restaurant"""
    data = request.json
    player_id = data.get('player_id', 'default')
    food_name = data.get('food_name')
    price = data.get('price', 0)
    
    if player_id not in game_states:
        return jsonify({'success': False, 'message': 'Player tidak ditemukan'}), 404
    
    state = game_states[player_id]
    
    if state['coins'] < price:
        return jsonify({'success': False, 'message': 'Uang tidak cukup'}), 400
    
    state['coins'] -= price
    
    # Track makanan yang sudah dicoba
    if 'tried_foods' not in state:
        state['tried_foods'] = []
    if food_name not in state['tried_foods']:
        state['tried_foods'].append(food_name)
    
    game_states[player_id] = state
    return jsonify({'success': True, 'message': f'Anda mencoba {food_name}', 'state': state})

@app.route('/api/game/inventory', methods=['GET'])
def get_inventory():
    """Mendapatkan inventory player"""
    player_id = request.args.get('player_id', 'default')
    
    if player_id not in game_states:
        return jsonify({'success': False, 'message': 'Player tidak ditemukan'}), 404
    
    state = game_states[player_id]
    return jsonify({
        'success': True,
        'inventory': state.get('inventory', {}),
        'coins': state.get('coins', 0),
        'tried_foods': state.get('tried_foods', [])
    })

@app.route('/api/game/story-progress', methods=['POST'])
def update_story_progress():
    """Update story progress"""
    data = request.json
    player_id = data.get('player_id', 'default')
    progress = data.get('progress', 0)
    
    if player_id not in game_states:
        return jsonify({'success': False, 'message': 'Player tidak ditemukan'}), 404
    
    game_states[player_id]['story_progress'] = progress
    return jsonify({'success': True, 'story_progress': progress})

if __name__ == '__main__':
    print("=" * 50)
    print("Flask Backend - Spice Trader 1400")
    print("=" * 50)
    print("Server berjalan di http://localhost:5000")
    print("API Endpoints:")
    print("  GET  /api/game/state")
    print("  POST /api/game/state")
    print("  POST /api/game/buy-spice")
    print("  POST /api/game/buy-food")
    print("  POST /api/game/change-scene")
    print("  GET  /api/game/inventory")
    print("=" * 50)
    app.run(debug=True, port=5000)

