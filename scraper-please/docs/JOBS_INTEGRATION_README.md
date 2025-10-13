# Jobs Scraper Integration

This document describes the integrated job scraping functionality that combines job searching, filtering, resume matching, and cover letter generation into a unified pipeline.

## Overview

The integrated `JobsScraper` class provides a complete solution for:

1. **Job Searching** - Search for jobs using the JSearch API
2. **Quality Filtering** - Filter out low-quality, suspicious, or duplicate postings
3. **Resume Matching** - Match your resume to job descriptions using TF-IDF similarity
4. **Cover Letter Generation** - Generate tailored cover letters using OpenAI

## Architecture

### Core Components

```
scraper_please/
├── models/
│   └── jobs_models.py          # Data models (JobPosting, Resume, JobMatch, etc.)
├── scrapers/
│   ├── base_scraper.py         # Base scraper with caching and rate limiting
│   └── jobs_scraper.py         # Integrated jobs scraper
├── config.py                   # Configuration settings
└── scraper_manager.py          # Scraper lifecycle management
```

### Data Models

- **`JobPosting`** - Represents a job listing with title, company, description, etc.
- **`JobSearchQuery`** - Search parameters (keywords, location, filters)
- **`Resume`** - Extracted resume text with metadata
- **`JobMatch`** - Job posting with similarity score and matched keywords
- **`CoverLetter`** - Generated cover letter for a job posting

## Setup

### 1. Environment Variables

Create a `.env` file with your API keys:

```bash
# Required for job searching
JSEARCH_API_KEY=your_jsearch_api_key_here

# Optional - for cover letter generation
OPENAI_API_KEY=your_openai_api_key_here

# Optional - for Redis caching (defaults to in-memory)
USE_REDIS=false
REDIS_HOST=localhost
REDIS_PORT=6379
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare Resume

Place your resume in the `resumes/` directory:
- `resumes/resume.pdf` (preferred)
- `resumes/resume.docx` (alternative)

## Usage

### Quick Start

```python
from scraper_please.scraper_manager import ScraperManager, ScraperType
from scraper_please.models import JobSearchQuery

# Initialize manager
manager = ScraperManager(cache_enabled=True, rate_limit_enabled=True)

# Get jobs scraper
scraper = manager.get_scraper(ScraperType.JOBS)

# Create search query
query = JobSearchQuery(
    keywords="Python developer",
    location="Chicago",
    date_posted="week"
)

# Search and filter jobs
jobs = scraper.search_jobs(query)
filtered_jobs = scraper.filter_jobs(jobs)

print(f"Found {len(filtered_jobs)} quality job postings")
```

### Resume Matching

```python
# Extract resume
resume = scraper.extract_resume("resumes/resume.pdf")

# Match resume to jobs
matches = scraper.match_resume_to_jobs(resume, filtered_jobs, threshold=0.2)

# Display top matches
for match in matches[:5]:
    print(f"{match.job.title} at {match.job.company}")
    print(f"Match Score: {match.match_score:.2%}")
```

### Cover Letter Generation

```python
# Generate cover letter for a job
resume_summary = "5 years of Python experience, REST APIs, and DevOps tooling"

cover_letter = scraper.generate_cover_letter(
    job=matches[0].job,
    resume_summary=resume_summary
)

print(cover_letter.content)
```

### Full Pipeline

```python
# Run complete pipeline in one call
results = scraper.run_full_pipeline(
    query=query,
    resume_path="resumes/resume.pdf",
    generate_letters=True,
    resume_summary="5 years of Python experience..."
)

print(f"Jobs found: {len(results['jobs'])}")
print(f"Filtered: {len(results['filtered_jobs'])}")
print(f"Matches: {len(results['matches'])}")
print(f"Cover letters: {len(results['cover_letters'])}")
```

## Features

### 1. Job Searching

Search for jobs with flexible parameters:

```python
query = JobSearchQuery(
    keywords="Python developer",
    location="Chicago",
    page=1,
    num_pages=1,
    country="us",
    date_posted="week",        # all, today, 3days, week, month
    employment_type="fulltime", # fulltime, parttime, contractor, intern
    remote_jobs_only=True
)
```

### 2. Quality Filtering

Automatic filtering removes:

- **Duplicates** - Based on content hash
- **Red Flags** - Suspicious terms like "quick cash", "investment required"
- **Untrusted Sources** - Only allows known job boards (LinkedIn, Indeed, etc.)
- **Low Quality** - Filters short descriptions or all-caps text

Custom filtering options:

```python
filtered = scraper.filter_jobs(
    jobs,
    remove_duplicates=True,
    check_red_flags=True,
    trusted_only=True,
    validate_description=True
)
```

### 3. Resume Matching

Uses TF-IDF vectorization and cosine similarity:

```python
# Match with custom threshold
matches = scraper.match_resume_to_jobs(
    resume=resume,
    jobs=filtered_jobs,
    threshold=0.25  # 0-1 scale, higher = stricter
)

