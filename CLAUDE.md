# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A build-less, dependency-free static site (deployed to free static hosting, e.g. Cloudflare Pages; `bash scripts/build.sh` → `dist/`) for retail-store inbound/return inspection ("입고 검수"). Staff scan barcodes on phones/BT scanners and check them against a product list pulled from the company's internal web system. There is no package.json, build, lint, or test tooling — edit files directly and open `index.html`/`start.html` in a browser. All user-facing text and docs are Korean; keep that.

## Architecture

- **`index.html`** (~6k lines, ~578KB) — the entire inspection app: inline CSS/JS, plus inlined vendored libs (qrcode-generator 1.4.4, ZXing 0.21.3 barcode decoder). Don't try to "extract" or reformat the vendored blocks. It loads `config.js` first.
- **`config.js`** — sets `window.INBOUND_CONFIG` (Firebase web config, optional `appCheckKey`). Public by design; data safety relies on Firestore rules + App Check (see `보안안내.md`). Leave Firebase blank → app falls back to per-device, non-shared checking. Firebase SDK (compat, version `FB_VER`) is lazy-loaded from gstatic in `firebaseInit()`, anonymous auth, Firestore paths `stores/{store}/sessions/{code}` and `.../counts/{device}`. Writes must stay within the key allowlists in the Firestore rules documented in `보안안내.md` — adding a new field to a session/count doc requires updating those rules too.
- **Bookmarklet pipeline** — the store PC bookmarklets scrape the company system's ag-Grid (via `__agComponent` on `.ag-root`, including same-origin iframes) and hand data to `index.html`:
  - `listgrab.js` → "리스트 가져오기" (reads inbound/return list, opens the app with store/slip/items prefilled)
  - `returnfill.js` → "반품 입력하기" (fills box number / processed qty back into the return screen; never saves — user presses save)
  - `bookmarklets.js` → **generated-by-hand copy**: defines `window.BM_LIST` / `window.BM_RETURN` as JS strings of the bookmarklet source (with `__APP_URL__` placeholder). Consumed by `start.html` and `리스트가져오기_설치.html`. **When you change `listgrab.js` or `returnfill.js`, the corresponding string in `bookmarklets.js` must be updated, and `북마크모음.html` (Chrome bookmark import file, contains the same code) too** — nothing automates this.
- **`start.html`** — store-facing install page (QR for phones, drag-to-bookmarkbar links built from `bookmarklets.js`, uses `qrcode.js`). `리스트가져오기_설치.html` is a legacy redirect to it.
- **Docs** (under `docs/` (store/admin/deploy/dev; see `docs/README.md`)) — update them when behavior they describe changes.

## Conventions / gotchas

- `config.js` is a plain script: never put `import`/`initializeApp` lines in it.
- State is persisted in `localStorage` through a small wrapper (see ~`index.html:3736`) — use it rather than raw calls.
- Bookmarklet code must stay ES5-style and self-contained (it's pasted into a `javascript:` URL); the target system's grid columns are matched by Korean header names (`HEAD` regexes).
- Commit messages in this repo are written in Korean, short, describing the user-visible behavior change. Default branch is `main`; local branch is `master`.
- Deploy: private repo, so no GitHub Pages. Host builds with `bash scripts/build.sh` (output `dist/`); new app files must be added to the `cp` list there. See `docs/deploy/배포안내.md`.
