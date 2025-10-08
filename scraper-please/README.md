# Scraper-Please

A professional web scraping service for fetching real-time NFL player and team data with intelligent caching and rate limiting.

## Features

- **Base Scraper Architecture**: Extensible base class with common scraping functionality
- **Smart Caching**: Different cache TTL strategies
  - Team data: 24 hours (infrequent changes)
  - Player data: 5 minutes (frequent updates)
  - Live scores: No caching (real-time data)
- **Rate Limiting**: 
  - Configurable rate limiting per scraper
  - Adaptive rate limiting that backs off on errors
- **Error Handling**: Robust retry logic with exponential backoff
- **Multiple Data Sources**: Support for ESPN and NFL.com APIs
- **Type Safety**: Full Pydantic models for data validation

## Installation

```bash
# Create virtual environment
python -m venv venv_scraper_please

# Activate virtual environment
# Windows:
venv_scraper-please\Scripts\activate
# Linux/Mac:
source venv_scraper-please/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Quick Start

```python
from scrapers.foolsball_scraper import FoolsballScraper

# Initialize scraper
scraper = FoolsballScraper(
    source="espn",
    cache_enabled=True,
    rate_limit_enabled=True
)

# Fetch teams (cached for 24 hours)
teams = scraper.get_teams()
print(f"Found {len(teams)} teams")

# Fetch players for a team (cached for 5 minutes)
players = scraper.get_players(team_id="1")
print(f"Found {len(players)} players")

# Fetch live scores (real-time, not cached)
scores = scraper.get_live_scores()
print(f"Found {len(scores)} live games")

# Clean up
scraper.close()
```

## Architecture

### Base Scraper (`base_scraper.py`)

The foundation for all scrapers with:
- HTTP session management with retry logic
- Cache integration (in-memory or Redis)
- Rate limiting (standard or adaptive)
- Error handling and logging

### Foolsball Scraper (`foolsball_scraper.py`)

NFL-specific scraper that extends BaseScraper:
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
- `ScraperResponse`: Standard API response wrapper

## Configuration

Edit `config.py` to customize:

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

The scraper uses intelligent caching based on data freshness requirements:

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

### FoolsballScraper

```python
# Get all teams
teams = scraper.get_teams()

# Get players (all or by team)
all_players = scraper.get_players()
team_players = scraper.get_players(team_id="1")

# Get specific player
player = scraper.get_player(player_id="12345")

# Get player stats
stats = scraper.get_player_stats(player_id="12345", season=2024)

# Get live scores
scores = scraper.get_live_scores()

# Refresh cache
scraper.refresh_team_data()
scraper.refresh_player_data(player_id="12345")

# Generic scrape method
response = scraper.scrape("teams")
response = scraper.scrape("players", team_id="1")
response = scraper.scrape("stats", player_id="12345", season=2024)
```

## Error Handling

The scraper includes comprehensive error handling:

```python
from scrapers.base_scraper import ScraperException, RateLimitException, DataNotFoundException

try:
    teams = scraper.get_teams()
except RateLimitException:
    print("Rate limit exceeded, wait and retry")
except DataNotFoundException:
    print("Data source unavailable")
except ScraperException as e:
    print(f"Scraping error: {e}")
```

## Extending the Scraper

Create custom scrapers by inheriting from `BaseScraper`:

```python
from scrapers.base_scraper import BaseScraper

class MyCustomScraper(BaseScraper):
    def __init__(self):
        super().__init__(
            cache_enabled=True,
            rate_limit_enabled=True
        )
    
    def scrape(self, *args, **kwargs):
        # Implement your scraping logic
        cache_key = self._get_cache_key("my_data", *args)
        
        def fetch_data():
            response = self._make_request("https://api.example.com")
            return response.json()
        
        return self.fetch_with_cache(cache_key, fetch_data, ttl=3600)
```

## Testing

Run the example script to test the scraper:

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
