# Commission Calculator

Current branded implementation: Moonshine Capital.

One static financial application, four independently styled visual variations. Production default: **Variant 1 — Punk Utility Brutalism**. Other themes: Broker’s Manifesto, Lime Precision Fintech, Pastel Intelligence. All share the same deterministic calculation, state validation, export and reporting logic.

## Run

```sh
npm run build:all
npm run dev
```

`npm run build:all` runs the financial tests and regenerates production, review and portfolio outputs in sequence. No ZIP extraction or package installation is needed on subsequent builds. Edit the source files, then rerun this command.

Visit http://127.0.0.1:8080/ for the selected root or `/sites/` for the local design gallery. No install dependencies. Use a local HTTP server (not file://). To promote a theme: `npm run promote -- variant-1`. Root `index.html`, `style.css`, `script.js` are generated from `sites/variant-1/`; edit the source variant rather than generated files. Build refreshes them from the manifest. Promotion preserves all variants.

## Structure

- `sites/variant-1/` … `sites/variant-4/`: independent layouts, theme CSS, theme JSON and shared entry modules.
- `shared/config`: compensation and destination configuration.
- `shared/lib`: pure model, reports, interactive bindings.
- `scripts`: build, promote, export and local server.
- `dist/production`: selected application only; `dist/review`: all variants with gallery; `dist/portfolio/sites/...`: nested portable demo.
- `previews`: actual local browser screenshots; `references`: source brief and missing-reference notice.
- `tests`: model tests and browser QA script.

## Launch limitations

Demo mode only: no approved rates, agreement, recruitment URL, brochure, canonical URL or lead endpoint supplied. All such destinations are disabled or hidden until configured. Original visual reference PNGs unavailable; written direction used instead. No production deployment or existing repo changes were made. Contract-specific clawbacks, deductions, team overrides and unsupported compensation bases need implementation before verified launch. See `docs/COMMISSION-MODEL.md`, `docs/DESIGN-SYSTEM.md`, `docs/DEPLOYMENT.md`, and `docs/PORTFOLIO-IMPORT.md`.
