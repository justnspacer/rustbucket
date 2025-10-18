"""Unified parser that auto-detects statement type."""
from pathlib import Path
from typing import List
import pdfplumber
from transaction import Transaction
from bank_one_parser import BankOneParser
from bank_two_parser import BankTwoParser
from bank_three_parser import BankThreeParser
from bank_four_parser import BankFourParser


class UnifiedParser:
    """Auto-detect and parse different types of bank statements."""
    
    def __init__(self, pdf_path: Path):
        """Initialize with PDF file path."""
        self.pdf_path = pdf_path
        self.statement_type = None
        self.parser = None
    
    def detect_statement_type(self) -> str:
        """Detect what type of statement this is."""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                if not pdf.pages:
                    return 'unknown'
                
                # Check first page
                first_page = pdf.pages[0]
                text = first_page.extract_text()
                
                if not text:
                    return 'unknown'
                
                text_lower = text.lower()
                
                # Check for Bank_One indicators
                if 'apple card' in text_lower or 'goldman sachs' in text_lower:
                    return 'bank_one'
                
                # Check for Bank_Two indicators
                if 'chase' in text_lower or 'jpmorgan chase' in text_lower:
                    return 'bank_two'
                
                # Check for Bank_Three indicators
                if 'ally bank' in text_lower or 'ally.com' in text_lower:
                    return 'bank_three'
                
                # Check for Bank_Four indicators
                if 'cafcu' in text_lower or 'cafcu.org' in text_lower or 'central alabama' in text_lower:
                    if 'federal' in text_lower or 'credit union' in text_lower or 'federally insured by ncua' in text_lower:
                        return 'bank_four'
                
                return 'unknown'
        except Exception:
            return 'unknown'
    
    def parse(self) -> List[Transaction]:
        """Parse the statement using the appropriate parser."""
        # Detect statement type
        self.statement_type = self.detect_statement_type()
        
        # Use appropriate parser
        if self.statement_type == 'bank_one':
            self.parser = BankOneParser(self.pdf_path)
        elif self.statement_type == 'bank_two':
            self.parser = BankTwoParser(self.pdf_path)
        elif self.statement_type == 'bank_three':
            self.parser = BankThreeParser(self.pdf_path)
        elif self.statement_type == 'bank_four':
            self.parser = BankFourParser(self.pdf_path)
        else:
            # Try Bank_One parser as fallback
            print(f"Warning: Could not detect statement type for {self.pdf_path.name}")
            print("Attempting to parse as Bank_One statement...")
            self.parser = BankOneParser(self.pdf_path)
        
        return self.parser.parse()
    
    def get_statement_info(self) -> dict:
        """Get information about the parsed statement."""
        # Ensure detection has been run
        if self.statement_type is None:
            self.statement_type = self.detect_statement_type()
        
        return {
            'filename': self.pdf_path.name,
            'statement_type': self.statement_type,
            'account_type': getattr(self.parser, 'account_type', None) if self.parser else None
        }
