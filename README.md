# ⚠️ Legacy repository

> Replaced by [DongsooJung/stargate-blog-hub](https://github.com/DongsooJung/stargate-blog-hub).  
> Do not edit or deploy this repository as the current blog. Production: [blog.stargateedu.co.kr](https://blog.stargateedu.co.kr/)

The content below is retained for historical reference. The root page stays the old landing.

## 읽기 앱

`app/`은 글을 쓰는 곳이 아닙니다. 네이버, Blogger, 티스토리, Notion에 있는 글을 한 목록으로 읽습니다. 루트 `index.html`은 바꾸지 않습니다.

목록은 `python3 scripts/build_feed.py`가 `app/feed.json`으로 만듭니다. 새 서버는 없습니다. 이 저장소의 GitHub Pages는 `main` 루트를 게시하므로, 머지되면 `https://blog.stargateshop.co.kr/app/`에서 열 수 있습니다. 배포 순서는 `app/README.md`에 있습니다.

---

# STARGATE 블로그

blog.stargateshop.co.kr 정적 사이트 (GitHub Pages 호스팅).

## 구성
- `index.html` — 페이지 본문
- `스타게이트 통합 네비.css` — 공통 디자인 (3사이트 동일)
- `스타게이트 통합 네비.js` — 헤더·푸터·Cross-link 자동 주입
- `CNAME` — GitHub Pages 커스텀 도메인 (`blog.stargateshop.co.kr`)
- `.nojekyll` — Jekyll 처리 비활성화

## 수정·재배포
1. `index.html` 편집
2. `git commit -am "콘텐츠 업데이트"`
3. `git push` → 1\~2분 내 자동 반영

## 운영
주식회사 별의문 (Stargate Corporation) · ceo@stargateedu.co.kr
