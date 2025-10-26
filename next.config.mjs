/** @type {import('next').NextConfig} */
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  },
  images: {
    unoptimized: true,
  },
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        fs: false,
        net: false,
        tls: false,
        crypto: false,
        stream: false,
        url: false,
        zlib: false,
        http: false,
        https: false,
        assert: false,
        os: false,
        path: false,
        util: false,
        buffer: false,
        events: false,
        querystring: false,
        punycode: false,
        "node:async_hooks": false,
        "node:process": false,
        "node:path": false,
        "node:url": false,
        "node:util": false,
        "node:buffer": false,
        "node:events": false,
        "node:fs": false,
        "node:os": false,
        "node:crypto": false,
        "node:stream": false,
        "node:querystring": false,
        "node:punycode": false,
        "node:zlib": false,
        "node:http": false,
        "node:https": false,
        "node:net": false,
        "node:tls": false,
        "node:assert": false,
      };
    }
    return config;
  },
}

export default nextConfig
