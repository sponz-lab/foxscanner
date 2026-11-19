#!/usr/bin/env bash
# 배포용 폴더(dist/)를 만든다. 문서·스크립트·CLAUDE.md 는 웹에 올리지 않는다.
# Cloudflare Pages / Netlify / Firebase Hosting 모두 이 결과물(dist/)을 쓴다.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf dist && mkdir dist

# 북마크릿은 앱 주소를 안에 품고 있다. 주소가 바뀌면 옛 주소로 열리므로,
# 호스팅이 알려 주는 주소(SITE_URL)로 북마크모음.html 을 다시 만든다.
# Cloudflare Pages 는 CF_PAGES_URL, Netlify 는 URL 을 자동으로 넣어 준다.
SITE_URL="${SITE_URL:-${CF_PAGES_URL:-${URL:-}}}"
if [ -n "$SITE_URL" ]; then
  python3 scripts/make-bookmarks.py "$SITE_URL"
else
  echo "build: SITE_URL 이 없어 북마크모음.html 을 그대로 씁니다 (주소가 바뀌었다면 옛 주소로 열립니다)"
fi

cp index.html start.html config.js qrcode.js bookmarklets.js listgrab.js returnfill.js \
   북마크모음.html 리스트가져오기_설치.html dist/
cp deploy/_headers deploy/robots.txt dist/
echo "dist/ 준비 완료: $(ls dist | wc -l)개 파일"
