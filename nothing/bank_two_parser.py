"""Parser for Bank_Two PDF statements."""
import re
from datetime import datetime
from pathlib import Path
from typing import List
import pdfplumber
from transaction import Transaction
import config


class BankTwoParser:
    """Parser for Bank_Two PDF statements (checking and savings)."""
    
    def __init__(self, pdf_path: Path):
        """Initialize parser with PDF file path."""
        self.pdf_path = pdf_path
        self.transactions: List[Transaction] = []
        self.account_type = None  # 'checking' or 'savings'
    
    def parse(self) -> List[Transaction]:
        """Parse PDF and extract transactions."""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    # Detect account type
                    if self.account_type is None:
                        self._detect_account_type(text)
                    
                    # Extract transactions
                    self._extract_transactions_from_text(text)
        
        return self.transactions
    
    def _detect_account_type(self, text: str):
        """Detect if this is a checking or savings account."""
        text_lower = text.lower()
        if 'checking' in text_lower or 'total checks' in text_lower:
            self.account_type = 'checking'
        elif 'savings' in text_lower or 'interest earned' in text_lower:
            self.account_type = 'savings'
        else:
            self.account_type = 'checking'  # Default
    
    def _extract_transactions_from_text(self, text: str):
        """Extract transactions from page text.
        """
        lines = text.split('\n')
        
        for line in lines:
            # Skip header lines and non-transaction lines
            if any(skip in line.lower() for skip in ['balance', 'beginning', 'ending', 'deposits', 'withdrawals', 'date', 'description', 'checks']):
                if not re.search(r'\d{2}/\d{2}', line):  # Unless it has a date
                    continue
            
            # Pattern for Bank_Two transactions with running balance
            # Format: MM/DD DESCRIPTION AMOUNT RUNNING_BALANCE
            # Example: "07/2 Verizon Wireless Payments 706.31 34,033.92"
            # We want to capture the amount before the balance
            pattern = r'(\d{2}/\d{2})\s+(.+?)\s+([-+]?)(\$?)?([\d,]+\.\d{2})\s+([-+]?)(\$?)?([\d,]+\.\d{2})\s*$'
            match = re.search(pattern, line)
            
            if match:
                date_str, description, sign1, _, amount_str, sign2, _, balance_str = match.groups()
                
                try:
                    # The first number is the transaction amount, second is running balance
                    year = self._extract_year_from_filename()
                    date = datetime.strptime(f"{date_str}/{year}", "%m/%d/%Y")
                    amount = float(amount_str.replace(',', ''))
                    
                    # Skip deposits/credits (we only track expenses)
                    desc_lower = description.lower()
                    if any(word in desc_lower for word in ['deposit', 'dir dep', 'transfer from', 'zelle payment from', 'payment from']):
                        continue
                    
                    # Keep debits (expenses)
                    transaction = Transaction(
                        date=date,
                        description=description.strip(),
                        amount=amount
                    )
                    self.transactions.append(transaction)
                except ValueError:
                    continue
                continue
            
            # Pattern for simpler format without running balance
            # Example: "01/29 AMAZON.COM*ABC456 98.22"
            pattern2 = r'(\d{2}/\d{2})\s+(.+?)\s+([-+]?)(\$?)?([\d,]+\.\d{2})\s*$'
            match2 = re.search(pattern2, line)
            
            if match2:
                date_str, description, sign, _, amount_str = match2.groups()
                
                try:
                    year = self._extract_year_from_filename()
                    date = datetime.strptime(f"{date_str}/{year}", "%m/%d/%Y")
                    amount = float(amount_str.replace(',', ''))
                    
                    # Skip deposits/credits
                    desc_lower = description.lower()
                    if any(word in desc_lower for word in ['deposit', 'dir dep', 'transfer from', 'zelle payment from', 'payment from']):
                        continue
                    
                    # Apply sign if negative
                    if sign == '-':
                        amount = abs(amount)
                    
                    transaction = Transaction(
                        date=date,
                        description=description.strip(),
                        amount=amount
                    )
                    self.transactions.append(transaction)
                except ValueError:
                    continue
    
    def _extract_year_from_filename(self) -> int:
        """Extract year from PDF filename."""
        match = re.search(r'20\d{2}', self.pdf_path.name)
        if match:
            return int(match.group())
        return datetime.now().year
