"""
Quick test to verify the refactored code works correctly.
"""
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_imports():
    """Test that all imports work correctly."""
    print("\n=== Testing Imports ===")
    
    try:
        from scraper_please import ScraperManager, ScraperType, FoolsballScraper
        print("✓ Core imports successful")
        
        from api.schemas import ApiResponse, TeamResponse, PlayerResponse
        print("✓ API schema imports successful")
        
        from api.routes import router
        print("✓ API router import successful")
        
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_scraper_manager():
    """Test ScraperManager initialization."""
    print("\n=== Testing ScraperManager ===")
    
    try:
        from scraper_please import ScraperManager, ScraperType
        
        # Initialize manager
        manager = ScraperManager(cache_enabled=True, rate_limit_enabled=True)
        print("✓ ScraperManager initialized")
        
        # Get available sources
        sources = manager.get_available_sources(ScraperType.FOOLSBALL)
        print(f"✓ Available sources: {sources}")
        
        # Get active source
        active = manager.get_active_source(ScraperType.FOOLSBALL)
        print(f"✓ Active source: {active}")
        
        # Get stats
        stats = manager.get_scraper_stats()
        print(f"✓ Manager stats: {stats['active_scrapers']} active scrapers")
        
        # Cleanup
        manager.close_all()
        print("✓ Manager closed successfully")
        
        return True
    except Exception as e:
        print(f"✗ ScraperManager error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_scraper_instantiation():
    """Test direct scraper instantiation."""
    print("\n=== Testing Scraper Instantiation ===")
    
    try:
        from scraper_please import FoolsballScraper
        
        # Create scraper
        scraper = FoolsballScraper(
            source="espn",
            cache_enabled=True,
            rate_limit_enabled=True
        )
        print("✓ FoolsballScraper created")
        
        # Check properties
        print(f"✓ Source: {scraper.source}")
        print(f"✓ Cache enabled: {scraper.cache_enabled}")
        print(f"✓ Rate limit enabled: {scraper.rate_limit_enabled}")
        
        # Cleanup
        scraper.close()
        print("✓ Scraper closed successfully")
        
        return True
    except Exception as e:
        print(f"✗ Scraper instantiation error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_fastapi_app():
    """Test FastAPI app creation."""
    print("\n=== Testing FastAPI App ===")
    
    try:
        # Import without starting server
        import run
        
        print(f"✓ FastAPI app created")
        print(f"✓ App title: {run.app.title}")
        print(f"✓ App version: {run.app.version}")
        
        # Check routes
        routes = [route.path for route in run.app.routes]
        print(f"✓ Routes registered: {len(routes)}")
        
        return True
    except Exception as e:
        print(f"✗ FastAPI app error: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("="*60)
    print("SCRAPER-PLEASE REFACTORING TESTS")
    print("="*60)
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("ScraperManager", test_scraper_manager()))
    results.append(("Scraper Instantiation", test_scraper_instantiation()))
    results.append(("FastAPI App", test_fastapi_app()))
    
    # Print summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print("\n" + "-"*60)
    print(f"Results: {passed}/{total} tests passed")
    print("="*60 + "\n")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
