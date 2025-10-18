"""Debug script to examine unknown PDFs and identify bank types."""
import pdfplumber
from pathlib import Path
import config

def examine_pdf(pdf_path: Path):
    """Examine a PDF to identify its type."""
    print(f"\n{'='*70}")
    print(f"File: {pdf_path.name}")
    print(f"{'='*70}")
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            print(f"Total pages: {len(pdf.pages)}")
            
            if not pdf.pages:
                print("No pages found!")
                return
            
            # Check first page
            first_page = pdf.pages[0]
            text = first_page.extract_text()
            
            if not text:
                print("No text found!")
                return
            
            # Show first 2000 characters
            print("\nFirst 2000 characters:")
            print("-" * 70)
            print(text[:2000])
            print("-" * 70)
            
            # Try to identify bank
            text_lower = text.lower()
            
            print("\nBank Identification:")
            if 'apple card' in text_lower or 'goldman sachs' in text_lower:
                print("  ✓ Bank_One")
            if 'chase' in text_lower or 'jpmorgan' in text_lower:
                print("  ✓ Bank_Two")
            if 'ally bank' in text_lower or 'ally.com' in text_lower:
                print("  ✓ Bank_Three")
            if 'cafcu' in text_lower or 'central alabama' in text_lower or 'credit union' in text_lower:
                print("  ✓ Bank_Four")
            
            # Look for transaction patterns
            lines = text.split('\n')
            print(f"\nTotal lines: {len(lines)}")
            print("\nSample lines (showing lines with dates and amounts):")
            print("-" * 70)
            
            import re
            count = 0
            for i, line in enumerate(lines[:100], 1):
                # Look for lines with dates and dollar amounts
                if re.search(r'\d{1,2}/\d{1,2}', line) and re.search(r'\$?[\d,]+\.\d{2}', line):
                    print(f"{i:3d}: {line}")
                    count += 1
                    if count >= 10:
                        break
            
            print("-" * 70)
    
    except Exception as e:
        print(f"Error: {e}")

def main():
    """Examine all PDFs in statements directory."""
    statements = sorted(config.STATEMENTS_DIR.glob("*.pdf"))
    
    print(f"Found {len(statements)} PDF file(s)\n")
    
    # Look for likely Bank_Three and Bank_Four statements
    unknown_pdfs = []
    for pdf in statements:
        name = pdf.name.lower()
        # Skip known types
        if 'apple card' in name or '20250' in name:
            continue
        unknown_pdfs.append(pdf)
    
    print(f"Examining {len(unknown_pdfs)} potentially new statement(s):\n")
    
    for pdf in unknown_pdfs:
        examine_pdf(pdf)
    
    print("\n" + "="*70)
    print("Examination complete!")
    print("="*70)

if __name__ == "__main__":
    main()
