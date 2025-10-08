"""
Example usage of the Foolsball scraper.
Demonstrates fetching NFL teams and players with different caching strategies.
"""
import logging
from scraper_please.scrapers.foolsball_scraper import FoolsballScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def main():
    """Demonstrate scraper functionality."""
    
    # Initialize the scraper
    scraper = FoolsballScraper(
        source="espn",  # Use ESPN as data source
        cache_enabled=True,
        rate_limit_enabled=True
    )
    
    try:
        # 1. Fetch all teams (cached for 24 hours)
        print("\n=== Fetching NFL Teams ===")
        teams = scraper.get_teams()
        print(f"Found {len(teams)} teams")
        for team in teams[:3]:  # Show first 3 teams
            print(f"  - {team.display_name} ({team.abbreviation})")
        
        # 2. Fetch players for a specific team (cached for 5 minutes)
        if teams:
            first_team = teams[0]
            print(f"\n=== Fetching Players for {first_team.display_name} ===")
            players = scraper.get_players(team_id=first_team.id)
            print(f"Found {len(players)} players")
            for player in players[:5]:  # Show first 5 players
                print(f"  - {player.display_name} ({player.position})")
        
        # 3. Fetch live scores (not cached - real-time data)
        print("\n=== Fetching Live Scores ===")
        scores = scraper.get_live_scores()
        print(f"Found {len(scores)} games")
        for score in scores[:3]:  # Show first 3 games
            print(f"  - {score.away_team} @ {score.home_team}: {score.away_score}-{score.home_score} ({score.status})")
        
        # 4. Using the generic scrape method
        print("\n=== Using Generic Scrape Method ===")
        response = scraper.scrape("teams")
        if response.success:
            print(f"Successfully scraped {len(response.data)} teams")
            print(f"Source: {response.source}")
            print(f"Cached: {response.cached}")
        
        # 5. Demonstrate cache refresh
        print("\n=== Refreshing Team Data ===")
        scraper.refresh_team_data()
        print("Team data cache invalidated")
        
        # Get rate limiter stats
        if scraper.rate_limiter:
            stats = scraper.rate_limiter.get_stats()
            print(f"\n=== Rate Limiter Stats ===")
            print(f"Calls used: {stats['current_calls']}/{stats['max_calls']}")
            print(f"Calls remaining: {stats['calls_remaining']}")
            print(f"Usage: {stats['percentage_used']:.1f}%")
    
    except Exception as e:
        logger.error(f"Error during scraping: {e}")
    
    finally:
        # Clean up
        scraper.close()
        print("\nScraper closed")


if __name__ == "__main__":
    main()
