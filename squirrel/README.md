# Squirrel

A professional web search service for fetching real-time NFL player and team data with intelligent caching, rate limiting, and REST API endpoints.

## Features

- **REST API**: FastAPI-based REST endpoints for easy integration
- **Squirrel Manager**: Centralized management with dynamic source switching
- **Base Squirrel Architecture**: Extensible base class with common search functionality
- **Smart Caching**: Different cache TTL strategies
  - Team data: 24 hours (infrequent changes)
  - Player data: 5 minutes (frequent updates)
  - Live scores: No caching (real-time data)
- **Rate Limiting**: 
  - Configurable rate limiting per squirrel
  - Adaptive rate limiting that backs off on errors
- **Error Handling**: Robust retry logic with exponential backoff
- **Multiple Data Sources**: Support for ESPN and NFL.com APIs
- **Type Safety**: Full Pydantic models for data validation

## Installation

```bash
# Create virtual environment
python -m venv venv_squirrel

# Activate virtual environment
# Windows:
venv_squirrel\Scripts\activate
# Linux/Mac:
source venv_squirrel/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start - REST API

Start the API server:

```bash
python run.py
```

The API will be available at `http://localhost:8000`

### API Endpoints

#### Get all teams
```bash
curl http://localhost:8000/api/v1/teams

# With specific source
curl http://localhost:8000/api/v1/teams?source=espn
```

#### Get players
```bash
# All players
curl http://localhost:8000/api/v1/players

# Players for specific team
curl http://localhost:8000/api/v1/players?team_id=1
```

#### Get player stats
```bash
curl http://localhost:8000/api/v1/players/{player_id}/stats?season=2024
```

#### Get live scores
```bash
curl http://localhost:8000/api/v1/scores
```

#### Switch data source
```bash
curl -X POST http://localhost:8000/api/v1/sources/switch \
  -H "Content-Type: application/json" \
  -d '{"squirrel_type": "foolsball", "source": "nfl"}'
```

#### Get available sources
```bash
curl http://localhost:8000/api/v1/sources
```

#### Invalidate cache
```bash
# Invalidate all cache
curl -X POST http://localhost:8000/api/v1/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{}'

# Invalidate specific squirrel
curl -X POST http://localhost:8000/api/v1/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{"squirrel_type": "foolsball"}'

# Clear all cache
curl -X DELETE http://localhost:8000/api/v1/cache
```

#### Get squirrel stats
```bash
curl http://localhost:8000/api/v1/stats
```

### API Documentation

Interactive API documentation available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Quick Start - Python SDK

```python
from squirrel import SquirrelManager, SquirrelType

# Initialize squirrel manager
with SquirrelManager() as manager:
    # Get squirrel
    squirrel = manager.get_squirrel(SquirrelType.FOOLSBALL, source="espn")
    
    # Fetch teams (cached for 24 hours)
    teams = squirrel.get_teams()
    print(f"Found {len(teams)} teams")
    
    # Fetch players for a team (cached for 5 minutes)
    players = squirrel.get_players(team_id="1")
    print(f"Found {len(players)} players")
    
    # Fetch live scores (real-time, not cached)
    scores = squirrel.get_live_scores()
    print(f"Found {len(scores)} live games")
    
    # Switch data source
    manager.switch_source(SquirrelType.FOOLSBALL, "nfl")
    
    # Invalidate cache
    manager.invalidate_cache(SquirrelType.FOOLSBALL)
```

## Architecture

### Squirrel Manager (`squirrel_manager.py`)

Centralized manager for all squirrels:
- Dynamic squirrel instantiation
- Source switching per squirrel type
- Unified cache management
- Statistics and monitoring

### Base Squirrel (`base_squirrel.py`)

The foundation for all squirrels with:
- HTTP session management with retry logic
- Cache integration (in-memory or Redis)
- Rate limiting (standard or adaptive)
- Error handling and logging

### Foolsball Squirrel (`foolsball_squirrel.py`)

