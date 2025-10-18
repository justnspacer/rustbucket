# Nothing App
## A app that reads bank statement PDFs and can analyze and track transactions. Spending trends based on transaction categories show expense changes over time

## Supported Banks

### Bank Name Key
For privacy and generalization, banks are referred to by generic names in the code:
- **Bank_One** = Apple Card (credit card statements)
- **Bank_Two** = Chase Bank (checking and savings)
- **Bank_Three** = Ally Bank (savings and money market)
- **Bank_Four** = CAFCU (credit union shares/savings)

### Features by Bank
- **Bank_One** - Full support for monthly credit card statements
- **Bank_Two** - Checking and Savings account statements
- **Bank_Three** - Savings and Money Market accounts
- **Bank_Four** - Credit Union savings/shares accounts

## Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Place your bank statement PDFs in the `statements/` directory
   - Supports Bank_One (credit card) statements
   - Supports Bank_Two (checking and savings) statements
   - Supports Bank_Three (savings) statements
   - Supports Bank_Four (credit union) statements
   - Auto-detects statement type

### Usage

Run the application:
```bash
python main.py
```

Or use the convenience scripts:
- Windows: Double-click `run.bat` or run it from command prompt
- Linux/Mac: `./run.sh`

### Features

The app provides an interactive menu with the following options:

1. **List all statements** - View all PDF files in the statements directory
2. **Analyze statement** - Parse and analyze a single statement
3. **Analyze all statements** - Combine and analyze all statements
4. **View summary report** - Generate detailed spending summary
5. **Generate visualizations** - Create charts and graphs:
   - Category Breakdown (Pie Chart)
   - Daily Spending Trends (Line Chart)
   - Category Trends Over Time (Area Chart)

### Transaction Categories

The app automatically categorizes transactions into:
- Food (restaurants, groceries, coffee shops)
- Transportation (Uber, Lyft, gas, parking)
- Entertainment (streaming services, movies, games)
- Shopping (Amazon, retail stores)
- Utilities (electricity, internet, phone)
- Health (pharmacy, medical)
- Travel (hotels, airlines)
- Other (uncategorized)

### Output

Generated visualizations are saved in the `output/` directory.

## Project Structure

```
nothing/
├── main.py              # Main application entry point
├── config.py            # Configuration and settings
├── transaction.py       # Transaction model and categorization
├── bank_one_parser.py        # PDF parsing logic for Bank_One statements
├── bank_two_parser.py      # PDF parsing logic for Bank_Two statements
├── bank_three_parser.py       # PDF parsing logic for Bank_Three statements
├── bank_four_parser.py      # PDF parsing logic for Bank_Four statements
├── unified_parser.py    # Auto-detection and routing
├── analyzer.py          # Transaction analysis and visualization
├── requirements.txt     # Python dependencies
├── statements/          # Place PDF statements here
└── output/             # Generated reports and visualizations
```

## Example

1. Place PDFs in `statements/` directory:
   - Bank_One statements (credit card)
   - Bank_Two statements (checking/savings)
   - Bank_Three statements (savings)
   - Bank_Four statements (credit union)
2. Run `python main.py`
3. Select option 2 to analyze a statement (auto-detects bank type)
4. View transactions in formatted table
5. Select option 4 to see spending summary
6. Select option 5 to generate visualizations

## Notes

- The app automatically detects which bank a PDF is from (Bank_One through Bank_Four)
- Only expense transactions are tracked (deposits and income are filtered out)
- Bank_Three and Bank_Four statements are typically savings accounts with minimal expenses
- Refunds and returns are tracked separately in the summary report
- Mix and match statements from different banks in the same analysis
