# Job Scraper API - Quick Reference

## 🚀 Start Server
```bash
python run.py
```
**URL**: http://localhost:8000

---

## 📋 Endpoints

### 1️⃣ Search Jobs
```http
POST /api/v1/jobs/search
```
```json
{"keywords": "Python developer", "location": "Chicago"}
```

### 2️⃣ Filter Jobs
```http
POST /api/v1/jobs/filter
```
```json
{
  "jobs": [/* job array */],
  "filter_options": {"remove_duplicates": true}
}
```

### 3️⃣ Match Resume
```http
POST /api/v1/jobs/match
```
```json
{
  "resume_text": "...",
  "threshold": 0.2,
  "jobs": [/* job array */]
}
```

### 4️⃣ Generate Cover Letter
```http
POST /api/v1/jobs/cover-letter
```
```json
{
  "job_title": "Developer",
  "company": "Tech Corp",
  "job_description": "...",
  "resume_summary": "..."
}
```

### 5️⃣ Full Pipeline
```http
POST /api/v1/jobs/pipeline
```
```json
{
  "search_request": {"keywords": "developer"},
  "resume_text": "...",
  "generate_letters": true
}
```

---

## 🔑 Environment Variables
```bash
JSEARCH_API_KEY=your_key     # Required
OPENAI_API_KEY=your_key      # Optional (for cover letters)
```

---

## 📖 Documentation
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Full Docs**: `JOB_API_DOCS.md`

---

## 🧪 Test
```bash
python test_job_api.py
```

---

## 💡 Quick cURL Examples

**Search:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs/search \
  -H "Content-Type: application/json" \
  -d '{"keywords":"developer","location":"chicago"}'
```

**Pipeline:**
```bash
curl -X POST http://localhost:8000/api/v1/jobs/pipeline \
  -H "Content-Type: application/json" \
  -d '{
    "search_request": {"keywords": "Python developer"},
    "resume_text": "5 years Python experience",
    "match_threshold": 0.2
  }'
```

---

## 🐍 Python Client
```python
import requests

# Search
r = requests.post(
    "http://localhost:8000/api/v1/jobs/search",
    json={"keywords": "developer", "location": "chicago"}
)
jobs = r.json()["data"]

# Match
r = requests.post(
    "http://localhost:8000/api/v1/jobs/match",
    json={
        "resume_text": "Python developer...",
        "threshold": 0.2,
        "jobs": jobs
    }
)
matches = r.json()["data"]["matches"]
```

---

## ⚡ Response Format
```json
{
  "success": true,
  "data": { /* results */ },
  "timestamp": "2025-10-11T10:30:00",
  "source": "jsearch"
}
```

---

## ⚠️ Common Errors
- `503` - OpenAI key not configured
- `500` - JSearch API error or invalid key
- `400` - Invalid request parameters

---

## 🎯 Features
- ✅ Job search (JSearch API)
- ✅ Quality filtering
- ✅ Resume matching (TF-IDF)
- ✅ Cover letter generation (GPT-3.5)
- ✅ Full pipeline
- ✅ Caching (1 hour)
- ✅ Rate limiting (10/min)

---

## 📚 More Info
- Integration: `API_INTEGRATION_SUMMARY.md`
- Full docs: `JOB_API_DOCS.md`
- Architecture: `ARCHITECTURE.md`
- Examples: `test_job_api.py`