NFL-specific squirrel that extends BaseSquirrel:
- **Teams**: Cached for 24 hours
- **Players**: Cached for 5 minutes
- **Stats**: Cached for 5 minutes
- **Live Scores**: No caching (real-time)

### Data Models

Type-safe Pydantic models:
- `Team`: NFL team information
- `Player`: Player details and stats
- `PlayerStats`: Detailed player statistics
- `GameScore`: Live game scores
- `SquirrelResponse`: Standard API response wrapper

## Configuration

Edit `squirrel/config.py` to customize:

```python
# Cache TTL
CACHE_TTL_TEAM_DATA = 86400  # 24 hours
CACHE_TTL_PLAYER_DATA = 300  # 5 minutes

# Rate Limiting
RATE_LIMIT_CALLS = 10  # calls
RATE_LIMIT_PERIOD = 60  # seconds

# Use Redis for caching (optional)
USE_REDIS = True
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```

## Cache Strategy

The squirrel uses intelligent caching based on data freshness requirements:

| Data Type | TTL | Reasoning |
|-----------|-----|-----------|
| Teams | 24 hours | Team information changes infrequently |
| Players | 5 minutes | Player data updates regularly (injuries, roster changes) |
| Stats | 5 minutes | Stats update during games |
| Live Scores | No cache | Real-time data requires fresh fetches |

## Rate Limiting

### Standard Rate Limiter
- Fixed rate: 10 calls per 60 seconds (configurable)
- Blocks when limit reached

### Adaptive Rate Limiter
- Automatically backs off on errors
- Recovers rate on successful calls
- Ideal for unpredictable API behavior

## Example Usage

See `example_usage.py` for comprehensive examples:

```bash
python example_usage.py
```

## API Methods

### FoolsballSquirrel

```python
# Get all teams
teams = squirrel.get_teams()

# Get players (all or by team)
all_players = squirrel.get_players()
team_players = squirrel.get_players(team_id="1")

# Get specific player
player = squirrel.get_player(player_id="12345")

# Get player stats
stats = squirrel.get_player_stats(player_id="12345", season=2024)

# Get live scores
scores = squirrel.get_live_scores()

# Refresh cache
squirrel.refresh_team_data()
squirrel.refresh_player_data(player_id="12345")

# Generic scrape method
response = squirrel.scrape("teams")
response = squirrel.scrape("players", team_id="1")
response = squirrel.scrape("stats", player_id="12345", season=2024)
```

## Error Handling

The squirrel includes comprehensive error handling:

```python
from squirrels.base_squirrel import SquirrelException, RateLimitException, DataNotFoundException

try:
    teams = squirrel.get_teams()
except RateLimitException:
    print("Rate limit exceeded, wait and retry")
except DataNotFoundException:
    print("Data source unavailable")
except SquirrelException as e:
    print(f"Search error: {e}")
```

## Extending the Squirrel

Create custom squirrels by inheriting from `BaseSquirrel`:

```python
from squirrels.base_squirrel import BaseSquirrel

class MyCustomSquirrel(BaseSquirrel):
    def __init__(self):
        super().__init__(
            cache_enabled=True,
            rate_limit_enabled=True
        )
    
    def scrape(self, *args, **kwargs):
        # Implement your search logic
        cache_key = self._get_cache_key("my_data", *args)
        
        def fetch_data():
            response = self._make_request("https://api.example.com")
            return response.json()
        
        return self.fetch_with_cache(cache_key, fetch_data, ttl=3600)
```

## Testing

Run the example script to test the squirrel:

```bash
python example_usage.py
```

Monitor logs for cache hits/misses and rate limiting:

```
2024-10-08 10:30:15 - Cache hit: foolsball:teams:espn
2024-10-08 10:30:20 - Cache miss: foolsball:players:espn:1
2024-10-08 10:30:25 - Rate limit reached, waiting 2.5s
```

## Dependencies

- `requests`: HTTP client
- `pydantic`: Data validation
- `redis`: Optional caching backend
- `urllib3`: HTTP utilities

## License

See LICENSE file for details.

## Support

For issues or questions, please check the code documentation or create an issue in the repository.
