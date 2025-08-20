"""
CLI utilities for database maintenance and testing
"""
import click
from api.database import get_supabase_client, cleanup_expired_oauth_states
from api.config import SUPABASE_URL

@click.group()
def cli():
    """Spotify API Database Utilities"""
    pass

@cli.command()
def cleanup_oauth():
    """Clean up expired OAuth states"""
    try:
        deleted_count = cleanup_expired_oauth_states()
        click.echo(f"✅ Cleaned up {deleted_count} expired OAuth states")
    except Exception as e:
        click.echo(f"❌ Error cleaning up OAuth states: {e}")

@cli.command()
def test_db():
    """Test database connection"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('app_spotify').select('count').execute()
        click.echo(f"✅ Database connection successful")
        click.echo(f"📊 Connected to: {SUPABASE_URL}")
    except Exception as e:
        click.echo(f"❌ Database connection failed: {e}")

@cli.command()
@click.argument('user_id')
def show_user(user_id):
    """Show user's Spotify linkage info"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('app_spotify').select('*').eq('user_id', user_id).execute()
        if result.data:
            user = result.data[0]
            click.echo(f"✅ User found:")
            click.echo(f"   Spotify ID: {user['spotify_id']}")
            click.echo(f"   Linked at: {user.get('linked_at', 'N/A')}")
            click.echo(f"   Expires at: {user.get('expires_at', 'N/A')}")
        else:
            click.echo(f"❌ No Spotify linkage found for user: {user_id}")
    except Exception as e:
        click.echo(f"❌ Error retrieving user info: {e}")

@cli.command()
def list_users():
    """List all linked Spotify users"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('app_spotify').select('user_id, spotify_id, linked_at').execute()
        if result.data:
            click.echo(f"📋 Found {len(result.data)} linked users:")
            for user in result.data:
                click.echo(f"   {user['user_id']} -> {user['spotify_id']} (linked: {user.get('linked_at', 'N/A')})")
        else:
            click.echo("📋 No linked users found")
    except Exception as e:
        click.echo(f"❌ Error listing users: {e}")

@cli.command()
@click.argument('query')
def search_users_cli(query):
    """Search for users by Spotify ID (CLI version)"""
    try:
        supabase = get_supabase_client()
        result = supabase.table('app_spotify').select('user_id, spotify_id, linked_at').ilike('spotify_id', f'%{query}%').execute()
        if result.data:
            click.echo(f"🔍 Found {len(result.data)} users matching '{query}':")
            for user in result.data:
                click.echo(f"   {user['spotify_id']} (User ID: {user['user_id'][:8]}...)")
        else:
            click.echo(f"❌ No users found matching '{query}'")
    except Exception as e:
        click.echo(f"❌ Error searching users: {e}")

@cli.command()
def stats():
    """Show database statistics"""
    try:
        supabase = get_supabase_client()
        
        # Count total linked users
        users_result = supabase.table('app_spotify').select('user_id', count='exact').execute()
        total_users = users_result.count
        
        # Count pending OAuth states
        oauth_result = supabase.table('temp_oauth_state').select('state_key', count='exact').execute()
        pending_oauth = oauth_result.count
        
        click.echo("📊 Database Statistics:")
        click.echo(f"   Total linked users: {total_users}")
        click.echo(f"   Pending OAuth states: {pending_oauth}")
        
        if total_users > 0:
            # Get most recent linkage
            recent_result = supabase.table('app_spotify').select('spotify_id, linked_at').order('linked_at', desc=True).limit(1).execute()
            if recent_result.data:
                recent_user = recent_result.data[0]
                click.echo(f"   Most recent linkage: {recent_user['spotify_id']} at {recent_user.get('linked_at', 'N/A')}")
                
    except Exception as e:
        click.echo(f"❌ Error getting statistics: {e}")

if __name__ == '__main__':
    cli()
