"""
Data models for job search operations.
"""
from typing import Optional, List
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class JobPosting:
    """Represents a job posting."""
    title: str
    company: str
    description: str
    url: str
    location: Optional[str] = None
    salary: Optional[str] = None
    date_posted: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    match_score: Optional[float] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'title': self.title,
            'company': self.company,
            'description': self.description,
            'url': self.url,
            'location': self.location,
            'salary': self.salary,
            'date_posted': self.date_posted,
            'employment_type': self.employment_type,
            'experience_level': self.experience_level,
            'match_score': self.match_score
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'JobPosting':
        """Create from dictionary."""
        return cls(
            title=data.get('title', ''),
            company=data.get('company', ''),
            description=data.get('description', ''),
            url=data.get('url', ''),
            location=data.get('location'),
            salary=data.get('salary'),
            date_posted=data.get('date_posted'),
            employment_type=data.get('employment_type'),
            experience_level=data.get('experience_level'),
            match_score=data.get('match_score')
        )


@dataclass
class Resume:
    """Represents a resume."""
    text: str
    file_path: str
    file_type: str  # 'pdf' or 'docx'
    extracted_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'text': self.text,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'extracted_at': self.extracted_at.isoformat()
        }


@dataclass
class JobMatch:
    """Represents a matched job with score."""
    job: JobPosting
    match_score: float
    matched_keywords: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        job_dict = self.job.to_dict()
        job_dict['match_score'] = self.match_score
        job_dict['matched_keywords'] = self.matched_keywords
        return job_dict


@dataclass
class CoverLetter:
    """Represents a generated cover letter."""
    job_posting: JobPosting
    content: str
    generated_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'job_title': self.job_posting.title,
            'company': self.job_posting.company,
            'content': self.content,
            'generated_at': self.generated_at.isoformat()
        }


@dataclass
class JobSearchQuery:
    """Represents a job search query."""
    keywords: str
    location: Optional[str] = None
    page: int = 1
    num_pages: int = 1
    country: str = "us"
    date_posted: str = "all"  # all, today, 3days, week, month
    employment_type: Optional[str] = None  # fulltime, parttime, contractor, intern
    remote_jobs_only: bool = False
    
    def to_params(self) -> dict:
        """Convert to API query parameters."""
        params = {
            'query': self.keywords,
            'page': str(self.page),
            'num_pages': str(self.num_pages),
            'country': self.country,
            'date_posted': self.date_posted
        }
        
        if self.location:
            params['query'] = f"{self.keywords} in {self.location}"
        
        if self.employment_type:
            params['employment_type'] = self.employment_type
        
        if self.remote_jobs_only:
            params['remote_jobs_only'] = 'true'
        
        return params
