"use client";
import { useState } from "react";
import { useAuth } from "@/app/context/AuthContext";

export default function SpotifyConnectionTest() {
  const { user, getAuthToken } = useAuth();
  const [testResults, setTestResults] = useState<string[]>([]);
  const [testing, setTesting] = useState(false);

  const addResult = (message: string) => {
    setTestResults(prev => [...prev, `${new Date().toLocaleTimeString()}: ${message}`]);
  };

  const testConnections = async () => {
    setTesting(true);
    setTestResults([]);
    
    const token = getAuthToken();
    if (!token) {
      addResult("❌ No auth token available");
      setTesting(false);
      return;
    }

    addResult("✅ Auth token found");

    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    };

    // Test 1: Direct gatekeeper connection
    try {
      addResult("🔄 Testing direct gatekeeper connection...");
      const response = await fetch('http://localhost:8000/user', { headers });
      if (response.ok) {
        const data = await response.json();
        addResult(`✅ Direct gatekeeper: ${data.user?.email || 'No email'}`);
      } else {
        addResult(`❌ Direct gatekeeper failed: ${response.status}`);
      }
    } catch (error) {
      addResult(`❌ Direct gatekeeper error: ${error}`);
    }

    // Test 2: Proxy route
    try {
      addResult("🔄 Testing proxy route...");
      const response = await fetch('/api/gateway/spotify/auth/profile', { headers });
      if (response.ok) {
        const data = await response.json();
        addResult("✅ Proxy route works - Spotify profile loaded");
      } else {
        addResult(`❌ Proxy route failed: ${response.status}`);
      }
    } catch (error) {
      addResult(`❌ Proxy route error: ${error}`);
    }

    // Test 3: Direct spotify endpoint
    try {
      addResult("🔄 Testing direct Spotify endpoint...");
      const response = await fetch('http://localhost:8000/api/spotify/auth/profile', { headers });
      if (response.ok) {
        const data = await response.json();
        addResult("✅ Direct Spotify endpoint works");
      } else {
        addResult(`❌ Direct Spotify endpoint failed: ${response.status}`);
      }
    } catch (error) {
      addResult(`❌ Direct Spotify endpoint error: ${error}`);
    }

    setTesting(false);
  };

  if (!user) {
    return (
      <div className="p-4 bg-yellow-100 border border-yellow-400 rounded">
        <p>Please log in to test Spotify connections</p>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-2xl mx-auto">
      <h2 className="text-2xl font-bold mb-4">Spotify Connection Test</h2>
      
      <div className="mb-4">
        <p className="text-sm text-gray-600">
          User: {user.email} | Token: {getAuthToken() ? '✅ Present' : '❌ Missing'}
        </p>
      </div>

      <button
        onClick={testConnections}
        disabled={testing}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:opacity-50 mb-4"
      >
        {testing ? 'Testing...' : 'Test Connections'}
      </button>

      {testResults.length > 0 && (
        <div className="bg-gray-100 p-4 rounded">
          <h3 className="font-semibold mb-2">Test Results:</h3>
          <div className="space-y-1">
            {testResults.map((result, index) => (
              <div key={index} className="text-sm font-mono">
                {result}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="mt-6 text-sm text-gray-600">
        <h4 className="font-semibold mb-2">What this tests:</h4>
        <ul className="list-disc list-inside space-y-1">
          <li>Direct gatekeeper authentication</li>
          <li>Next.js proxy route (/api/gateway/...)</li>
          <li>Direct Spotify endpoint access</li>
        </ul>
      </div>
    </div>
  );
}
