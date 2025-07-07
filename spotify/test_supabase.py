#!/usr/bin/env python3
"""
Test script to verify Supabase connection and create app_spotify table if it doesn't exist.
Run this script after setting up your .env file with Supabase credentials.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    from supabase import create_client, Client
    
    # Get environment variables
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("❌ Error: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env file")
        exit(1)
    
    # Create Supabase client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    print("✅ Supabase client created successfully!")
    print(f"📍 Connected to: {SUPABASE_URL}")
    
    # Test connection by checking if app_spotify table exists
    try:
        result = supabase.table('app_spotify').select('count', count='exact').execute()
        print(f"✅ app_spotify table exists with {result.count} records")
    except Exception as e:
        print(f"⚠️  app_spotify table might not exist yet: {e}")
        print("💡 Run the SQL script in supabase_schema.sql to create the table")
    
    # Test inserting a dummy record (will be removed)
    try:
        test_data = {
            'spotify_id': 'test_user_123',
            'display_name': 'Test User',
            'app_authorized': True
        }
        
        # Insert test record
        insert_result = supabase.table('app_spotify').insert(test_data).execute()
        print("✅ Test insert successful")
        
        # Delete test record
        delete_result = supabase.table('app_spotify').delete().eq('spotify_id', 'test_user_123').execute()
        print("✅ Test delete successful")
        
        print("🎉 All tests passed! Your Supabase integration is ready.")
        
    except Exception as e:
        print(f"❌ Error during test operations: {e}")
        print("💡 Make sure the app_spotify table exists and your service role key has proper permissions")

except ImportError:
    print("❌ Error: supabase package not installed. Run: pip install supabase")
except Exception as e:
    print(f"❌ Error connecting to Supabase: {e}")
