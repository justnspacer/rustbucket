import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  
  // Add rewrites for API calls to avoid CORS issues during development
  async rewrites() {
    return [
      {
        source: '/api/gateway/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
