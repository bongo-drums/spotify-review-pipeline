/** @type {import('next').NextConfig} */
const nextConfig = {
  // The file-backed data source reads web/data at request time; keep API routes dynamic.
  serverExternalPackages: ["pg"],
  outputFileTracingIncludes: { "/api/**": ["./data/**"] },
};
export default nextConfig;
