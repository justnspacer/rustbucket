import nfl_data_py as nfl
import pandas as pd
import json

def fetch_player_data():
    """Fetch comprehensive player data including performance metrics"""
    print("Fetching player data...")
    
    try:
        # Get seasonal roster data for basic player info
        print("Loading seasonal rosters...")
        rosters = nfl.import_seasonal_rosters(years=[2024])
        
        # Get seasonal data with performance metrics
        print("Loading seasonal performance data...")
        seasonal_data = nfl.import_seasonal_data(years=[2024], s_type='REG')
        
        # Merge roster data with seasonal performance data
        print("Merging player data...")
        player_data = pd.merge(
            rosters, 
            seasonal_data, 
            on=['player_id'], 
            how='left',
            suffixes=('_roster', '_stats')
        )
        
        # Select relevant columns for the frontend
        columns_to_keep = [
            # Basic player info
            'player_id', 'player_name', 'position', 'team', 'jersey_number',
            'height', 'weight', 'birth_date', 'college', 'years_exp',
            
            # Performance metrics from what_to_do_with_data.md
            'tgt_sh',      # target share
            'ay_sh',       # air yards share  
            'yac_sh',      # yards after catch share
            'wopr',        # weighted opportunity rating
            'ry_sh',       # receiving yards share
            'rtd_sh',      # receiving TDs share
            'rfd_sh',      # receiving 1st Downs share
            'rtdfd_sh',    # receiving TDs + 1st Downs share
            'dom',         # dominator rating
            'w8dom',       # weighted dominator rating
            'yptmpa',      # receiving yards per team pass attempt
            'ppr_sh',      # PPR fantasy points share
            
            # Additional useful stats
            'targets', 'receptions', 'receiving_yards', 'receiving_tds',
            'receiving_first_downs', 'receiving_epa', 'racr', 'target_share',
            'air_yards_share', 'wopr_x', 'fantasy_points_ppr'
        ]
        
        # Filter columns that actually exist in the data
        available_columns = [col for col in columns_to_keep if col in player_data.columns]
        player_data_filtered = player_data[available_columns].copy()
        
        # Remove rows without player names
        player_data_filtered = player_data_filtered.dropna(subset=['player_name'])
        
        # Fill NaN values with appropriate defaults
        numeric_columns = player_data_filtered.select_dtypes(include=['float64', 'int64']).columns
        player_data_filtered[numeric_columns] = player_data_filtered[numeric_columns].fillna(0)
        
        string_columns = player_data_filtered.select_dtypes(include=['object']).columns
        player_data_filtered[string_columns] = player_data_filtered[string_columns].fillna('')
        
        print(f"Processed {len(player_data_filtered)} players")
        print(f"Available columns: {list(player_data_filtered.columns)}")
        
        return player_data_filtered
        
    except Exception as e:
        print(f"Error fetching player data: {e}")
        return pd.DataFrame()

def save_player_data():
    """Save player data to JSON file"""
    player_data = fetch_player_data()
    
    if not player_data.empty:
        # Convert to JSON
        players_json = player_data.to_json(orient='records', indent=2)
        
        with open('players_data.json', 'w') as f:
            f.write(players_json)
        
        print(f"Player data saved to players_data.json ({len(player_data)} players)")
        
        # Show sample of data
        print("\nSample player data:")
        print(player_data.head()[['player_name', 'position', 'team']].to_string())
        
        # Show position breakdown
        print(f"\nPosition breakdown:")
        print(player_data['position'].value_counts().head(10))
        
    else:
        print("No player data to save")

if __name__ == "__main__":
    save_player_data()
