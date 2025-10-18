"""
Nothing App - Bank Statement Analyzer
Reads bank statement PDFs and analyzes transactions with spending trends.
"""
import sys
from pathlib import Path
from tabulate import tabulate
import config
from unified_parser import UnifiedParser
from analyzer import TransactionAnalyzer


def list_statements():
    """List all PDF statements in the statements directory."""
    pdf_files = list(config.STATEMENTS_DIR.glob("*.pdf"))
    return sorted(pdf_files)


def parse_statement(pdf_path: Path):
    """Parse a single statement and return transactions."""
    print(f"\n📄 Parsing: {pdf_path.name}")
    parser = UnifiedParser(pdf_path)
    info = parser.get_statement_info()
    
    # Show statement type
    if info['statement_type'] == 'bank_one':
        print(f"   Type: Bank_One Statement")
    elif info['statement_type'] == 'chase_bank':
        account_type = info.get('account_type', 'checking') or 'checking'
        print(f"   Type: Bank_Two {account_type.title()} Statement")
    elif info['statement_type'] == 'ally_bank':
        account_type = info.get('account_type', 'savings') or 'savings'
        print(f"   Type: Bank_Three {account_type.title()} Account")
    elif info['statement_type'] == 'cafcu':
        account_type = info.get('account_type', 'savings') or 'savings' 
        print(f"   Type: Bank_Four {account_type.title()} Account")
    else:
        print(f"   Type: Unknown (attempting to parse)")
    
    transactions = parser.parse()
    print(f"✅ Found {len(transactions)} transactions")
    return transactions


def display_menu():
    """Display interactive menu."""
    print("\n" + "="*50)
    print("💰 Nothing App - Bank Statement Analyzer")
    print("   (Multi-Bank Support)")
    print("="*50)
    print("\n1. List all statements")
    print("2. Analyze statement")
    print("3. Analyze all statements")
    print("4. View summary report")
    print("5. Generate visualizations")
    print("6. List transactions by category")
    print("7. Exit")
    print()


def display_transactions(transactions):
    """Display transactions in a table."""
    if not transactions:
        print("No transactions found.")
        return
    
    table_data = []
    for t in transactions:
        table_data.append([
            t.date.strftime("%m/%d/%Y"),
            t.description[:40],
            f"${t.amount:.2f}",
            t.category.capitalize()
        ])
    
    headers = ["Date", "Description", "Amount", "Category"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid"))


def main():
    """Main application entry point."""
    all_transactions = []
    
    while True:
        display_menu()
        choice = input("Select an option (1-7): ").strip()
        
        if choice == "1":
            # List all statements
            statements = list_statements()
            if not statements:
                print("\n❌ No PDF statements found in the statements directory.")
            else:
                print(f"\n📋 Found {len(statements)} statement(s):")
                for i, stmt in enumerate(statements, 1):
                    print(f"  {i}. {stmt.name}")
        
        elif choice == "2":
            # Analyze a specific statement
            statements = list_statements()
            if not statements:
                print("\n❌ No PDF statements found.")
                continue
            
            print("\nAvailable statements:")
            for i, stmt in enumerate(statements, 1):
                print(f"  {i}. {stmt.name}")
            
            try:
                idx = int(input("\nSelect statement number: ").strip()) - 1
                if 0 <= idx < len(statements):
                    transactions = parse_statement(statements[idx])
                    all_transactions = transactions
                    display_transactions(transactions)
                else:
                    print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        elif choice == "3":
            # Analyze all statements
            statements = list_statements()
            if not statements:
                print("\n❌ No PDF statements found.")
                continue
            
            all_transactions = []
            for stmt in statements:
                transactions = parse_statement(stmt)
                all_transactions.extend(transactions)
            
            print(f"\n✅ Total transactions across all statements: {len(all_transactions)}")
            display_transactions(all_transactions[-20:])  # Show last 20
        
        elif choice == "4":
            # View summary report
            if not all_transactions:
                print("\n❌ No transactions loaded. Please analyze a statement first.")
                continue
            
            analyzer = TransactionAnalyzer(all_transactions)
            print(analyzer.get_summary_report())
        
        elif choice == "5":
            # Generate visualizations
            if not all_transactions:
                print("\n❌ No transactions loaded. Please analyze a statement first.")
                continue
            
            analyzer = TransactionAnalyzer(all_transactions)
            
            print("\nGenerating visualizations...")
            print("1. Category Breakdown (Pie Chart)")
            print("2. Daily Spending Trends (Line Chart)")
            print("3. Category Trends Over Time (Area Chart)")
            print("4. All Visualizations")
            
            viz_choice = input("\nSelect visualization (1-4): ").strip()
            
            if viz_choice == "1":
                analyzer.plot_category_breakdown(
                    save_path=str(config.OUTPUT_DIR / "category_breakdown.png")
                )
            elif viz_choice == "2":
                analyzer.plot_spending_trends(
                    save_path=str(config.OUTPUT_DIR / "spending_trends.png")
                )
            elif viz_choice == "3":
                analyzer.plot_category_trends(
                    save_path=str(config.OUTPUT_DIR / "category_trends.png")
                )
            elif viz_choice == "4":
                analyzer.plot_category_breakdown(
                    save_path=str(config.OUTPUT_DIR / "category_breakdown.png")
                )
                analyzer.plot_spending_trends(
                    save_path=str(config.OUTPUT_DIR / "spending_trends.png")
                )
                analyzer.plot_category_trends(
                    save_path=str(config.OUTPUT_DIR / "category_trends.png")
                )
                print(f"\n✅ All visualizations saved to {config.OUTPUT_DIR}")
            else:
                print("❌ Invalid selection.")
        
        elif choice == "6":
            # List transactions by category
            if not all_transactions:
                print("\n❌ No transactions loaded. Please analyze a statement first.")
                continue
            
            analyzer = TransactionAnalyzer(all_transactions)
            
            print("\n� Available categories:")
            category_spending = analyzer.get_spending_by_category()
            sorted_cats = sorted(category_spending.items(), key=lambda x: x[1], reverse=True)
            
            print("  0. All categories")
            for i, (cat, amount) in enumerate(sorted_cats, 1):
                trans_count = len([t for t in all_transactions if t.category == cat])
                print(f"  {i}. {cat.capitalize()} - {trans_count} transaction(s) - ${amount:.2f}")
            
            try:
                cat_choice = input("\nSelect category (0 for all): ").strip()
                
                if cat_choice == "0":
                    # Show all categories
                    limit_input = input("Limit transactions per category? (enter number or press Enter for all): ").strip()
                    limit = int(limit_input) if limit_input else None
                    print(analyzer.list_category_transactions(limit=limit))
                else:
                    cat_idx = int(cat_choice) - 1
                    if 0 <= cat_idx < len(sorted_cats):
                        selected_cat = sorted_cats[cat_idx][0]
                        print(analyzer.list_category_transactions(category=selected_cat))
                    else:
                        print("❌ Invalid selection.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        elif choice == "7":
            print("\n�👋 Thanks for using Nothing App!")
            break
        
        else:
            print("\n❌ Invalid option. Please select 1-7.")


if __name__ == "__main__":
    main()
