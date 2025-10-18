"""Parser for Bank_Four (Credit Union) PDF statements."""
import re
from datetime import datetime
from pathlib import Path
from typing import List
import pdfplumber
from transaction import Transaction

class BankFourParser:
   
    def __init__(self, pdf_path: Path):
        """Initialize parser with PDF file path."""
        self.pdf_path = pdf_path
        self.transactions: List[Transaction] = []
        self.account_type = 'savings'  # Bank_Four statements are typically savings/shares
    
    def parse(self) -> List[Transaction]:
        """Parse PDF and extract transactions."""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Extract statement period for year
                    if not hasattr(self, 'statement_year'):
                        self._extract_statement_date(text)
                    self._extract_transactions_from_text(text)
        
        return self.transactions
    
    def _extract_statement_date(self, text: str):
        """Extract statement date to get year."""
        # Look for "Statement For: MM/DD/YYYY - MM/DD/YYYY"
        match = re.search(r'Statement For:\s+(\d{2}/\d{2}/\d{4})', text)
        if match:
            date_str = match.group(1)
            date = datetime.strptime(date_str, "%m/%d/%Y")
            self.statement_year = date.year
        else:
            self.statement_year = datetime.now().year
    
    def _extract_transactions_from_text(self, text: str):
        """Extract transactions from page text.
        
        Format: MM/DD [Eff. MM-DD] DESCRIPTION $AMOUNT- $BALANCE-
        Note: Amounts end with "-" 
        """
        lines = text.split('\n')
        
        for line in lines:
            # Skip header lines
            if 'Date' in line and 'Transaction' in line:
                continue
            if 'Balance-' in line:
                continue
            
            # Pattern for Bank_Four transactions
            # Format: MM/DD [Optional: Eff. MM-DD] DESCRIPTION $AMOUNT- $BALANCE-
            pattern = r'^(\d{2}/\d{2})(?:\s+Eff\.\s+\d{2}-\d{2})?\s+(.+?)\s+\$([\d,]+\.\d{2})-\s+\$([\d,]+\.\d{2})-'
            match = re.search(pattern, line.strip())
            
            if match:
                date_str, description, amount_str, balance_str = match.groups()
                
                try:
                    # Parse date (MM/DD, need year from statement period)
                    year = getattr(self, 'statement_year', datetime.now().year)
                    date = datetime.strptime(f"{date_str}/{year}", "%m/%d/%Y")
                    
                    # Parse amount
                    amount = float(amount_str.replace(',', ''))
                    
                    # Skip dividends and interest (income, not expenses)
                    desc_lower = description.lower()
                    if any(word in desc_lower for word in ['dividend', 'interest', 'deposit']):
                        continue
                    
                    # Track withdrawals, fees, purchases as expenses
                    if any(word in desc_lower for word in ['withdrawal', 'fee', 'purchase', 'payment', 'transfer out']):
                        transaction = Transaction(
                            date=date,
                            description=description.strip(),
                            amount=amount
                        )
                        self.transactions.append(transaction)
                
                except (ValueError, IndexError):
                    continue
    
    def _extract_year_from_filename(self) -> int:
        """Extract year from PDF filename."""
        match = re.search(r'20\d{2}', self.pdf_path.name)
        if match:
            return int(match.group())
        return datetime.now().year
