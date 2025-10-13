# Job Scraper Integration Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Application                            │
│  (integrated_jobs_example.py, quick_test.py, or your custom code)  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        ScraperManager                               │
│  • Lifecycle management                                             │
│  • Scraper instance caching                                         │
│  • Source switching                                                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         JobsScraper                                 │
│  ┌───────────────────────────────────────────────────────────────┐ │
│  │                  Inherits from BaseScraper                    │ │
│  │  • Caching (Redis/In-Memory)                                  │ │
│  │  • Rate Limiting (Fixed/Adaptive)                             │ │
│  │  • Error Handling & Retry Logic                               │ │
│  │  • HTTP Session Management                                    │ │
│  └───────────────────────────────────────────────────────────────┘ │
│                                                                      │
│  Core Methods:                                                       │
│  ┌─────────────────────┐  ┌─────────────────────┐                 │
│  │  search_jobs()      │  │  filter_jobs()      │                 │
│  │  • API integration  │  │  • Duplicates       │                 │
│  │  • Query params     │  │  • Red flags        │                 │
│  │  • Response parsing │  │  • Trust validation │                 │
│  └─────────────────────┘  └─────────────────────┘                 │
│                                                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐                 │
│  │  extract_resume()   │  │  match_resume_to    │                 │
│  │  • PDF extraction   │  │  _jobs()            │                 │
│  │  • DOCX extraction  │  │  • TF-IDF           │                 │
│  │  • Text cleaning    │  │  • Cosine similarity│                 │
│  └─────────────────────┘  └─────────────────────┘                 │
│                                                                      │
│  ┌─────────────────────┐  ┌─────────────────────┐                 │
│  │  generate_cover     │  │  run_full_pipeline()│                 │
│  │  _letter()          │  │  • Complete workflow│                 │
│  │  • OpenAI API       │  │  • All-in-one       │                 │
│  │  • GPT-3.5 Turbo    │  │  • Error recovery   │                 │
│  └─────────────────────┘  └─────────────────────┘                 │
└──────────────┬────────────────────────────┬──────────────────────────┘
               │                            │
               ▼                            ▼
┌──────────────────────────┐  ┌────────────────────────────────────┐
│    Data Models           │  │    External Services               │
│                          │  │                                    │
│  • JobPosting            │  │  • JSearch API (RapidAPI)          │
│  • JobSearchQuery        │  │  • OpenAI API                      │
│  • Resume                │  │  • Redis (Optional)                │
│  • JobMatch              │  │                                    │
│  • CoverLetter           │  │                                    │
└──────────────────────────┘  └────────────────────────────────────┘
```

## Data Flow - Full Pipeline

```
1. User Input
   ↓
   JobSearchQuery(keywords="Python", location="Chicago")
   ↓
2. Job Search
   ↓
   [API Request] → JSearch API → [Raw JSON Response]
   ↓
3. Parse Response
   ↓
   [JobPosting, JobPosting, JobPosting, ...]
   ↓
4. Filter Jobs
   ↓
   • Check duplicates (MD5 hash)
   • Scan red flags (terms)
   • Validate domain (trusted list)
   • Check description (length, quality)
   ↓
   [Filtered JobPosting List]
   ↓
5. Extract Resume (if provided)
   ↓
   resume.pdf → [pdfplumber] → Raw Text → Clean Text → Resume Object
   ↓
6. Match Resume to Jobs
   ↓
   For each job:
     • Vectorize resume text (TF-IDF)
     • Vectorize job description (TF-IDF)
     • Calculate cosine similarity
     • Extract keywords
   ↓
   [JobMatch, JobMatch, ...] (sorted by score)
   ↓
7. Generate Cover Letters (optional)
   ↓
   For top matches:
     • Build prompt (job + resume summary)
     • Call OpenAI API
     • Get generated letter
   ↓
   [CoverLetter, CoverLetter, ...]
   ↓
8. Return Results
   {
     'jobs': [...],
     'filtered_jobs': [...],
     'matches': [...],
     'cover_letters': [...]
   }
```

## Component Interactions

```
┌──────────────┐
│    Cache     │◄──────┐
│  (Redis/Mem) │       │
└──────────────┘       │
                       │
┌──────────────┐       │
│ Rate Limiter │◄──────┤
└──────────────┘       │
                       │
┌──────────────┐       │      ┌──────────────┐
│ HTTP Session │◄──────┼──────┤ JobsScraper  │
└──────────────┘       │      └──────┬───────┘
                       │             │
┌──────────────┐       │             │
│   Logger     │◄──────┘             │
└──────────────┘                     │
                                     │
                  ┌──────────────────┼──────────────────┐
                  │                  │                  │
                  ▼                  ▼                  ▼
         ┌────────────────┐  ┌──────────┐  ┌──────────────────┐
         │ External APIs  │  │  Models  │  │  Utilities       │
         │  • JSearch     │  │          │  │  • Text cleaning │
         │  • OpenAI      │  │          │  │  • Hashing       │
         └────────────────┘  └──────────┘  │  • Vectorization │
                                            └──────────────────┘
