"""Transaction model and categorization logic."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import config


@dataclass
class Transaction:
    """Represents a single transaction from a bank statement."""
    date: datetime
    description: str
    amount: float
    category: Optional[str] = None
    
    def __post_init__(self):
        """Automatically categorize transaction if not already categorized."""
        if self.category is None:
            self.category = self.categorize()
    
    def categorize(self) -> str:
        """Categorize transaction based on description."""
        description_lower = self.description.lower()
        
        for category, keywords in config.CATEGORIES.items():
            if any(keyword in description_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            'date': self.date.strftime(config.DATE_FORMAT),
            'description': self.description,
            'amount': self.amount,
            'category': self.category
        }
