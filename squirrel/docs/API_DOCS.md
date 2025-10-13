# API Documentation

## Overview

The Squirrel API provides REST endpoints for search NFL data with intelligent caching and rate limiting.

**Base URL**: `http://localhost:8000/api/v1`

## Quick Start

Start the server:
```bash
python run.py
```

Access the interactive documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

Currently, the API does not require authentication. For production use, implement appropriate authentication mechanisms.

## Endpoints

### Teams

#### Get All Teams
```http
GET /api/v1/teams
```

**Query Parameters:**
- `source` (optional): Data source to use (`espn` or `nfl`)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "1",
      "name": "Falcons",
      "abbreviation": "ATL",
      "display_name": "Atlanta Falcons",
      "location": "Atlanta",
      "color": "A71930",
      "logo_url": "https://...",
      "conference": "NFC",
      "division": "South"
    }
  ],
  "source": "espn",
  "cached": false,
  "timestamp": "2025-10-10T12:00:00"
}
```

**Cache TTL:** 24 hours

#### Get Specific Team
```http
GET /api/v1/teams/{team_id}
```

**Path Parameters:**
- `team_id`: Team ID

**Query Parameters:**
- `source` (optional): Data source to use

---

### Players

#### Get All Players
```http
GET /api/v1/players
```

**Query Parameters:**
- `team_id` (optional): Filter by team ID
- `source` (optional): Data source to use

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "id": "12345",
      "name": "John Doe",
      "display_name": "John Doe",
      "team_id": "1",
      "position": "QB",
      "jersey_number": "12",
      "height": "6-2",
      "weight": 225
    }
  ],
  "source": "espn",
  "cached": false,
  "timestamp": "2025-10-10T12:00:00"
}
```

**Cache TTL:** 5 minutes

#### Get Specific Player
```http
GET /api/v1/players/{player_id}
```

**Path Parameters:**
- `player_id`: Player ID

**Query Parameters:**
- `source` (optional): Data source to use

#### Get Player Statistics
```http
GET /api/v1/players/{player_id}/stats
```

**Path Parameters:**
- `player_id`: Player ID

**Query Parameters:**
- `season` (optional): Season year (defaults to current year)
- `source` (optional): Data source to use

**Response:**
```json
{
  "success": true,
  "data": {
    "player_id": "12345",
    "player_name": "John Doe",
    "season": 2024,
    "stats": {
      "passing_yards": 4500,
      "touchdowns": 35,
      "interceptions": 10
    }
  },
  "source": "espn",
  "timestamp": "2025-10-10T12:00:00"
}
```

**Cache TTL:** 5 minutes

---

### Scores

#### Get Live Scores
```http
GET /api/v1/scores
```

**Query Parameters:**
- `source` (optional): Data source to use

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "game_id": "401234567",
      "home_team": "ATL",
      "away_team": "NO",
      "home_score": 24,
      "away_score": 21,
      "quarter": "4",
      "time_remaining": "2:45",
      "status": "in-progress"
    }
  ],
  "source": "espn",
  "cached": false,
  "timestamp": "2025-10-10T12:00:00"
}
```

**Cache TTL:** No caching (always fresh data)

---

### Data Sources

#### Get Available Sources
```http
GET /api/v1/sources
```

**Response:**
```json
[
  {
    "squirrel_type": "foolsball",
    "active_source": "espn",
    "available_sources": ["espn", "nfl"]
  }
]
```

#### Switch Data Source
```http
POST /api/v1/sources/switch
```

**Request Body:**
```json
{
  "squirrel_type": "foolsball",
  "source": "nfl"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "squirrel_type": "foolsball",
    "new_source": "nfl",
    "message": "Switched foolsball source to nfl"
  },
  "timestamp": "2025-10-10T12:00:00"
}
```

---

### Cache Management

#### Invalidate Cache
```http
POST /api/v1/cache/invalidate
```

**Request Body:**
```json
{
  "squirrel_type": "foolsball",
  "source": "espn",
  "cache_key": "foolsball:teams:espn"
}
```

All fields are optional:
- No fields: Invalidates all cache
- `squirrel_type` only: Invalidates all cache for that squirrel type
- `squirrel_type` + `source`: Invalidates cache for specific source
- `cache_key`: Invalidates specific cache key

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "Cache invalidated for foolsball:espn"
  },
  "timestamp": "2025-10-10T12:00:00"
}
```

#### Clear All Cache
```http
DELETE /api/v1/cache
```

**Response:**
```json
{
  "success": true,
  "data": {
    "message": "All cache cleared"
  },
  "timestamp": "2025-10-10T12:00:00"
}
```

---

### System

#### Get Squirrel Statistics
```http
GET /api/v1/stats
```

**Response:**
```json
{
  "active_squirrels": 1,
  "active_sources": {
    "foolsball": "espn"
  },
  "squirrels": {
    "foolsball:espn": {
      "type": "foolsball",
      "source": "espn",
      "cache_enabled": true,
      "rate_limit_enabled": true,
      "rate_limiter": {
        "current_calls": 5,
        "max_calls": 10,
        "period": 60,
        "calls_remaining": 5,
        "percentage_used": 50.0
      }
    }
  }
}
```

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-10T12:00:00",
  "version": "0.1.0",
  "squirrel_stats": { /* ... */ }
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error type",
  "detail": "Detailed error message",
  "timestamp": "2025-10-10T12:00:00"
}
```

### HTTP Status Codes

- `200 OK`: Success
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

---

## Rate Limiting

The API implements rate limiting per squirrel:
- Default: 10 calls per 60 seconds
- Adaptive rate limiting backs off on errors
- Rate limit stats available via `/api/v1/stats`

---

## Caching Strategy

Different cache TTL for different data types:

| Data Type | Cache TTL | Reason |
|-----------|-----------|--------|
| Teams | 24 hours | Infrequent changes |
| Players | 5 minutes | Frequent updates |
| Stats | 5 minutes | Frequent updates |
| Scores | No cache | Real-time data |

---

## Examples

### Python with requests

```python
import requests

# Get teams
response = requests.get("http://localhost:8000/api/v1/teams")
teams = response.json()

# Get players for a team
response = requests.get(
    "http://localhost:8000/api/v1/players",
    params={"team_id": "1"}
)
players = response.json()

# Switch source
response = requests.post(
    "http://localhost:8000/api/v1/sources/switch",
    json={"squirrel_type": "foolsball", "source": "nfl"}
)
```

### cURL

```bash
# Get teams
curl http://localhost:8000/api/v1/teams

# Get players
curl "http://localhost:8000/api/v1/players?team_id=1"

# Switch source
curl -X POST http://localhost:8000/api/v1/sources/switch \
  -H "Content-Type: application/json" \
  -d '{"squirrel_type": "foolsball", "source": "nfl"}'

# Invalidate cache
curl -X POST http://localhost:8000/api/v1/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{"squirrel_type": "foolsball"}'
```

---

## Configuration

The API behavior can be configured via `squirrel/config.py`:

```python
# Cache TTL (seconds)
CACHE_TTL_TEAM_DATA = 86400  # 24 hours
CACHE_TTL_PLAYER_DATA = 300  # 5 minutes

# Rate limiting
RATE_LIMIT_CALLS = 10
RATE_LIMIT_PERIOD = 60

# Redis (optional)
USE_REDIS = False
REDIS_HOST = "localhost"
REDIS_PORT = 6379
```
