"""Transaction analyzer for spending trends and insights."""
from collections import defaultdict
from datetime import datetime
from typing import List, Dict
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from transaction import Transaction

# Set seaborn style for better looking plots
sns.set_style("whitegrid")
sns.set_palette("husl")


class TransactionAnalyzer:
    """Analyzer for transaction spending trends."""
    
    def __init__(self, transactions: List[Transaction]):
        """Initialize analyzer with list of transactions."""
        self.transactions = transactions
        self.df = self._create_dataframe()
        
        # Color palette for categories
        self.category_colors = {
            'food': '#FF6B6B',
            'transportation': '#4ECDC4',
            'entertainment': '#45B7D1',
            'shopping': '#FFA07A',
            'utilities': '#98D8C8',
            'health': '#F7DC6F',
            'travel': '#BB8FCE',
            'other': '#95A5A6'
        }
    
    def _create_dataframe(self) -> pd.DataFrame:
        """Create pandas DataFrame from transactions."""
        if not self.transactions:
            return pd.DataFrame()
        
        data = [t.to_dict() for t in self.transactions]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        return df
    
    def get_total_spending(self) -> float:
        """Get total spending across all transactions."""
        return self.df['amount'].sum() if not self.df.empty else 0.0
    
    def get_spending_by_category(self) -> Dict[str, float]:
        """Get total spending grouped by category."""
        if self.df.empty:
            return {}
        
        return self.df.groupby('category')['amount'].sum().to_dict()
    
    def get_average_transaction_amount(self) -> float:
        """Get average transaction amount."""
        return self.df['amount'].mean() if not self.df.empty else 0.0
    
    def get_spending_trends(self) -> pd.DataFrame:
        """Get daily spending trends."""
        if self.df.empty:
            return pd.DataFrame()
        
        daily_spending = self.df.groupby('date')['amount'].sum().reset_index()
        daily_spending.columns = ['date', 'total_spending']
        return daily_spending
    
    def plot_category_breakdown(self, save_path: str = None):
        """Create enhanced pie chart of spending by category."""
        if self.df.empty:
            print("No transactions to plot.")
            return
        
        category_spending = self.get_spending_by_category()
        
        # Filter out negative or zero values (refunds/returns)
        positive_spending = {k: v for k, v in category_spending.items() if v > 0}
        
        if not positive_spending:
            print("No positive spending to plot.")
            return
        
        # Create figure with better styling
        fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
        
        # Get colors for each category
        colors = [self.category_colors.get(cat, '#95A5A6') for cat in positive_spending.keys()]
        
        # Create pie chart with enhanced styling
        wedges, texts, autotexts = ax.pie(
            positive_spending.values(), 
            labels=[cat.title() for cat in positive_spending.keys()],
            autopct='%1.1f%%',
            startangle=90,
            colors=colors,
            explode=[0.05] * len(positive_spending),  # Slight separation
            shadow=True,
            textprops={'fontsize': 11, 'weight': 'bold'}
        )
        
        # Enhance percentage text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_weight('bold')
        
        # Add title with total
        total = sum(positive_spending.values())
        ax.set_title(f'Spending Breakdown by Category\nTotal: ${total:,.2f}', 
                     fontsize=16, weight='bold', pad=20)
        
        # Add legend with amounts
        legend_labels = [f'{cat.title()}: ${amt:,.2f}' 
                        for cat, amt in positive_spending.items()]
        ax.legend(legend_labels, loc='upper left', bbox_to_anchor=(1, 1), 
                 fontsize=10, frameon=True, shadow=True)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
    
    def plot_spending_trends(self, save_path: str = None):
        """Create enhanced line chart of daily spending trends."""
        if self.df.empty:
            print("No transactions to plot.")
            return
        
        trends = self.get_spending_trends()
        
        # Create figure with better styling
        fig, ax = plt.subplots(figsize=(14, 7), facecolor='white')
        
        # Plot with gradient fill
        ax.plot(trends['date'], trends['total_spending'], 
               marker='o', markersize=6, linewidth=2.5, 
               color='#3498db', label='Daily Spending')
        ax.fill_between(trends['date'], trends['total_spending'], 
                        alpha=0.3, color='#3498db')
        
        # Add moving average if enough data
        if len(trends) > 7:
            trends['ma7'] = trends['total_spending'].rolling(window=7, min_periods=1).mean()
            ax.plot(trends['date'], trends['ma7'], 
                   linestyle='--', linewidth=2, color='#e74c3c', 
                   label='7-Day Average', alpha=0.8)
        
        # Styling
        ax.set_title('Daily Spending Trends', fontsize=18, weight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12, weight='bold')
        ax.set_ylabel('Total Spending ($)', fontsize=12, weight='bold')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.legend(fontsize=11, frameon=True, shadow=True)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Rotate x-axis labels
        plt.xticks(rotation=45, ha='right')
        
        # Add statistics box
        total = trends['total_spending'].sum()
        avg = trends['total_spending'].mean()
        max_day = trends.loc[trends['total_spending'].idxmax()]
        
        stats_text = f'Total: ${total:,.2f}\nAvg/Day: ${avg:,.2f}\nMax Day: ${max_day["total_spending"]:,.2f}'
        ax.text(0.02, 0.98, stats_text, transform=ax.transAxes,
               fontsize=10, verticalalignment='top',
               bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
    
    def plot_category_trends(self, save_path: str = None):
        """Create enhanced stacked area chart showing spending trends by category over time."""
        if self.df.empty:
            print("No transactions to plot.")
            return
        
        # Filter to positive amounts only
        positive_df = self.df[self.df['amount'] > 0].copy()
        
        if positive_df.empty:
            print("No positive spending to plot.")
            return
        
        # Group by date and category
        category_trends = positive_df.groupby(['date', 'category'])['amount'].sum().unstack(fill_value=0)
        
        # Create figure with better styling
        fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')
        
        # Get colors for each category in the data
        colors = [self.category_colors.get(cat, '#95A5A6') for cat in category_trends.columns]
        
        # Create stacked area chart
        category_trends.plot(kind='area', stacked=True, alpha=0.7, ax=ax, 
                           color=colors, linewidth=2)
        
        # Styling
        ax.set_title('Spending Trends by Category Over Time', 
                    fontsize=18, weight='bold', pad=20)
        ax.set_xlabel('Date', fontsize=12, weight='bold')
        ax.set_ylabel('Amount ($)', fontsize=12, weight='bold')
        ax.grid(True, alpha=0.3, linestyle='--', axis='y')
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:,.0f}'))
        
        # Enhance legend
        ax.legend(title='Category', title_fontsize=11, fontsize=10,
                 bbox_to_anchor=(1.05, 1), loc='upper left',
                 frameon=True, shadow=True)
        
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
        plt.close()
    
    def plot_all_visualizations(self, output_dir: str = 'output'):
        """Generate all visualizations at once."""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        print("Generating visualizations...")
        
        # Category breakdown
        print("  - Category breakdown pie chart...")
        self.plot_category_breakdown(f'{output_dir}/category_breakdown.png')
        
        # Spending trends
        print("  - Daily spending trends...")
        self.plot_spending_trends(f'{output_dir}/spending_trends.png')
        
        # Category trends
        print("  - Category trends over time...")
        self.plot_category_trends(f'{output_dir}/category_trends.png')
        
        print(f"\n✅ All visualizations saved to '{output_dir}/' directory!")
    
    def get_summary_report(self) -> str:
        """Generate text summary report."""
        if self.df.empty:
            return "No transactions found."
        
        total = self.get_total_spending()
        avg = self.get_average_transaction_amount()
        category_spending = self.get_spending_by_category()
        
        # Separate positive and negative transactions
        positive_total = self.df[self.df['amount'] > 0]['amount'].sum()
        negative_total = self.df[self.df['amount'] < 0]['amount'].sum()
        refund_count = len(self.df[self.df['amount'] < 0])
        
        report = f"""
=== TRANSACTION SUMMARY REPORT ===

Total Transactions: {len(self.transactions)}
Total Spending: ${total:.2f}
Average Transaction: ${avg:.2f}
"""
        
        if refund_count > 0:
            report += f"""
Refunds/Returns: {refund_count} transaction(s) totaling ${abs(negative_total):.2f}
Net Spending (after refunds): ${total:.2f}
Gross Spending (before refunds): ${positive_total:.2f}
"""
        
        report += "\nSpending by Category:\n"
        for category, amount in sorted(category_spending.items(), key=lambda x: x[1], reverse=True):
            percentage = (amount / total) * 100 if total != 0 else 0
            report += f"  {category.capitalize()}: ${amount:.2f} ({percentage:.1f}%)\n"
        
        return report
    
    def get_transactions_by_category(self, category: str = None) -> Dict[str, List[Transaction]]:
        """Get transactions grouped by category or for a specific category.
        
        Args:
            category: Optional category name to filter by. If None, returns all categories.
        
        Returns:
            Dictionary mapping category names to lists of transactions
        """
        if not self.transactions:
            return {}
        
        # Group transactions by category
        categorized = defaultdict(list)
        for transaction in self.transactions:
            categorized[transaction.category].append(transaction)
        
        # If specific category requested, return only that
        if category:
            category_lower = category.lower()
            return {category_lower: categorized.get(category_lower, [])}
        
        # Return all categories, sorted by total spending
        category_totals = {cat: sum(t.amount for t in trans) 
                          for cat, trans in categorized.items()}
        sorted_categories = sorted(category_totals.items(), 
                                  key=lambda x: x[1], reverse=True)
        
        return {cat: categorized[cat] for cat, _ in sorted_categories}
    
    def list_category_transactions(self, category: str = None, limit: int = None) -> str:
        """Generate a detailed list of transactions by category.
        
        Args:
            category: Optional category to filter by (e.g., 'food', 'transportation')
            limit: Optional limit on number of transactions to show per category
        
        Returns:
            Formatted string with transaction details
        """
        categorized = self.get_transactions_by_category(category)
        
        if not categorized:
            return "No transactions found."
        
        report = "\n" + "="*70 + "\n"
        report += "TRANSACTIONS BY CATEGORY\n"
        report += "="*70 + "\n"
        
        for cat, transactions in categorized.items():
            # Sort transactions by date (most recent first)
            sorted_trans = sorted(transactions, key=lambda t: t.date, reverse=True)
            
            # Calculate category total
            cat_total = sum(t.amount for t in transactions)
            trans_count = len(transactions)
            
            report += f"\n📁 {cat.upper()} - {trans_count} transaction(s) - ${cat_total:.2f}\n"
            report += "-" * 70 + "\n"
            
            # Apply limit if specified
            display_trans = sorted_trans[:limit] if limit else sorted_trans
            
            for t in display_trans:
                report += f"  {t.date.strftime('%m/%d/%Y')} | ${t.amount:>8.2f} | {t.description[:45]}\n"
            
            if limit and len(sorted_trans) > limit:
                report += f"  ... and {len(sorted_trans) - limit} more transaction(s)\n"
            
            report += "\n"
        
        return report
