"""
Configuration settings for the scraper service.
"""
import os
from typing import Dict

# API and scraping settings
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
REQUEST_TIMEOUT = 30  # seconds
MAX_RETRIES = 3
RETRY_DELAY = 2  # seconds

# Rate limiting settings
RATE_LIMIT_CALLS = 10  # max calls
RATE_LIMIT_PERIOD = 60  # per period in seconds

# Cache settings (TTL in seconds)
CACHE_TTL_TEAM_DATA = 86400  # 24 hours - team data changes infrequently
CACHE_TTL_PLAYER_DATA = 300  # 5 minutes - player data updates frequently
CACHE_TTL_JOB_DATA = 3600  # 1 hour - job data updates regularly
CACHE_TTL_DEFAULT = 3600  # 1 hour - default cache

# Redis settings (optional - falls back to in-memory cache)
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
USE_REDIS = os.getenv("USE_REDIS", "false").lower() == "true"

# NFL Data sources
NFL_DATA_SOURCES = {
    "espn": {
        "teams": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams",
        "scoreboard": "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard",
        "player_stats": "https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/athletes/{player_id}",
    },
    "nfl": {
        "teams": "https://api.nfl.com/v3/shield/teams",
        "players": "https://api.nfl.com/v3/shield/players",
    }
}

# Default data source
DEFAULT_NFL_SOURCE = "espn"

# Job Search API settings
JSEARCH_API_KEY = os.getenv("JSEARCH_API_KEY", "")
JSEARCH_API_HOST = "jsearch.p.rapidapi.com"

# OpenAI settings for cover letter generation
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# Job filtering settings
TRUSTED_DOMAINS = ['linkedin.com', 'indeed.com', 'lever.co', 'greenhouse.io']
RED_FLAG_TERMS = [
    'quick cash', 'no experience', 'work from home', 
    'earn money fast', 'investment required'
]

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
