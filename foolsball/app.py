from flask import Flask, jsonify, send_from_directory, render_template_string, request
import nfl_data_py as nfl
import os
import pandas as pd
import numpy as np
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Cache for team and player data
teams_cache = None
players_cache = None

def get_teams_data():
    global teams_cache
    if teams_cache is None:
        try:
            teams_cache = nfl.import_team_desc()
        except Exception as e:
            print(f"Error loading team data: {e}")
            teams_cache = []
    return teams_cache

def get_players_data():
    global players_cache
    if players_cache is None:
        try:
            # Try to load from JSON file first
            with open('players_data.json', 'r') as f:
                import json
                players_cache = json.load(f)
                print(f"Loaded {len(players_cache)} players from cache")
        except Exception as e:
            print(f"Error loading player data from cache: {e}")
            print("Generating fresh player data...")
            try:
                from player_data import fetch_player_data
                df = fetch_player_data()
                if not df.empty:
                    players_cache = df.to_dict('records')
                    # Save to cache
                    with open('players_data.json', 'w') as f:
                        json.dump(players_cache, f, indent=2)
                else:
                    players_cache = []
            except Exception as fetch_error:
                print(f"Error fetching fresh player data: {fetch_error}")
                players_cache = []
    return players_cache

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

@app.route('/api/teams')
def api_teams():
    """API endpoint to get all team data"""
    try:
        teams = get_teams_data()
        if teams is None or len(teams) == 0:
            return jsonify({'error': 'No team data available'}), 500
            
        # Convert to dict and handle any NaN values
        teams_dict = teams.to_dict('records')
        
        # Clean up any NaN values that might cause JSON serialization issues
        # Replace NaN with None for JSON serialization
        for team in teams_dict:
            for key, value in team.items():
                if pd.isna(value) or (isinstance(value, float) and np.isnan(value)):
                    team[key] = None
                    
        print(f"Serving {len(teams_dict)} teams via API")
        return jsonify(teams_dict)
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/teams/<team_abbr>')
def api_team_detail(team_abbr):
    """API endpoint to get specific team data"""
    try:
        teams = get_teams_data()
        team = teams[teams['team_abbr'] == team_abbr.upper()]
        if len(team) > 0:
            return jsonify(team.iloc[0].to_dict())
        else:
            return jsonify({'error': 'Team not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/conferences')
def api_conferences():
    """API endpoint to get all conferences"""
    try:
        teams = get_teams_data()
        conferences = teams['team_conf'].unique().tolist()
        return jsonify(conferences)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/divisions')
def api_divisions():
    """API endpoint to get all divisions"""
    try:
        teams = get_teams_data()
        divisions = teams['team_division'].unique().tolist()
        return jsonify(sorted(divisions))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/players')
def api_players():
    """API endpoint to get all player data"""
    try:
        players = get_players_data()
        if not players:
            return jsonify({'error': 'No player data available'}), 500
            
        print(f"Serving {len(players)} players via API")
        return jsonify(players)
    except Exception as e:
        print(f"Player API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/search')
def api_players_search():
    """API endpoint to search players by name or position"""
    try:
        players = get_players_data()
        if not players:
            return jsonify([])
            
        # Get query parameters
        name_query = request.args.get('name', '').lower()
        position_filter = request.args.get('position', '')
        team_filter = request.args.get('team', '')
        limit = int(request.args.get('limit', 50))
        
        filtered_players = []
        
        for player in players:
            # Name search
            if name_query and name_query not in player.get('player_name', '').lower():
                continue
                
            # Position filter
            if position_filter and player.get('position', '') != position_filter:
                continue
                
            # Team filter
            if team_filter and player.get('team', '') != team_filter:
                continue
                
            filtered_players.append(player)
            
            # Limit results
            if len(filtered_players) >= limit:
                break
        
        return jsonify(filtered_players)
    except Exception as e:
        print(f"Player search API error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/players/<player_id>')
def api_player_detail(player_id):
    """API endpoint to get specific player data"""
    try:
        players = get_players_data()
        player = next((p for p in players if p.get('player_id') == player_id), None)
        
        if player:
            return jsonify(player)
        else:
            return jsonify({'error': 'Player not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/positions')
def api_positions():
    """API endpoint to get all positions"""
    try:
        players = get_players_data()
        if not players:
            return jsonify([])
            
        positions = list(set(p.get('position', '') for p in players if p.get('position')))
        return jsonify(sorted(positions))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("Starting NFL Teams Dashboard...")
    print("Loading team data...")
    
    # Pre-load team data
    get_teams_data()
    print(f"Loaded {len(teams_cache)} teams")
    
    print("Server starting at http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
