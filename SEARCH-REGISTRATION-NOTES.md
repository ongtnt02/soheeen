# 소희엔 검색 등록 진행 메모 (2026-11-20)

## 완료
- 사이트 SEO·OG: 5개 페이지 canonical/OG/Twitter, `og-image.png`(1200×630), `robots.txt`, `sitemap.xml`
  - 커밋 `5d6558d`, `7776741` (README), 저장소 `ongtnt02/soheeen` main
- 구글 서치 콘솔: 속성 `https://ongtnt02.github.io/soheeen/` 추가·소유확인(HTML 파일 `googleab1a4b36e6d73faa.html`, 커밋 `7f546a6`)
- 사용자 사이트 루트: `ongtnt02/ongtnt02.github.io` 커밋 `8324c6a`
  - `naver412c25bfa2bf0b163b833dfce2e7f4ab.html`, `robots.txt`, `index.html`(→ `/soheeen/` 안내), `.nojekyll`

## 남은 일 (네이버)
1. `https://searchadvisor.naver.com` → 사이트 관리 → `https://ongtnt02.github.io` 행 **소유확인 진행**
   (HTML 파일 업로드 방식 그대로, [소유확인] → 보안문자 입력)
2. 소유확인 후 → **사이트맵 제출**: `https://ongtnt02.github.io/soheeen/sitemap.xml`
3. **웹 페이지 수집 요청**: `/`, `/about.html`, `/services.html`, `/process.html`, `/contact.html`
4. (선택) 네이버 사이트 최적화 점검에서 og:title/og:image 인식 확인

## 확인 대기
- 구글 사이트맵 상태가 제출 직후 `가져올 수 없음`(발견 0)으로 표시됨.
  파일 자체는 정상(HTTP 200 · `application/xml` · XML 파싱 정상 · Googlebot UA 200). 1~2일 뒤 재확인 필요.
