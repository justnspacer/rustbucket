# Job Scraper API Endpoints

This document describes the API endpoints for the integrated job scraper functionality.

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

Currently, no authentication is required. API keys for external services (JSearch, OpenAI) are configured server-side.

---

## Endpoints

### 1. Search for Jobs

Search for job postings using the JSearch API.

**Endpoint:** `POST /jobs/search`

**Request Body:**
```json
{
  "keywords": "Python developer",
  "location": "Chicago",
  "page": 1,
  "num_pages": 1,
  "country": "us",
  "date_posted": "week",
  "employment_type": "fulltime",
  "remote_jobs_only": false
}
```

**Query Parameters:**
- `apply_filters` (boolean, optional): Apply quality filters to results (default: true)

**Response:**
```json
{
  "success": true,
  "data": [
    {
      "title": "Senior Python Developer",
      "company": "Tech Corp",
      "description": "We are looking for...",
      "url": "https://...",
      "location": "Chicago, IL",
      "salary": "$120,000 - $150,000",
      "date_posted": "2025-10-01",
      "employment_type": "fulltime",
      "experience_level": "senior"
    }
  ],
  "source": "jsearch",
  "timestamp": "2025-10-11T10:30:00"
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/search?apply_filters=true" \
  -H "Content-Type: application/json" \
  -d '{
    "keywords": "Python developer",
    "location": "Chicago",
    "date_posted": "week"
  }'
```

---

### 2. Filter Jobs

Apply quality filters to job postings.

**Endpoint:** `POST /jobs/filter`

**Request Body:**
```json
{
  "jobs": [
    {
      "title": "Developer",
      "company": "Company",
      "description": "Job description...",
      "url": "https://..."
    }
  ],
  "filter_options": {
    "remove_duplicates": true,
    "check_red_flags": true,
    "trusted_only": true,
    "validate_description": true
  }
}
```

**Filter Options:**
- `remove_duplicates`: Remove duplicate postings based on content hash
- `check_red_flags`: Filter out jobs with suspicious terms (e.g., "quick cash")
- `trusted_only`: Only include jobs from trusted domains (LinkedIn, Indeed, etc.)
- `validate_description`: Filter out low-quality descriptions (< 30 words, all caps)

**Response:**
```json
{
  "success": true,
  "data": {
    "original_count": 50,
    "filtered_count": 35,
    "removed_count": 15,
    "jobs": [ /* filtered jobs */ ]
  }
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/filter" \
  -H "Content-Type: application/json" \
  -d '{
    "jobs": [/* job array */],
    "filter_options": {
      "remove_duplicates": true,
      "check_red_flags": true,
      "trusted_only": true,
      "validate_description": true
    }
  }'
```

---

### 3. Match Resume to Jobs

Match a resume to job postings using TF-IDF similarity.

**Endpoint:** `POST /jobs/match`

**Request Body:**
```json
{
  "resume_text": "Experienced Python developer with 5 years...",
  "threshold": 0.2,
  "jobs": [
    {
      "title": "Python Developer",
      "company": "Tech Corp",
      "description": "Looking for Python developer...",
      "url": "https://..."
    }
  ]
}
```

**Parameters:**
- `resume_text`: Full resume text content
- `threshold`: Minimum match score (0.0 to 1.0, default: 0.2)
- `jobs`: Array of job postings to match against

**Response:**
```json
{
  "success": true,
  "data": {
    "total_jobs": 10,
    "matches_found": 5,
    "threshold": 0.2,
    "matches": [
      {
        "job": {
          "title": "Python Developer",
          "company": "Tech Corp",
          /* other job fields */
        },
        "match_score": 0.75,
        "matched_keywords": ["python", "django", "api", "testing"]
      }
    ]
  }
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/match" \
  -H "Content-Type: application/json" \
  -d '{
    "resume_text": "Python developer with Django and Flask experience...",
    "threshold": 0.2,
    "jobs": [/* job array */]
  }'
```

---

### 4. Generate Cover Letter

Generate a tailored cover letter using OpenAI GPT-3.5.

**Endpoint:** `POST /jobs/cover-letter`

**Request Body:**
```json
{
  "job_title": "Senior Python Developer",
  "company": "Tech Corp",
  "job_description": "We are looking for an experienced Python developer...",
  "resume_summary": "5 years of Python experience with Django, REST APIs, and DevOps"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "job_title": "Senior Python Developer",
    "company": "Tech Corp",
    "content": "Dear Hiring Manager,\n\nI am writing to express my strong interest...",
    "generated_at": "2025-10-11T10:30:00"
  }
}
```

**Errors:**
- `503 Service Unavailable`: OpenAI API key not configured

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/cover-letter" \
  -H "Content-Type: application/json" \
  -d '{
    "job_title": "Python Developer",
    "company": "Tech Corp",
    "job_description": "Looking for Python developer...",
    "resume_summary": "5 years Python experience"
  }'
