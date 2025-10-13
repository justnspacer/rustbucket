"""
Job squirrel with integrated filtering, matching, and cover letter generation.
"""
import os
import logging
import hashlib
import re
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

import requests
import docx
import pdfplumber
import wordninja
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from .base_squirrel import BaseSquirrel, SquirrelException
from ..models.jobs_models import (
    JobPosting, JobSearchQuery, Resume, JobMatch, CoverLetter
)
from ..config import (
    CACHE_TTL_JOB_DATA, JSEARCH_API_KEY, JSEARCH_API_HOST,
    OPENAI_API_KEY, TRUSTED_DOMAINS, RED_FLAG_TERMS
)

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class JobsSquirrel(BaseSquirrel):
    """
    Squirrel for job postings with filtering, matching, and cover letter generation.
    Integrates with JSearch API for job listings.
    """
    
    def __init__(
        self,
        cache_enabled: bool = True,
        rate_limit_enabled: bool = True,
        api_key: Optional[str] = None
    ):
        """
        Initialize jobs squirrel.
        
        Args:
            cache_enabled: Enable caching
            rate_limit_enabled: Enable rate limiting
            api_key: JSearch API key (falls back to env/config)
        """
        super().__init__(
            cache_enabled=cache_enabled,
            rate_limit_enabled=rate_limit_enabled
        )
        
        self.api_key = api_key or JSEARCH_API_KEY or os.getenv("JSEARCH_API_KEY")
        if not self.api_key:
            logger.warning("No JSearch API key provided. Some features may not work.")
        
        self.openai_api_key = OPENAI_API_KEY or os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            logger.warning("No OpenAI API key provided. Cover letter generation disabled.")
        
        logger.info("JobsSquirrel initialized")
    
    def search_jobs(self, query: JobSearchQuery) -> List[JobPosting]:
        """
        Search for jobs using JSearch API.
        
        Args:
            query: Job search query parameters
        
        Returns:
            List of job postings
        
        Raises:
            SquirrelException: If search fails
        """
        cache_key = f"job_search:{query.keywords}:{query.location}:{query.page}"
        
        # Check cache first
        if self.cache_enabled:
            cached = self.cache.get(cache_key)
            if cached:
                logger.info(f"Cache hit for job search: {cache_key}")
                return [JobPosting.from_dict(job) for job in cached]
        
        # Rate limiting
        if self.rate_limit_enabled:
            self.rate_limiter.wait_if_needed()
        
        # Make API request
        url = f"https://{JSEARCH_API_HOST}/search"
        headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": JSEARCH_API_HOST
        }
        params = query.to_params()
        
        try:
            logger.info(f"Searching jobs: {params['query']}")
            response = self.session.get(url, headers=headers, params=params)
            response.raise_for_status()
            
            data = response.json()
            jobs = self._parse_job_response(data)
            
            # Cache results
            if self.cache_enabled:
                self.cache.set(
                    cache_key,
                    [job.to_dict() for job in jobs],
                    ttl=CACHE_TTL_JOB_DATA
                )
            
            logger.info(f"Found {len(jobs)} job postings")
            return jobs
            
        except requests.RequestException as e:
            logger.error(f"Job search failed: {e}")
            raise SquirrelException(f"Job search failed: {e}")
    
    def _parse_job_response(self, data: dict) -> List[JobPosting]:
        """Parse API response into JobPosting objects."""
        jobs = []
        
        if 'data' not in data:
            return jobs
        
        for item in data['data']:
            try:
                job = JobPosting(
                    title=item.get('job_title', ''),
                    company=item.get('employer_name', ''),
                    description=item.get('job_description', ''),
                    url=item.get('job_apply_link', ''),
                    location=item.get('job_city', ''),
                    salary=self._format_salary(item),
                    date_posted=item.get('job_posted_at_datetime_utc', ''),
                    employment_type=item.get('job_employment_type', ''),
                    experience_level=item.get('job_required_experience', {}).get('experience_level', '')
                )
                jobs.append(job)
            except Exception as e:
                logger.warning(f"Failed to parse job posting: {e}")
                continue
        
        return jobs
    
    def _format_salary(self, item: dict) -> Optional[str]:
        """Format salary information from job posting."""
        min_sal = item.get('job_min_salary')
        max_sal = item.get('job_max_salary')
        
        if min_sal and max_sal:
            return f"${min_sal:,} - ${max_sal:,}"
        elif min_sal:
            return f"${min_sal:,}+"
        elif max_sal:
            return f"Up to ${max_sal:,}"
        
        return None
    
    def filter_jobs(
        self,
        jobs: List[JobPosting],
        remove_duplicates: bool = True,
        check_red_flags: bool = True,
        trusted_only: bool = True,
        validate_description: bool = True
    ) -> List[JobPosting]:
        """
        Filter job postings based on quality criteria.
        
        Args:
            jobs: List of job postings to filter
            remove_duplicates: Remove duplicate postings
            check_red_flags: Check for suspicious terms
            trusted_only: Only include trusted domains
            validate_description: Validate description quality
        
        Returns:
            Filtered list of job postings
        """
        logger.info(f"Filtering {len(jobs)} job postings...")
        
        seen_hashes = set()
        filtered_jobs = []
        
        for job in jobs:
            # Check for duplicates
            if remove_duplicates:
                job_hash = self._get_job_hash(job)
                if job_hash in seen_hashes:
                    logger.debug(f"Duplicate job skipped: {job.title}")
                    continue
                seen_hashes.add(job_hash)
            
            # Check for red flags
            if check_red_flags and self._has_red_flags(job):
                logger.warning(f"⚠️ Job marked as suspect: {job.title}")
                continue
            
            # Check domain trust
            if trusted_only and not self._is_trusted_domain(job):
                logger.warning(f"🚫 Untrusted source: {job.title} - {job.url}")
                continue
            
            # Validate description
            if validate_description and not self._is_description_valid(job):
                logger.warning(f"⚠️ Low quality description: {job.title}")
                continue
            
            filtered_jobs.append(job)
        
        logger.info(f"✔️ {len(filtered_jobs)} valid job postings after filtering")
        return filtered_jobs
    
    def _get_job_hash(self, job: JobPosting) -> str:
        """Generate unique hash for job posting."""
        combined = job.title + job.description
        return hashlib.md5(combined.encode()).hexdigest()
    
    def _has_red_flags(self, job: JobPosting) -> bool:
        """Check if job posting contains red flag terms."""
        text = (job.title + ' ' + job.description).lower()
        return any(term in text for term in RED_FLAG_TERMS)
    
    def _is_trusted_domain(self, job: JobPosting) -> bool:
        """Check if job posting is from a trusted domain."""
        return any(domain in job.url for domain in TRUSTED_DOMAINS)
    
    def _is_description_valid(self, job: JobPosting) -> bool:
        """Validate job description quality."""
        desc = job.description
        # Check minimum word count and avoid all-caps descriptions
        return len(desc.split()) > 30 and not desc.isupper()
    
    def extract_resume(self, file_path: str) -> Resume:
        """
        Extract text from resume file (PDF or DOCX).
        
        Args:
            file_path: Path to resume file
        
        Returns:
            Resume object with extracted text
        
        Raises:
            SquirrelException: If extraction fails
        """
        if not os.path.exists(file_path):
            raise SquirrelException(f"Resume file not found: {file_path}")
        
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.pdf':
                text = self._extract_pdf(file_path)
            elif file_ext in ['.docx', '.doc']:
                text = self._extract_docx(file_path)
            else:
                raise SquirrelException(f"Unsupported file type: {file_ext}")
            
            # Clean the extracted text
            cleaned_text = self._clean_resume_text(text)
            
            logger.info(f"Resume extracted from {file_path}")
            return Resume(
                text=cleaned_text,
                file_path=file_path,
                file_type=file_ext[1:]
            )
            
        except Exception as e:
            logger.error(f"Failed to extract resume: {e}")
            raise SquirrelException(f"Resume extraction failed: {e}")
    
    def _extract_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        with pdfplumber.open(file_path) as pdf:
            pages = [page.extract_text(layout=True) for page in pdf.pages]
        return "\n".join(p for p in pages if p).strip()
    
    def _extract_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file_path)
        return "\n".join(para.text for para in doc.paragraphs)
    
    def _clean_resume_text(self, text: str) -> str:
        """Clean and normalize resume text."""
        # Remove multiple blank lines
        text = re.sub(r'\n\s*\n', '\n', text)
        # Remove bullet points and symbols
        text = re.sub(r'[•·●▪▶►]', '', text)
        # Remove leading/trailing whitespace
        text = re.sub(r'^\s+|\s+$', '', text)
        # Remove special characters
        text = re.sub(r'[^\w\s.,;:!?-]', '', text)
        # Normalize newlines
        text = re.sub(r'\n+', '\n', text)
        # Replace tabs with spaces
        text = text.replace('\t', ' ')
        # Collapse multiple spaces
        text = re.sub(r' +', ' ', text)
        # Fix concatenated words
        fixed = " ".join(wordninja.split(text.strip()))
        return fixed
    
    def match_resume_to_jobs(
        self,
        resume: Resume,
        jobs: List[JobPosting],
        threshold: float = 0.2
    ) -> List[JobMatch]:
        """
        Match resume to job postings using TF-IDF similarity.
        
        Args:
            resume: Resume object
            jobs: List of job postings
            threshold: Minimum match score (0-1)
        
        Returns:
            Sorted list of job matches above threshold
        """
        logger.info(f"Matching resume to {len(jobs)} job postings...")
        
        matches = []
        
        for job in jobs:
            score = self._calculate_match_score(resume.text, job.description)
            logger.debug(f"Match score for {job.title}: {score:.2f}")
            
            if score >= threshold:
                match = JobMatch(
                    job=job,
                    match_score=score,
                    matched_keywords=self._extract_keywords(resume.text, job.description)
                )
                matches.append(match)
        
        # Sort by match score descending
        matches.sort(key=lambda x: x.match_score, reverse=True)
        
        logger.info(f"Found {len(matches)} matching jobs above threshold {threshold}")
        return matches
    
    def _calculate_match_score(self, resume_text: str, job_description: str) -> float:
        """Calculate similarity score between resume and job description."""
        if not resume_text or not job_description:
            return 0.0
        
        try:
            vectorizer = TfidfVectorizer().fit([resume_text, job_description])
            vectors = vectorizer.transform([resume_text, job_description])
            similarity = cosine_similarity(vectors[0:1], vectors[1:2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.warning(f"Match score calculation failed: {e}")
            return 0.0
    
    def _extract_keywords(
        self,
        resume_text: str,
        job_description: str,
        top_n: int = 10
    ) -> List[str]:
        """Extract common keywords between resume and job description."""
        try:
            vectorizer = TfidfVectorizer(max_features=top_n, stop_words='english')
            vectorizer.fit([resume_text, job_description])
            return list(vectorizer.get_feature_names_out())
        except Exception as e:
            logger.warning(f"Keyword extraction failed: {e}")
            return []
    
    def generate_cover_letter(
        self,
        job: JobPosting,
        resume_summary: str
    ) -> CoverLetter:
        """
        Generate a cover letter using OpenAI API.
        
        Args:
            job: Job posting
            resume_summary: Summary of candidate's experience
        
        Returns:
            CoverLetter object
        
        Raises:
            SquirrelException: If generation fails or API key missing
        """
        if not self.openai_api_key:
            raise SquirrelException("OpenAI API key not configured")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_api_key)
            
            prompt = f"""
Write a short, professional cover letter for a {job.title} position at {job.company}.
Here is a summary of the candidate's experience: {resume_summary}.
Make the letter concise, enthusiastic, and tailored to the role.
"""
            
            logger.info(f"Generating cover letter for {job.title} at {job.company}")
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            return CoverLetter(
                job_posting=job,
                content=content
            )
            
        except Exception as e:
            logger.error(f"Cover letter generation failed: {e}")
            raise SquirrelException(f"Cover letter generation failed: {e}")
    
    def run_full_pipeline(
        self,
        query: JobSearchQuery,
        resume_path: Optional[str] = None,
        generate_letters: bool = False,
        resume_summary: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Run full job search pipeline: search, filter, match, generate cover letters.
        
        Args:
            query: Job search query
            resume_path: Path to resume file (optional)
            generate_letters: Generate cover letters for top matches
            resume_summary: Resume summary for cover letter generation
        
        Returns:
            Dictionary with results: jobs, matches, cover_letters
        """
        results = {
            'jobs': [],
            'filtered_jobs': [],
            'matches': [],
            'cover_letters': []
        }
        
        # Step 1: Search for jobs
        jobs = self.search_jobs(query)
        results['jobs'] = jobs
        
        # Step 2: Filter jobs
        filtered_jobs = self.filter_jobs(jobs)
        results['filtered_jobs'] = filtered_jobs
        
        # Step 3: Match resume to jobs (if provided)
        if resume_path and filtered_jobs:
            resume = self.extract_resume(resume_path)
            matches = self.match_resume_to_jobs(resume, filtered_jobs)
            results['matches'] = matches
            
            # Step 4: Generate cover letters (if requested)
            if generate_letters and matches and resume_summary:
                top_matches = matches[:5]  # Top 5 matches
                for match in top_matches:
                    try:
                        cover_letter = self.generate_cover_letter(
                            match.job,
                            resume_summary
                        )
                        results['cover_letters'].append(cover_letter)
                    except Exception as e:
                        logger.warning(f"Cover letter generation failed: {e}")
                        continue
        
        return results
    
    def scrape(self, *args, **kwargs):
        return super().scrape(*args, **kwargs)
