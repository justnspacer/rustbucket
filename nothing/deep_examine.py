"""Deep dive into Bank_Three and Bank_Four statements to find all transaction patterns."""
import pdfplumber
from pathlib import Path
import config
import re

def examine_all_pages(pdf_path: Path):
    """Look at all pages for transactions."""
    print(f"\n{'='*70}")
    print(f"File: {pdf_path.name}")
    print(f"{'='*70}\n")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            all_transaction_lines = []
            
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if not text:
                    continue
                
                lines = text.split('\n')
                print(f"Page {page_num} - {len(lines)} lines")
                
                # Look for transaction patterns
                for line in lines:
                    # Pattern 1: Date at start with amount
                    if re.search(r'^\d{2}/\d{2}', line) and re.search(r'\$?[\d,]+\.\d{2}', line):
                        all_transaction_lines.append((page_num, line))
                    # Pattern 2: Line with "Date" header
                    elif 'Date' in line and ('Description' in line or 'Transaction' in line):
                        print(f"  Found header: {line}")
                    # Pattern 3: Lines with deposits/withdrawals
                    elif any(word in line.lower() for word in ['deposit', 'withdrawal', 'transfer', 'payment', 'purchase', 'fee']):
                        if re.search(r'\$?[\d,]+\.\d{2}', line):
                            all_transaction_lines.append((page_num, line))
            
            if all_transaction_lines:
                print(f"\nFound {len(all_transaction_lines)} potential transaction lines:\n")
                for page_num, line in all_transaction_lines[:20]:  # Show first 20
                    print(f"Page {page_num}: {line}")
            else:
                print("\nNo transactions found (savings account with interest only)")
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Examine Bank_Three and Bank_Four statements in detail."""
    statements = sorted(config.STATEMENTS_DIR.glob("*.pdf"))
    
    # Find Bank_Three and Bank_Four statements
    ally_cafcu = []
    for pdf in statements:
        name = pdf.name.lower()
        if 'apple card' not in name and '20250' not in name:
            ally_cafcu.append(pdf)
    
    print(f"Examining {len(ally_cafcu)} Bank_Three/Bank_Four statement(s) in detail:\n")
    
    for pdf in ally_cafcu:
        examine_all_pages(pdf)
    
    print("\n" + "="*70)
    print("Deep examination complete!")
    print("="*70)

if __name__ == "__main__":
    main()
