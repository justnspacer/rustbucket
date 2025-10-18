"""Parser for Bank_Three PDF statements."""
import re
from datetime import datetime
from pathlib import Path
from typing import List
import pdfplumber
from transaction import Transaction

class BankThreeParser:
    """Parser for Bank_Three PDF statements (primarily savings accounts)."""
    
    def __init__(self, pdf_path: Path):
        """Initialize parser with PDF file path."""
        self.pdf_path = pdf_path
        self.transactions: List[Transaction] = []
        self.account_type = 'savings'  # Bank_Three statements are typically savings
    
    def parse(self) -> List[Transaction]:
        """Parse PDF and extract transactions."""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    self._extract_transactions_from_text(text)
        
        return self.transactions
    
    def _extract_transactions_from_text(self, text: str):
        """Extract transactions from page text.        
        Format: DATE DESCRIPTION CREDITS DEBITS BALANCE
        """
        lines = text.split('\n')
        
        for line in lines:
            # Skip header lines
            if 'Date' in line and 'Description' in line:
                continue
            if 'Beginning Balance' in line or 'Ending Balance' in line:
                continue
            
            # Pattern for Bank_Three transactions
            # Format: MM/DD/YYYY DESCRIPTION $AMOUNT -$AMOUNT $BALANCE
            # or: MM/DD/YYYY DESCRIPTION -$AMOUNT $AMOUNT $BALANCE
            pattern = r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+([-]?\$[\d,]+\.\d{2})\s+([-]?\$[\d,]+\.\d{2})\s+\$[\d,]+\.\d{2}'
            match = re.search(pattern, line)
            
            if match:
                date_str, description, credit_str, debit_str = match.groups()
                
                try:
                    # Parse date
                    date = datetime.strptime(date_str, "%m/%d/%Y")
                    
                    # Parse amounts
                    credit = float(credit_str.replace('$', '').replace(',', '').replace('-', '')) if credit_str != '-$0.00' else 0
                    debit = float(debit_str.replace('$', '').replace(',', '').replace('-', '')) if debit_str != '-$0.00' else 0
                    
                    # Skip interest and deposits (income, not expenses)
                    desc_lower = description.lower()
                    if any(word in desc_lower for word in ['interest paid', 'interest', 'dividend', 'deposit', 'ach deposit']):
                        continue
                    
                    # Only track debits (expenses) - negative amounts or explicit debits
                    if debit > 0:
                        transaction = Transaction(
                            date=date,
                            description=description.strip(),
                            amount=debit
                        )
                        self.transactions.append(transaction)
                    elif '-' in credit_str and credit > 0:
                        # This is actually a debit shown in the credit column
                        transaction = Transaction(
                            date=date,
                            description=description.strip(),
                            amount=credit
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
