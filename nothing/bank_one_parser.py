"""PDF parser for Bank_One statements."""
import re
from datetime import datetime
from pathlib import Path
from typing import List
import pdfplumber
from transaction import Transaction
import config


class BankOneParser:
    """Parser for Bank_One PDF statements."""
    
    def __init__(self, pdf_path: Path):
        """Initialize parser with PDF file path."""
        self.pdf_path = pdf_path
        self.transactions: List[Transaction] = []
    
    def parse(self) -> List[Transaction]:
        """Parse PDF and extract transactions."""
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    self._extract_transactions_from_text(text)
        
        return self.transactions
    
    def _extract_transactions_from_text(self, text: str):
        """Extract transactions from page text."""
        lines = text.split('\n')
        
        for line in lines:
            # Pattern for Bank_One statement format
            # Example: "07/31/2025 DUNKIN MOBILE AP 130 ROYALL STREET. CANTON 02021 MA USA 2% $0.20 $10.00"
            # Format: DATE DESCRIPTION PERCENTAGE $CASHBACK $AMOUNT
            # The amount is always the last dollar value on the line
            pattern = r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+\d+%\s+\$[\d,]+\.\d{2}\s+\$?([\d,]+\.\d{2})'
            match = re.search(pattern, line)
            
            if match:
                date_str, description, amount_str = match.groups()
                
                try:
                    # Parse date
                    date = datetime.strptime(date_str, "%m/%d/%Y")
                    
                    # Parse amount
                    amount = float(amount_str.replace(',', ''))
                    
                    # Skip negative amounts (refunds/returns) for now, or handle them
                    # You can modify this logic if you want to include returns
                    
                    # Create transaction
                    transaction = Transaction(
                        date=date,
                        description=description.strip(),
                        amount=amount
                    )
                    self.transactions.append(transaction)
                except ValueError as e:
                    # Skip if parsing fails
                    continue
            else:
                # Also check for returns/refunds which have (RETURN) and negative amounts
                return_pattern = r'(\d{2}/\d{2}/\d{4})\s+(.+?)\s+\(RETURN\)\s+-\$?([\d,]+\.\d{2})'
                return_match = re.search(return_pattern, line)
                if return_match:
                    date_str, description, amount_str = return_match.groups()
                    try:
                        date = datetime.strptime(date_str, "%m/%d/%Y")
                        amount = -float(amount_str.replace(',', ''))  # Negative for refund
                        
                        transaction = Transaction(
                            date=date,
                            description=description.strip() + " (RETURN)",
                            amount=amount
                        )
                        self.transactions.append(transaction)
                    except ValueError:
                        continue
    
    def _extract_year_from_filename(self) -> int:
        """Extract year from PDF filename."""
        # Pattern to match year in filename
        match = re.search(r'20\d{2}', self.pdf_path.name)
        if match:
            return int(match.group())
        return datetime.now().year