```

---

### 5. Full Pipeline

Run the complete job search pipeline in one request.

**Endpoint:** `POST /jobs/pipeline`

**Request Body:**
```json
{
  "search_request": {
    "keywords": "Python developer",
    "location": "Chicago",
    "page": 1,
    "num_pages": 1
  },
  "resume_text": "Experienced Python developer...",
  "resume_summary": "5 years of Python experience",
  "generate_letters": true,
  "match_threshold": 0.2
}
```

**Parameters:**
- `search_request`: Job search criteria (required)
- `resume_text`: Resume content for matching (optional)
- `resume_summary`: Brief resume summary for cover letters (optional)
- `generate_letters`: Whether to generate cover letters (default: false)
- `match_threshold`: Minimum match score (default: 0.2)

**Response:**
```json
{
  "success": true,
  "data": {
    "summary": {
      "total_jobs_found": 50,
      "jobs_after_filtering": 35,
      "resume_matches": 10,
      "cover_letters_generated": 5
    },
    "results": {
      "jobs": [/* all found jobs */],
      "filtered_jobs": [/* filtered jobs */],
      "matches": [/* resume matches */],
      "cover_letters": [/* generated letters */]
    }
  }
}
```

**Example cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/jobs/pipeline" \
  -H "Content-Type: application/json" \
  -d '{
    "search_request": {
      "keywords": "Python developer",
      "location": "Chicago"
    },
    "resume_text": "Experienced Python developer...",
    "resume_summary": "5 years Python experience",
    "generate_letters": true,
    "match_threshold": 0.25
  }'
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message describing what went wrong"
}
```

**Common HTTP Status Codes:**
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server-side error
- `503 Service Unavailable`: External service (OpenAI) not configured

---

## Examples

### Python Example

```python
import requests

# Search for jobs
response = requests.post(
    "http://localhost:8000/api/v1/jobs/search",
    json={
        "keywords": "Python developer",
        "location": "Chicago",
        "date_posted": "week"
    },
    params={"apply_filters": True}
)

jobs = response.json()["data"]
print(f"Found {len(jobs)} jobs")

# Match resume to jobs
match_response = requests.post(
    "http://localhost:8000/api/v1/jobs/match",
    json={
        "resume_text": "Python developer with 5 years experience...",
        "threshold": 0.2,
        "jobs": jobs
    }
)

matches = match_response.json()["data"]["matches"]
print(f"Found {len(matches)} matching jobs")

# Generate cover letter for top match
if matches:
    top_match = matches[0]
    letter_response = requests.post(
        "http://localhost:8000/api/v1/jobs/cover-letter",
        json={
            "job_title": top_match["job"]["title"],
            "company": top_match["job"]["company"],
            "job_description": top_match["job"]["description"],
            "resume_summary": "5 years Python experience with Django"
        }
    )
    
    cover_letter = letter_response.json()["data"]["content"]
    print(f"Generated cover letter:\n{cover_letter}")
```

### JavaScript Example

```javascript
// Search for jobs
const searchResponse = await fetch('http://localhost:8000/api/v1/jobs/search?apply_filters=true', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    keywords: 'Python developer',
    location: 'Chicago',
    date_posted: 'week'
  })
});

const jobs = (await searchResponse.json()).data;
console.log(`Found ${jobs.length} jobs`);

// Run full pipeline
const pipelineResponse = await fetch('http://localhost:8000/api/v1/jobs/pipeline', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    search_request: {
      keywords: 'Python developer',
      location: 'Chicago'
    },
    resume_text: 'Experienced Python developer...',
    resume_summary: '5 years Python experience',
    generate_letters: true,
    match_threshold: 0.25
  })
});

const results = (await pipelineResponse.json()).data;
console.log('Pipeline results:', results.summary);
```

---

## Rate Limiting

The API implements rate limiting:
- **Job Search**: 10 calls per 60 seconds (configurable)
- Results are cached for 1 hour to reduce API calls

---

## Configuration

Required environment variables:

```bash
# Required for job searching
JSEARCH_API_KEY=your_jsearch_api_key

# Optional for cover letter generation
OPENAI_API_KEY=your_openai_api_key

# Optional for caching
USE_REDIS=false
REDIS_HOST=localhost
REDIS_PORT=6379
```

---

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

These interfaces allow you to test endpoints directly in your browser.

---

## Testing

Test the API with the provided examples:

```bash
# Start the API server
python run.py

# In another terminal, test the endpoints
curl http://localhost:8000/api/v1/jobs/search -X POST \
  -H "Content-Type: application/json" \
  -d '{"keywords": "developer", "location": "chicago"}'
```

---

## Support

For issues or questions:
- Check the main documentation: `JOBS_INTEGRATION_README.md`
- Review code examples: `integrated_jobs_example.py`
- See architecture docs: `ARCHITECTURE.md`
