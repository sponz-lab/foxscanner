#!/usr/bin/env bash
# 배포용 폴더(dist/)를 만든다. 문서·스크립트·CLAUDE.md 는 웹에 올리지 않는다.
# Cloudflare Pages / Netlify / Firebase Hosting 모두 이 결과물(dist/)을 쓴다.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist
cp index.html start.html config.js qrcode.js bookmarklets.js listgrab.js returnfill.js \
   북마크모음.html 리스트가져오기_설치.html dist/
cp deploy/_headers deploy/robots.txt dist/
echo "dist/ 준비 완료: $(ls dist | wc -l)개 파일"
