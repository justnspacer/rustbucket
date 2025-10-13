# Quick Start Guide - Job Scraper Integration

Get started with the integrated job scraper in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Set Up API Keys

Create a `.env` file in the project root:

```bash
# Required for job searching
JSEARCH_API_KEY=your_jsearch_api_key_here

# Optional - for cover letter generation
OPENAI_API_KEY=your_openai_api_key_here
```

**Get API Keys:**
- JSearch API: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
- OpenAI API: https://platform.openai.com/api-keys

## 3. Add Your Resume (Optional)

Place your resume in the `resumes/` folder:
- `resumes/resume.pdf` (preferred), or
- `resumes/resume.docx`

## 4. Run Your First Job Search

Create a file `quick_test.py`:

```python
from scraper_please.scraper_manager import ScraperManager, ScraperType
from scraper_please.models import JobSearchQuery

# Initialize
manager = ScraperManager()
scraper = manager.get_scraper(ScraperType.JOBS)

# Search for jobs
query = JobSearchQuery(
    keywords="Python developer",
    location="Chicago"
)

jobs = scraper.search_jobs(query)
filtered = scraper.filter_jobs(jobs)

# Display results
for job in filtered[:5]:
    print(f"✅ {job.title} at {job.company}")
    print(f"   {job.location} - {job.url}")
    print()
```

Run it:
```bash
python quick_test.py
```

## 5. Match Your Resume (If Added)

```python
# Add to your script after filtering
resume = scraper.extract_resume("resumes/resume.pdf")
matches = scraper.match_resume_to_jobs(resume, filtered)

print(f"Found {len(matches)} matching jobs!")

for match in matches[:5]:
    print(f"🎯 {match.job.title} - Match: {match.match_score:.0%}")
```

## 6. See More Examples

Run the complete example suite:

```bash
python integrated_jobs_example.py
```

## Common Issues

### "No module named 'scraper_please'"

Make sure you're running from the project root directory.

### "JSEARCH_API_KEY not found"

Check your `.env` file exists and has the correct key.

### "No jobs found"

- Verify your API key is valid
- Try a different search query
- Check your internet connection

### "Resume file not found"

Make sure your resume is in the `resumes/` folder with correct name.

## What's Next?

- 📖 Read full docs: `JOBS_INTEGRATION_README.md`
- 💡 See all examples: `integrated_jobs_example.py`
- 🧪 Run tests: `pytest test_jobs_integration.py`
- 🔄 Migrate old code: `MIGRATION_GUIDE.py`

## Need Help?

Check these resources:
1. `JOBS_INTEGRATION_README.md` - Complete documentation
2. `INTEGRATION_SUMMARY.md` - Technical overview
3. `integrated_jobs_example.py` - Working examples

---

**You're ready to go!** 🚀
