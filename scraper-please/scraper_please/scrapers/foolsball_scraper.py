"""
NFL (Foolsball) scraper implementation.
Inherits from BaseScraper to provide real-time NFL player and team data.
Team data is cached for 24 hours, player data is cached for 5 minutes.
"""
import logging
from typing import List, Optional, Dict, Any
from datetime import datetime

from .base_scraper import BaseScraper, ScraperException, DataNotFoundException
from ..models.foolsball_models import (
    Team, Player, PlayerStats, GameScore, ScraperResponse
)
from ..config import (
    NFL_DATA_SOURCES, DEFAULT_NFL_SOURCE,
    CACHE_TTL_TEAM_DATA, CACHE_TTL_PLAYER_DATA
)

logger = logging.getLogger(__name__)


class FoolsballScraper(BaseScraper):
    """
    NFL data scraper that inherits from BaseScraper.
    Provides methods to fetch teams, players, stats, and live scores.
    """
    
    def __init__(
        self,
        source: str = DEFAULT_NFL_SOURCE,
        cache_enabled: bool = True,
        rate_limit_enabled: bool = True
    ):
        """
        Initialize NFL scraper.
        
        Args:
            source: Data source to use ('espn' or 'nfl')
            cache_enabled: Enable caching
            rate_limit_enabled: Enable rate limiting
        """
        super().__init__(
            cache_enabled=cache_enabled,
            rate_limit_enabled=rate_limit_enabled,
            adaptive_rate_limit=True  # Use adaptive rate limiting
        )
        
        self.source = source
        self.api_endpoints = NFL_DATA_SOURCES.get(source, NFL_DATA_SOURCES[DEFAULT_NFL_SOURCE])
        logger.info(f"FoolsballScraper initialized with source: {source}")
    
    def scrape(self, data_type: str, **kwargs) -> ScraperResponse:
        """
        Main scraping method - routes to specific scrapers.
        
        Args:
            data_type: Type of data to scrape ('teams', 'players', 'stats', 'scores')
            **kwargs: Additional parameters for specific scrapers
        
        Returns:
            ScraperResponse with data
        """
        try:
            if data_type == "teams":
                data = self.get_teams()
            elif data_type == "players":
                team_id = kwargs.get("team_id")
                data = self.get_players(team_id)
            elif data_type == "player":
                player_id = kwargs.get("player_id")
                if not player_id:
                    raise ValueError("player_id required for player data")
                data = self.get_player(player_id)
            elif data_type == "stats":
                player_id = kwargs.get("player_id")
                season = kwargs.get("season")
                if not player_id:
                    raise ValueError("player_id required for stats")
                data = self.get_player_stats(player_id, season)
            elif data_type == "scores":
                data = self.get_live_scores()
            else:
                raise ValueError(f"Unknown data_type: {data_type}")
            
            return ScraperResponse(
                success=True,
                data=data,
                cached=False,
                source=self.source
            )
            
        except Exception as e:
            logger.error(f"Scraping error: {e}")
            return ScraperResponse(
                success=False,
                error=str(e),
                source=self.source
            )
    
    def get_teams(self) -> List[Team]:
        """
        Fetch all NFL teams.
        Team data is cached for 24 hours as it changes infrequently.
        
        Returns:
            List of Team objects
        """
        cache_key = self._get_cache_key("foolsball", "teams", self.source)
        
        def fetch_teams():
            logger.info("Fetching NFL teams from API")
            url = self.api_endpoints.get("teams")
            if not url:
                raise DataNotFoundException("Teams endpoint not configured")
            
            response = self._make_request(url)
            data = response.json()
            
            # Parse based on source
            if self.source == "espn":
                return self._parse_espn_teams(data)
            elif self.source == "nfl":
                return self._parse_nfl_teams(data)
            else:
                raise ScraperException(f"Unknown source: {self.source}")
        
        # Use cache with 24-hour TTL for team data
        teams_data = self.fetch_with_cache(
            cache_key=cache_key,
            fetch_func=fetch_teams,
            ttl=CACHE_TTL_TEAM_DATA
        )
        
        return teams_data
    
    def get_players(self, team_id: Optional[str] = None) -> List[Player]:
        """
        Fetch NFL players, optionally filtered by team.
        Player data is cached for 5 minutes for real-time updates.
        
        Args:
            team_id: Optional team ID to filter players
        
        Returns:
            List of Player objects
        """
        cache_key = self._get_cache_key("foolsball", "players", self.source, team_id or "all")
        
        def fetch_players():
            logger.info(f"Fetching NFL players (team: {team_id or 'all'})")
            
            # For ESPN, we get players from team rosters
            if self.source == "espn":
                if team_id:
                    return self._fetch_team_roster(team_id)
                else:
                    # Fetch all teams and their rosters
                    teams = self.get_teams()
                    all_players = []
                    for team in teams:
                        players = self._fetch_team_roster(team.id)
                        all_players.extend(players)
                    return all_players
            
            elif self.source == "nfl":
                url = self.api_endpoints.get("players")
                if not url:
                    raise DataNotFoundException("Players endpoint not configured")
                
                params = {"team": team_id} if team_id else {}
                response = self._make_request(url, params=params)
                data = response.json()
                return self._parse_nfl_players(data)
            
            else:
                raise ScraperException(f"Unknown source: {self.source}")
        
        # Use cache with 5-minute TTL for player data
        players_data = self.fetch_with_cache(
            cache_key=cache_key,
            fetch_func=fetch_players,
            ttl=CACHE_TTL_PLAYER_DATA
        )
        
        return players_data
    
    def get_player(self, player_id: str) -> Player:
        """
        Fetch detailed data for a specific player.
        
        Args:
            player_id: Player ID
        
        Returns:
            Player object
        """
        cache_key = self._get_cache_key("foolsball", "player", self.source, player_id)
        
        def fetch_player():
            logger.info(f"Fetching player: {player_id}")
            
            if self.source == "espn":
                url = self.api_endpoints.get("player_stats")
                if not url:
                    raise DataNotFoundException("Player stats endpoint not configured")
                
                url = url.format(player_id=player_id)
                response = self._make_request(url)
                data = response.json()
                return self._parse_espn_player(data)
            
            else:
                raise ScraperException(f"Player endpoint not implemented for source: {self.source}")
        
        # Use cache with 5-minute TTL
        player_data = self.fetch_with_cache(
            cache_key=cache_key,
            fetch_func=fetch_player,
            ttl=CACHE_TTL_PLAYER_DATA
        )
        
        return player_data
    
    def get_player_stats(self, player_id: str, season: Optional[int] = None) -> PlayerStats:
        """
        Fetch player statistics.
        
        Args:
            player_id: Player ID
            season: Optional season year
        
        Returns:
            PlayerStats object
        """
        season = season or datetime.now().year
        cache_key = self._get_cache_key("foolsball", "stats", self.source, player_id, season)
        
        def fetch_stats():
            logger.info(f"Fetching stats for player: {player_id}, season: {season}")
            
            if self.source == "espn":
                url = self.api_endpoints.get("player_stats")
                if not url:
                    raise DataNotFoundException("Player stats endpoint not configured")
                
                url = url.format(player_id=player_id)
                response = self._make_request(url, params={"season": season})
                data = response.json()
                return self._parse_espn_player_stats(data, season)
            
            else:
                raise ScraperException(f"Stats endpoint not implemented for source: {self.source}")
        
        # Use cache with 5-minute TTL
        stats_data = self.fetch_with_cache(
            cache_key=cache_key,
            fetch_func=fetch_stats,
            ttl=CACHE_TTL_PLAYER_DATA
        )
        
        return stats_data
    
    def get_live_scores(self) -> List[Dict[str, Any]]:
        """
        Fetch live game scores.
        No caching for live data - always fetch fresh.
        
        Returns:
            List of GameScore dictionaries
        """
        logger.info("Fetching live scores")
        
        if self.source == "espn":
            url = self.api_endpoints.get("scoreboard")
            if not url:
                raise DataNotFoundException("Scoreboard endpoint not configured")
            
            response = self._make_request(url)
            data = response.json()
            return self._parse_espn_scores(data)
        
        else:
            raise ScraperException(f"Scoreboard not implemented for source: {self.source}")
    
    # Parsing methods for ESPN API
    def _parse_espn_teams(self, data: Dict) -> List[Team]:
        """Parse ESPN teams API response."""
        teams = []
        sports_data = data.get("sports", [{}])[0]
        leagues_data = sports_data.get("leagues", [{}])[0]
        teams_data = leagues_data.get("teams", [])
        
        for team_data in teams_data:
            team_info = team_data.get("team", {})
            teams.append(Team(
                id=team_info.get("id", ""),
                name=team_info.get("name", ""),
                abbreviation=team_info.get("abbreviation", ""),
                display_name=team_info.get("displayName", ""),
                location=team_info.get("location", ""),
                color=team_info.get("color"),
                alternate_color=team_info.get("alternateColor"),
                logo_url=team_info.get("logos", [{}])[0].get("href") if team_info.get("logos") else None,
                record=team_info.get("record", {}).get("items", [{}])[0].get("summary") if team_info.get("record") else None
            ))
        
        logger.info(f"Parsed {len(teams)} teams from ESPN")
        return teams
    
    def _parse_nfl_teams(self, data: Dict) -> List[Team]:
        """Parse NFL API teams response."""
        teams = []
        # NFL API structure would go here
        # This is a placeholder - actual implementation depends on NFL API structure
        logger.warning("NFL API parsing not fully implemented")
        return teams
    
    def _fetch_team_roster(self, team_id: str) -> List[Player]:
        """Fetch roster for a specific team from ESPN."""
        roster_url = f"https://site.api.espn.com/apis/site/v2/sports/football/nfl/teams/{team_id}/roster"
        response = self._make_request(roster_url)
        data = response.json()
        
        players = []
        athletes = data.get("athletes", [])
        
        for athlete_group in athletes:
            for athlete_data in athlete_group.get("items", []):
                players.append(Player(
                    id=athlete_data.get("id", ""),
                    name=athlete_data.get("fullName", ""),
                    display_name=athlete_data.get("displayName", ""),
                    first_name=athlete_data.get("firstName"),
                    last_name=athlete_data.get("lastName"),
                    team_id=team_id,
                    position=athlete_data.get("position", {}).get("abbreviation"),
                    jersey_number=athlete_data.get("jersey"),
                    headshot_url=athlete_data.get("headshot", {}).get("href")
                ))
        
        logger.debug(f"Fetched {len(players)} players for team {team_id}")
        return players
    
    def _parse_espn_player(self, data: Dict) -> Player:
        """Parse ESPN player API response."""
        return Player(
            id=data.get("id", ""),
            name=data.get("fullName", ""),
            display_name=data.get("displayName", ""),
            first_name=data.get("firstName"),
            last_name=data.get("lastName"),
            team_id=data.get("team", {}).get("id"),
            team_name=data.get("team", {}).get("name"),
            position=data.get("position", {}).get("abbreviation"),
            jersey_number=data.get("jersey"),
            height=data.get("height"),
            weight=data.get("weight"),
            age=data.get("age"),
            birth_date=data.get("dateOfBirth"),
            college=data.get("college", {}).get("name"),
            experience=data.get("experience", {}).get("years"),
            headshot_url=data.get("headshot", {}).get("href"),
            status=data.get("status", {}).get("type")
        )
    
    def _parse_nfl_players(self, data: Dict) -> List[Player]:
        """Parse NFL API players response."""
        # Placeholder for NFL API parsing
        logger.warning("NFL API player parsing not fully implemented")
        return []
    
    def _parse_espn_player_stats(self, data: Dict, season: int) -> PlayerStats:
        """Parse ESPN player stats."""
        stats_data = data.get("statistics", {})
        
        return PlayerStats(
            player_id=data.get("id", ""),
            player_name=data.get("fullName", ""),
            season=season,
            stats=stats_data
        )
    
    def _parse_espn_scores(self, data: Dict) -> List[Dict[str, Any]]:
        """Parse ESPN scoreboard data."""
        scores = []
        events = data.get("events", [])
        
        for event in events:
            competitions = event.get("competitions", [{}])[0]
            competitors = competitions.get("competitors", [])
            
            home_team = next((c for c in competitors if c.get("homeAway") == "home"), {})
            away_team = next((c for c in competitors if c.get("homeAway") == "away"), {})
            
            game_score = GameScore(
                game_id=event.get("id", ""),
                home_team=home_team.get("team", {}).get("abbreviation", ""),
                away_team=away_team.get("team", {}).get("abbreviation", ""),
                home_score=int(home_team.get("score", 0)),
                away_score=int(away_team.get("score", 0)),
                quarter=competitions.get("status", {}).get("period"),
                time_remaining=competitions.get("status", {}).get("displayClock"),
                status=competitions.get("status", {}).get("type", {}).get("name", "")
            )
            scores.append(game_score.dict() if hasattr(game_score, 'dict') else game_score.__dict__)
        
        logger.info(f"Parsed {len(scores)} live scores")
        return scores
    
    def refresh_player_data(self, player_id: Optional[str] = None):
        """
        Force refresh player data by invalidating cache.
        
        Args:
            player_id: Optional specific player to refresh, or None for all
        """
        if player_id:
            cache_key = self._get_cache_key("foolsball", "player", self.source, player_id)
            self.invalidate_cache(cache_key)
            logger.info(f"Refreshed cache for player: {player_id}")
        else:
            # Invalidate all player caches
            logger.info("Refreshing all player data caches")
            # Note: This is a simple implementation - could be more sophisticated
    
    def refresh_team_data(self):
        """Force refresh team data by invalidating cache."""
        cache_key = self._get_cache_key("foolsball", "teams", self.source)
        self.invalidate_cache(cache_key)
        logger.info("Refreshed team data cache")
