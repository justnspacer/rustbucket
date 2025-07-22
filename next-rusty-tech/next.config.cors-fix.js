/** @type {import('next').NextConfig} */
const nextConfig = {
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

module.exports = nextConfig;