# Results include:
# - match_score: Similarity score (0-1)
# - matched_keywords: Common important terms
```

### 4. Cover Letter Generation

Generate tailored cover letters using GPT-3.5:

```python
cover_letter = scraper.generate_cover_letter(
    job=job_posting,
    resume_summary="Brief summary of your experience"
)

# Save to file
with open(f"cover_letter_{job.company}.txt", "w") as f:
    f.write(cover_letter.content)
```

## Configuration

### Config Settings (`scraper_please/config.py`)

```python
# Cache TTL
CACHE_TTL_JOB_DATA = 3600  # 1 hour

# Rate limiting
RATE_LIMIT_CALLS = 10  # Max calls per period
RATE_LIMIT_PERIOD = 60  # Period in seconds

# Trusted job domains
TRUSTED_DOMAINS = [
    'linkedin.com',
    'indeed.com',
    'lever.co',
    'greenhouse.io'
]

# Red flag terms to filter
RED_FLAG_TERMS = [
    'quick cash',
    'no experience',
    'work from home',
    'earn money fast',
    'investment required'
]
```

### Customization

You can customize filtering by modifying these in `config.py`:

```python
# Add more trusted domains
TRUSTED_DOMAINS.append('mycompany.com')

# Add more red flag terms
RED_FLAG_TERMS.extend(['mlm', 'pyramid scheme'])
```

## Examples

Run the integrated examples:

```bash
python integrated_jobs_example.py
```

This demonstrates:
1. Basic job search
2. Resume matching
3. Full pipeline with cover letters
4. Custom filtering options

## API Reference

### JobsScraper Methods

#### `search_jobs(query: JobSearchQuery) -> List[JobPosting]`
Search for jobs using the JSearch API.

#### `filter_jobs(jobs: List[JobPosting], **options) -> List[JobPosting]`
Filter jobs based on quality criteria.

#### `extract_resume(file_path: str) -> Resume`
Extract text from PDF or DOCX resume file.

#### `match_resume_to_jobs(resume: Resume, jobs: List[JobPosting], threshold: float) -> List[JobMatch]`
Match resume to job postings using TF-IDF similarity.

#### `generate_cover_letter(job: JobPosting, resume_summary: str) -> CoverLetter`
Generate cover letter using OpenAI API.

#### `run_full_pipeline(query: JobSearchQuery, **options) -> Dict[str, Any]`
Run complete pipeline: search, filter, match, generate letters.

## Migration from Legacy Code

### Old Code Structure
```
filtering.py          # Filtering logic
resume.py            # Resume extraction and matching
coverletter.py       # Cover letter generation
jobs.py              # API calls
main.py              # Orchestration
```

### New Integrated Structure
All functionality is now in:
```
scraper_please/
├── models/jobs_models.py      # Data models
└── scrapers/jobs_scraper.py   # All logic in one place
```

### Migration Example

**Before:**
```python
from filtering import run_filters
from resume import extract_text_from_pdf, match_resume_to_jobs
from coverletter import generate_cover_letter

jobs = response['data']
filtered = run_filters(jobs)
resume_text = extract_text_from_pdf("resume.pdf")
matches = match_resume_to_jobs(resume_text, filtered)
```

**After:**
```python
from scraper_please.scraper_manager import ScraperManager, ScraperType
from scraper_please.models import JobSearchQuery

manager = ScraperManager()
scraper = manager.get_scraper(ScraperType.JOBS)

query = JobSearchQuery(keywords="developer", location="chicago")
results = scraper.run_full_pipeline(
    query=query,
    resume_path="resumes/resume.pdf"
)
```

## Benefits of Integration

1. **Unified API** - Single interface for all job scraping operations
2. **Built-in Caching** - Automatic caching with Redis or in-memory
3. **Rate Limiting** - Prevents API throttling
4. **Error Handling** - Consistent error handling and logging
5. **Type Safety** - Proper data models with type hints
6. **Extensibility** - Easy to add new features or data sources
7. **Testing** - Easier to test with dependency injection

## Troubleshooting

### No jobs found
- Check API key is valid
- Verify search query parameters
- Check rate limits

### Low match scores
- Lower the threshold (try 0.15-0.2)
- Improve resume formatting
- Ensure resume has relevant keywords

### Cover letter generation fails
- Verify OpenAI API key
- Check API credits/quota
- Ensure job description is not empty

### Import errors
- Run `pip install -r requirements.txt`
- Check Python version (3.8+)

## Future Enhancements

- [ ] Support for more job boards (ZipRecruiter, Glassdoor)
- [ ] Advanced resume parsing (extract skills, experience)
- [ ] Multi-language support
- [ ] Job application tracking
- [ ] Email notification for new matches
- [ ] Web UI with Streamlit
- [ ] Async job searching for better performance
- [ ] Machine learning for better matching

## License

See main project LICENSE file.
