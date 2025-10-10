# Quick Reference Guide

## Starting the API Server

```bash
# Activate virtual environment
venv_scraper_please\Scripts\activate  # Windows
source venv_scraper_please/bin/activate  # Linux/Mac

# Start server
python run.py
```

Server will be available at: `http://localhost:8000`

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Common API Calls

### Get Teams
```bash
curl http://localhost:8000/api/v1/teams
```

### Get Players for Team
```bash
curl "http://localhost:8000/api/v1/players?team_id=1"
```

### Get Live Scores
```bash
curl http://localhost:8000/api/v1/scores
```

### Switch Data Source
```bash
curl -X POST http://localhost:8000/api/v1/sources/switch \
  -H "Content-Type: application/json" \
  -d '{"scraper_type": "foolsball", "source": "nfl"}'
```

### Get Available Sources
```bash
curl http://localhost:8000/api/v1/sources
```

### Clear Cache
```bash
curl -X DELETE http://localhost:8000/api/v1/cache
```

### Get Scraper Stats
```bash
curl http://localhost:8000/api/v1/stats
```

## Python SDK Usage

### Using ScraperManager (Recommended)

```python
from scraper_please import ScraperManager, ScraperType

# Context manager handles cleanup automatically
with ScraperManager() as manager:
    # Get scraper
    scraper = manager.get_scraper(ScraperType.FOOLSBALL)
    
    # Fetch data
    teams = scraper.get_teams()
    players = scraper.get_players(team_id="1")
    scores = scraper.get_live_scores()
    
    # Switch source
    manager.switch_source(ScraperType.FOOLSBALL, "nfl")
    
    # Clear cache
    manager.invalidate_cache()
```

### Using Scraper Directly

```python
from scraper_please import FoolsballScraper

scraper = FoolsballScraper(
    source="espn",
    cache_enabled=True,
    rate_limit_enabled=True
)

try:
    teams = scraper.get_teams()
    players = scraper.get_players(team_id="1")
finally:
    scraper.close()
```

## Cache Strategy

| Data Type | Cache TTL | API Parameter |
|-----------|-----------|---------------|
| Teams | 24 hours | `team_id` optional |
| Players | 5 minutes | `team_id` optional filter |
| Player Stats | 5 minutes | `season` optional |
| Live Scores | No cache | Real-time |

## Available Data Sources

- **ESPN**: Default, most comprehensive
- **NFL**: Alternative source

Switch between them using:
- API: `POST /api/v1/sources/switch`
- SDK: `manager.switch_source(ScraperType.FOOLSBALL, "nfl")`

## Monitoring & Health

### Health Check
```bash
curl http://localhost:8000/health
```

### Scraper Statistics
```bash
curl http://localhost:8000/api/v1/stats
```

Returns:
- Active scrapers count
- Active sources per scraper type
- Rate limiter statistics
- Cache status

## Error Handling

All errors return:
```json
{
  "error": "Error type",
  "detail": "Error details",
  "timestamp": "2025-10-10T12:00:00"
}
```

HTTP Status Codes:
- `200` - Success
- `400` - Bad request
- `404` - Not found
- `500` - Server error

## Configuration

Edit `scraper_please/config.py`:

```python
# Cache TTL (seconds)
CACHE_TTL_TEAM_DATA = 86400  # 24 hours
CACHE_TTL_PLAYER_DATA = 300  # 5 minutes

# Rate Limiting
RATE_LIMIT_CALLS = 10  # calls per period
RATE_LIMIT_PERIOD = 60  # seconds

# Redis (optional)
USE_REDIS = False
```

## Running Examples

```bash
# Run example scripts
python example_usage.py

# Run tests
python test_refactor.py
```

## Project Structure

```
scraper-please/
├── api/                  # REST API
│   ├── routes.py        # API endpoints
│   └── schemas.py       # Request/response models
├── scraper_please/      # Core package
│   ├── scraper_manager.py  # Centralized manager
│   ├── scrapers/        # Scraper implementations
│   ├── models/          # Data models
│   └── utils/           # Utilities (cache, rate limiter)
├── run.py              # FastAPI server
├── example_usage.py    # Usage examples
└── test_refactor.py    # Tests
```

## Tips & Best Practices

1. **Use ScraperManager** for most use cases - it handles lifecycle automatically
2. **Use Context Managers** (`with` statement) to ensure cleanup
3. **Enable Caching** for frequently accessed data (teams, players)
4. **Monitor Rate Limits** using `/api/v1/stats` endpoint
5. **Switch Sources** if one API is slow or rate-limited
6. **Invalidate Cache** after major data updates (trades, injuries)
7. **Use API** for language-agnostic integration
8. **Check Health** endpoint for monitoring/alerting

## Troubleshooting

### Server won't start
- Check Python version (3.6+)
- Verify dependencies: `pip install -r requirements.txt`
- Check port 8000 is available

### Rate Limited
- Check stats: `curl http://localhost:8000/api/v1/stats`
- Switch to different source
- Adjust `RATE_LIMIT_CALLS` in config

### Stale Data
- Clear cache: `curl -X DELETE http://localhost:8000/api/v1/cache`
- Or invalidate specific cache via API

### Import Errors
- Ensure virtual environment is activated
- Reinstall: `pip install -e .`

## Support

- Documentation: `README.md`
- API Docs: `API_DOCS.md`
- Refactoring Notes: `REFACTORING_SUMMARY.md`
- Interactive Docs: http://localhost:8000/docs
