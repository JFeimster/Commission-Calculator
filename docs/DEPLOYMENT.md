# Deployment

Node 20+ is needed only for build and local development. Run `npm test`, `npm run build` for `dist/production`, `npm run build:review` for `dist/review`, or `npm run export:portfolio` for the nested portfolio project. Run `npm run dev` and visit http://127.0.0.1:8080/; to test a build, run `node scripts/serve.mjs dist/production` or `node scripts/serve.mjs dist/review`. Use HTTP, not file://, because ES modules need a web origin.

Vercel configuration builds and deploys `dist/production` only. On GitHub Pages publish the contents of `dist/production` to the Pages artifact. Keep alternate variants and reference assets out of public production. Review build is noindex, not authenticated; apply hosting protection if required. Use trailing-slash or explicit index.html URLs for nested folders.

Set approved destinations in `shared/config/partner-links.js` and configure the canonical URL. The lead endpoint must be HTTPS, accept CORS for this site, validate consent and payloads server-side, enforce abuse controls, and return 2xx only after accepting requests. Never put API keys in browser JS. With no endpoint, email capture is hidden and local reports remain usable. Configure only authorized public links; verify before launch.
