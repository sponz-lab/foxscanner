#!/usr/bin/env python3
"""북마크모음.html 을 만든다.

북마크릿은 주소를 안에 품고 있어서, 호스팅 주소가 바뀌면 옛 주소로 열린다.
그래서 배포할 때마다 이 파일을 다시 만든다.

    python3 scripts/make-bookmarks.py https://example.pages.dev/

주소를 주지 않으면 환경변수 SITE_URL 을 쓰고, 그것도 없으면 build.sh 가
경고만 남기고 기존 파일을 그대로 둔다.
"""
import html
import json
import os
import re
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def bookmarklet(code: str) -> str:
    return "javascript:" + urllib.parse.quote(code, safe="")


def main() -> int:
    site = (sys.argv[1] if len(sys.argv) > 1 else os.environ.get("SITE_URL", "")).strip()
    if not site:
        print("make-bookmarks: 주소가 없어 건너뜁니다 (SITE_URL 또는 인자로 주세요)")
        return 0
    if not site.endswith("/"):
        site += "/"
    if not site.startswith("http"):
        print(f"make-bookmarks: 주소가 http(s) 로 시작해야 합니다 — {site}")
        return 1

    src = (ROOT / "bookmarklets.js").read_text(encoding="utf-8")
    try:
        bm_list = json.loads(re.search(r'window\.BM_LIST = (".*?");\n', src, re.S).group(1))
        bm_return = json.loads(re.search(r'window\.BM_RETURN = (".*?");\n', src, re.S).group(1))
    except (AttributeError, json.JSONDecodeError) as e:
        print(f"make-bookmarks: bookmarklets.js 를 읽지 못했습니다 — {e}")
        return 1

    app = site + "index.html"
    start = site + "start.html"
    if "__APP_URL__" not in bm_list:
        print("make-bookmarks: BM_LIST 에 __APP_URL__ 자리가 없습니다")
        return 1
    bm_list = bm_list.replace("__APP_URL__", app)

    doc = f"""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- 입고 검수 북마크 모음. 크롬·엣지에서 '북마크 가져오기'로 한 번에 설치됩니다.
     주소: {html.escape(site)} -->
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks</H1>
<DL><p>
    <DT><H3>입고 검수</H3>
    <DL><p>
        <DT><A HREF="{html.escape(start)}">0. 설치와 사용법</A>
        <DT><A HREF="{html.escape(app)}">1. 검수 프로그램</A>
        <DT><A HREF="{html.escape(bookmarklet(bm_list))}">2. 리스트 가져오기</A>
        <DT><A HREF="{html.escape(bookmarklet(bm_return))}">3. 전산에 입력하기</A>
    </DL><p>
</DL><p>
"""
    out = ROOT / "북마크모음.html"
    out.write_text(doc, encoding="utf-8")
    print(f"make-bookmarks: {out.name} 를 {site} 기준으로 다시 만들었습니다")
    return 0


if __name__ == "__main__":
    sys.exit(main())
