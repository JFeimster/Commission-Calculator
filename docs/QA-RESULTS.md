# QA results

- Node model tests: 16 passed.
- Chromium offline rendered fixtures: 11 passed (root, 4 source variants, production build, review root and 4 nested export variants). All passed baseline and changed inputs, validation, reset, CSV and JSON downloads, and 320/390 px horizontal-overflow checks. Local HTML/CSS/module paths resolved before rendering.
- Gallery preview and link file existence checks passed; production excludes sites, previews and references.
- HTTP browser navigation blocked by environment policy (ERR_BLOCKED_BY_ADMINISTRATOR). This is NOT a live HTTP smoke test; run `python tests/browser_qa.py` locally after installing Playwright/Chromium. Print dialog, native share, clipboard permissions and accessibility conformance have not been fully tested.
- Screenshots are actual offline Chromium renders, not deployed captures.

- Naming revision: previous offline browser results in `browser-qa.json` retain their original paths as historical evidence. The new slug is checked by the build workflow.
