# 입고 검수 (foxscanner)

매장 입고·반품 검수 웹 앱. 직원이 휴대폰 카메라나 블루투스 스캐너로 바코드를 찍으면, 회사 시스템에서 가져온 상품 리스트와 대조하고 여러 기기의 수량을 실시간으로 합산합니다. 빌드·서버·패키지 의존성이 없는 **순수 정적 사이트**입니다.

## 구성

| 파일 | 역할 |
|---|---|
| `index.html` | 검수 앱 본체 (CSS/JS, QR·ZXing 라이브러리 포함) |
| `start.html` | 매장용 설치 페이지 (휴대폰 QR, PC 북마크) |
| `config.js` | Firebase 설정 (공개값) |
| `listgrab.js` / `returnfill.js` | 회사 시스템에서 리스트를 읽어 오는 / 반품 결과를 입력하는 북마클릿 원본 |
| `bookmarklets.js`, `북마크모음.html` | 위 북마클릿의 배포용 복사본 (**수동 동기화**) |
| `scripts/build.sh` | 배포용 `dist/` 생성 (문서 제외) |
| `deploy/`, `netlify.toml`, `firebase.json` | 호스팅 설정 |

## 로컬 실행

```bash
bash scripts/build.sh
cd dist && python -m http.server 8080   # http://localhost:8080/start.html
```

카메라는 `https` 또는 `localhost` 에서만 동작합니다.

## 배포 (무료 호스팅)

저장소가 비공개라 GitHub Pages(유료)는 쓰지 않습니다. **Cloudflare Pages** 를 권장합니다.

| 설정 | 값 |
|---|---|
| Build command | `bash scripts/build.sh` |
| Build output directory | `dist` |
| Branch | `main` |

push 하면 자동 배포됩니다. Netlify, Firebase Hosting 도 같은 방식입니다. 단계별 안내는 [docs/deploy/배포안내.md](docs/deploy/배포안내.md).

## 문서

[docs/README.md](docs/README.md) 에 목차가 있습니다.

- 매장 직원: [docs/store/](docs/store/)
- 본사 설정·보안: [docs/admin/](docs/admin/)
- 배포: [docs/deploy/](docs/deploy/)
- 개발자: [docs/dev/아키텍처.md](docs/dev/아키텍처.md)

## 배포 전 필수

Firestore 규칙과 App Check 를 켜야 합니다 → [docs/admin/보안안내.md](docs/admin/보안안내.md)
