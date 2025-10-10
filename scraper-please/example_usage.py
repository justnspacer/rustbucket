"""
Example usage of the Scraper-Please framework.
Demonstrates both direct SDK usage and the ScraperManager.
"""
import logging
from scraper_please import ScraperManager, ScraperType, FoolsballScraper

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


def example_direct_scraper():
    """Example 1: Using the scraper directly."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Direct Scraper Usage")
    print("="*60)
    
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
        
        # 4. Get rate limiter stats
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


def example_scraper_manager():
    """Example 2: Using the ScraperManager (recommended)."""
    print("\n" + "="*60)
    print("EXAMPLE 2: ScraperManager Usage (Recommended)")
    print("="*60)
    
    # Use context manager for automatic cleanup
    with ScraperManager() as manager:
        
        # 1. Get scraper with default source
        print("\n=== Using ESPN Source ===")
        scraper = manager.get_scraper(ScraperType.FOOLSBALL)
        teams = scraper.get_teams()
        print(f"Found {len(teams)} teams from {scraper.source}")
        
        # 2. Switch data source
        print("\n=== Switching to NFL Source ===")
        manager.switch_source(ScraperType.FOOLSBALL, "nfl")
        print(f"Active source: {manager.get_active_source(ScraperType.FOOLSBALL)}")
        
        # 3. Get available sources
        print("\n=== Available Sources ===")
        sources = manager.get_available_sources(ScraperType.FOOLSBALL)
        print(f"Available sources: {sources}")
        
        # 4. Get scraper stats
        print("\n=== Scraper Manager Stats ===")
        stats = manager.get_scraper_stats()
        print(f"Active scrapers: {stats['active_scrapers']}")
        print(f"Active sources: {stats['active_sources']}")
        
        # 5. Cache management
        print("\n=== Cache Management ===")
        print("Invalidating team data cache...")
        manager.invalidate_cache(ScraperType.FOOLSBALL, cache_key="foolsball:teams:espn")
        print("Cache invalidated")
        
        # 6. Fetch fresh data after cache invalidation
        print("\n=== Fetching Fresh Data ===")
        scraper = manager.get_scraper(ScraperType.FOOLSBALL, source="espn")
        teams = scraper.get_teams()
        print(f"Fetched {len(teams)} teams (fresh data)")


def example_api_usage():
    """Example 3: Using the REST API (requires running server)."""
    print("\n" + "="*60)
    print("EXAMPLE 3: REST API Usage")
    print("="*60)
    print("\nTo use the REST API:")
    print("1. Start the server: python run.py")
    print("2. Access the API at http://localhost:8000")
    print("\nExample API calls:")
    print("  curl http://localhost:8000/api/v1/teams")
    print("  curl http://localhost:8000/api/v1/players?team_id=1")
    print("  curl http://localhost:8000/api/v1/scores")
    print("  curl http://localhost:8000/api/v1/sources")
    print("\nAPI Documentation:")
    print("  Swagger UI: http://localhost:8000/docs")
    print("  ReDoc: http://localhost:8000/redoc")


def main():
    """Run all examples."""
    print("\n" + "="*60)
    print("SCRAPER-PLEASE EXAMPLES")
    print("="*60)
    
    # Example 1: Direct scraper usage
    example_direct_scraper()
    
    # Example 2: ScraperManager usage (recommended)
    example_scraper_manager()
    
    # Example 3: API usage info
    example_api_usage()
    
    print("\n" + "="*60)
    print("Examples completed!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
