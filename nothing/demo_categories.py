"""Demo script to show the new category listing functionality."""
from pathlib import Path
from unified_parser import UnifiedParser
from analyzer import TransactionAnalyzer
import config

def main():
    """Demo the new category listing feature."""
    print("="*70)
    print("DEMO: List Transactions by Category")
    print("="*70)
    
    # Parse all statements
    statements = list(config.STATEMENTS_DIR.glob('*.pdf'))
    print(f"\nParsing {len(statements)} statement(s)...\n")
    
    all_transactions = []
    for stmt in statements[:3]:  # Just use first 3 for quick demo
        print(f"📄 Parsing: {stmt.name}")
        parser = UnifiedParser(stmt)
        transactions = parser.parse()
        all_transactions.extend(transactions)
        print(f"   Found {len(transactions)} transactions")
    
    print(f"\n✅ Total: {len(all_transactions)} transactions\n")
    
    # Create analyzer
    analyzer = TransactionAnalyzer(all_transactions)
    
    # Show category summary
    print("\n" + "="*70)
    print("CATEGORY SUMMARY")
    print("="*70)
    category_spending = analyzer.get_spending_by_category()
    sorted_cats = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
    
    for cat, amount in sorted_cats:
        trans_count = len([t for t in all_transactions if t.category == cat])
        percentage = (amount / sum(category_spending.values())) * 100
        print(f"{cat.capitalize():15} - {trans_count:3} transactions - ${amount:8.2f} ({percentage:5.1f}%)")
    
    # Show detailed food transactions (since you mentioned many are food)
    print("\n" + "="*70)
    print("DETAILED VIEW: FOOD TRANSACTIONS")
    print("="*70)
    print(analyzer.list_category_transactions(category='food'))
    
    # Show all categories with limit
    print("\n" + "="*70)
    print("ALL CATEGORIES (limited to 5 transactions each)")
    print("="*70)
    print(analyzer.list_category_transactions(limit=5))

if __name__ == "__main__":
    main()
