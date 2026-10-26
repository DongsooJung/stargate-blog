# 스타게이트 블로그 읽기 앱

글은 네이버 두 곳, Blogger, 티스토리, Notion에 있습니다. 이 앱은 그 글을 모아 읽습니다. 에디터와 수익 카드는 넣지 않습니다. KOI 채점과 상담은 Play 앱 `kr.co.stargateedu.twa`에 둡니다.

## 화면

- 홈: 오늘·누적 방문, 주제 5개, 시간순 20편. 갤럭시 폴드7 접힘(412px)은 한 줄, 펼침(750px 이상)은 두 칸, 984px 이상에서는 목록과 본문이 나란히 있습니다
- 채널: 고정된 8개 채널
- 검색: 제목, 요약, 채널, 주제
- 읽기: Notion, Blogger, 티스토리, 수학 글은 앱 안에서. 네이버 두 곳, YouTube, Instagram은 원문
- 내 기록: 이 기기의 북마크와 새 글 표시, 방문 수. 좋아요·설문·자유게시판은 웹 허브로 이어 갑니다

## 목록 다시 만들기

```bash
python3 scripts/build_feed.py
python3 -m unittest discover -s tests -p 'test_feed.py' -v
```

`scripts/build_feed.py`가 만드는 `feed.json`이 1단계 계약입니다. 허브 빌더가 같은 파일을 `https://blog.stargateedu.co.kr/feed.json`에 올리면 앱은 그 파일을 먼저 읽고, 없으면 앱 안의 파일을 사용합니다.

## 배포

별도 빌드나 서버가 없습니다. 이 저장소 Pages는 `main`의 `/`를 `blog.stargateshop.co.kr`로 게시합니다. `main`에 머지되면 다음 주소로 열립니다.

`https://blog.stargateshop.co.kr/app/`

공개 브랜드 주소는 `https://blog.stargateedu.co.kr/app/` 입니다. Play 패키지는 `android/`의 `kr.co.stargateedu.blog`이고, 스토어 문구는 `store/play-listing.md`입니다. 자산 링크 초안은 `.well-known/assetlinks.json`입니다. Play 앱 서명 인증서의 SHA-256이 나온 뒤 그 지문을 채워야 도메인 검증이 끝납니다. 허브 저장소에 같은 파일을 넣어야 `blog.stargateedu.co.kr`에서 제공됩니다.

오늘·누적 방문의 실시간 조회는 워커가 `blog.stargateedu.co.kr` 출처만 허용합니다. 다른 주소에서는 목록을 만들 때 저장한 스냅샷을 보여 줍니다. 허브와 같은 주소에서 실시간 숫자를 보려면 `app/` 디렉터리를 `stargate-blog-hub`에 넣어 `https://blog.stargateedu.co.kr/app/`로 열면 됩니다.

로컬 확인:

```bash
python3 -m http.server 4173
```

브라우저에서 `http://127.0.0.1:4173/app/`를 엽니다.