```

## File Organization

```
scraper-please/
│
├── scraper_please/                    [Package]
│   ├── __init__.py
│   ├── config.py                      [Configuration]
│   ├── scraper_manager.py             [Manager]
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── jobs_models.py             [Data Models]
│   │   └── foolsball_models.py
│   │
│   ├── scrapers/
│   │   ├── __init__.py
│   │   ├── base_scraper.py            [Base Class]
│   │   ├── jobs_scraper.py            [Jobs Implementation] ★
│   │   └── foolsball_scraper.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── cache.py                   [Caching]
│       └── rate_limiter.py            [Rate Limiting]
│
├── integrated_jobs_example.py         [Examples] ★
├── test_jobs_integration.py           [Tests] ★
│
├── JOBS_INTEGRATION_README.md         [Main Docs] ★
├── INTEGRATION_SUMMARY.md             [Summary] ★
├── QUICKSTART.md                      [Quick Guide] ★
├── MIGRATION_GUIDE.py                 [Migration] ★
│
├── requirements.txt
├── .env                               [API Keys]
│
└── resumes/                           [Resume Storage]
    ├── resume.pdf
    └── resume.docx

★ = New/Modified for integration
```

## Class Hierarchy

```
BaseScraper (Abstract)
│
├── Properties:
│   • cache: Cache
│   • rate_limiter: RateLimiter
│   • session: requests.Session
│
├── Methods:
│   • _create_session()
│   • _make_request()
│   • _handle_rate_limit()
│
└── Child Classes:
    │
    ├── FoolsballScraper
    │   • get_teams()
    │   • get_scores()
    │
    └── JobsScraper ★
        • search_jobs()
        • filter_jobs()
        • extract_resume()
        • match_resume_to_jobs()
        • generate_cover_letter()
        • run_full_pipeline()
```

## Filtering Pipeline Detail

```
Input: List[JobPosting]
   │
   ├─► Step 1: Duplicate Check
   │    • Generate MD5 hash (title + description)
   │    • Track seen hashes
   │    • Skip if duplicate
   │    │
   │    ▼
   ├─► Step 2: Red Flag Check
   │    • Scan for suspicious terms
   │    • Terms: 'quick cash', 'no experience', etc.
   │    • Reject if found
   │    │
   │    ▼
   ├─► Step 3: Domain Trust Check
   │    • Extract domain from URL
   │    • Check against TRUSTED_DOMAINS
   │    • Only allow: linkedin, indeed, lever, greenhouse
   │    │
   │    ▼
   └─► Step 4: Description Validation
        • Check word count (min 30 words)
        • Reject all-caps descriptions
        • Ensure quality content
        │
        ▼
Output: List[JobPosting] (filtered)
```

## Resume Matching Algorithm

```
Input: Resume Text + Job Description
   │
   ├─► Step 1: Vectorization
   │    • Use TF-IDF Vectorizer
   │    • Create vocabulary from both texts
   │    • Transform into vectors
   │    │
   │    ▼
   ├─► Step 2: Similarity Calculation
   │    • Compute cosine similarity
   │    • Score range: 0.0 to 1.0
   │    • Higher = better match
   │    │
   │    ▼
   ├─► Step 3: Threshold Filtering
   │    • Default threshold: 0.2
   │    • Only keep matches above threshold
   │    │
   │    ▼
   ├─► Step 4: Keyword Extraction
   │    • Extract top TF-IDF terms
   │    • Common important words
   │    │
   │    ▼
   └─► Step 5: Ranking
        • Sort by match score (descending)
        • Return top matches
        │
        ▼
Output: List[JobMatch] (sorted)
```

## Configuration Flow

```
Environment Variables (.env)
   │
   ├─► JSEARCH_API_KEY
   ├─► OPENAI_API_KEY
   ├─► USE_REDIS
   ├─► REDIS_HOST
   └─► REDIS_PORT
        │
        ▼
Config Module (config.py)
   │
   ├─► API Keys
   ├─► Cache TTL
   ├─► Rate Limits
   ├─► Trusted Domains
   └─► Red Flag Terms
        │
        ▼
JobsScraper Initialization
   │
   └─► Ready for use
```

## Error Handling Flow

```
User Request
   │
   ▼
Try:
   │
   ├─► Rate Limiter Check
   │    └─► [Wait if needed]
   │
   ├─► Make API Request
   │    │
   │    ├─► Success → Parse Response
   │    │
   │    └─► Error → Retry Logic
   │         ├─► Retry 1
   │         ├─► Retry 2
   │         ├─► Retry 3
   │         └─► Raise ScraperException
   │
   └─► Return Result
        │
        ▼
Except ScraperException:
   │
   ├─► Log Error
   ├─► Return Empty/Partial Result
   └─► User gets error message
```

---

This architecture provides:
- ✅ Separation of concerns
- ✅ Reusability through inheritance
- ✅ Type safety with models
- ✅ Testability through dependency injection
- ✅ Scalability with caching and rate limiting
- ✅ Maintainability with clear structure
