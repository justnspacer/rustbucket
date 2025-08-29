#!/usr/bin/env python3
"""
Test script to verify Spotify authentication integration
"""

import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Configuration
GATEKEEPER_URL = os.getenv("GATEKEEPER_URL", "http://localhost:8000")
SPOTIFY_URL = os.getenv("SPOTIFY_URL", "http://localhost:5000")

def test_direct_spotify_endpoints():
    """Test direct Spotify endpoints (no auth required)"""
    print("🧪 Testing direct Spotify endpoints...")
    
    try:
        # Test users endpoint
        response = requests.get(f"{SPOTIFY_URL}/spotify/users")
        print(f"✅ Users endpoint: {response.status_code} - Found {len(response.json().get('users', []))} users")
        
        # Test search endpoint
        response = requests.get(f"{SPOTIFY_URL}/spotify/search-users?q=test")
        print(f"✅ Search endpoint: {response.status_code}")
        
    except Exception as e:
        print(f"❌ Error testing direct endpoints: {e}")

def test_gatekeeper_auth(token):
    """Test gatekeeper authentication"""
    print("\n🧪 Testing gatekeeper authentication...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test user endpoint
        response = requests.get(f"{GATEKEEPER_URL}/user", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Gatekeeper auth: {response.status_code} - User: {user_data.get('user', {}).get('email', 'No email')}")
            return True
        else:
            print(f"❌ Gatekeeper auth failed: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing gatekeeper auth: {e}")
        return False

def test_authenticated_spotify_endpoints(token):
    """Test authenticated Spotify endpoints through gatekeeper"""
    print("\n🧪 Testing authenticated Spotify endpoints...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # Test profile endpoint
        response = requests.get(f"{GATEKEEPER_URL}/api/spotify/auth/profile", headers=headers)
        if response.status_code == 200:
            profile_data = response.json()
            print(f"✅ Profile endpoint: {response.status_code} - Spotify linked!")
            return True
        elif response.status_code == 404:
            error_data = response.json()
            if "not linked" in error_data.get("error", ""):
                print(f"⚠️  Profile endpoint: Spotify account not linked yet")
                return False
            else:
                print(f"❌ Profile endpoint: {response.status_code} - {error_data}")
                return False
        else:
            print(f"❌ Profile endpoint: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing authenticated endpoints: {e}")
        return False

def main():
    print("🚀 Starting Spotify Authentication Integration Tests")
    print("=" * 60)
    
    # Test direct endpoints first
    test_direct_spotify_endpoints()
    
    # Get token from user
    token = input("\n🔑 Enter your Supabase JWT token (or press Enter to skip auth tests): ").strip()
    
    if not token:
        print("⚠️  Skipping authenticated tests - no token provided")
        return
    
    # Test gatekeeper authentication
    if not test_gatekeeper_auth(token):
        print("❌ Gatekeeper authentication failed - cannot proceed with Spotify tests")
        return
    
    # Test authenticated endpoints
    spotify_linked = test_authenticated_spotify_endpoints(token)
    
    if not spotify_linked:
        spotify_id = input("\n🎵 Enter your Spotify ID to test account linking (or press Enter to skip): ").strip()
        
        if spotify_id:
            if test_spotify_linking(token, spotify_id):
                print("\n🎉 Spotify account linked successfully!")
                # Test endpoints again after linking
                test_authenticated_spotify_endpoints(token)
            else:
                print("\n❌ Failed to link Spotify account")
    else:
        print("\n🎉 All tests passed! Spotify integration is working correctly.")
    
    print("\n" + "=" * 60)
    print("✅ Testing complete!")

if __name__ == "__main__":
    main()
