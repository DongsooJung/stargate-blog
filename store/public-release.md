# 공개 게시 준비

개발자 계정은 새로 만들지 않습니다. `kr.co.stargateedu.twa` 를 올린 기존 Play 계정에 앱을 추가합니다.

- 개발자 표시 이름: STARGATE
- 공개 메일: ceo@stargateedu.co.kr
- 법인명: 주식회사 별의문
- 개인정보처리방침: https://stargateedu.co.kr/privacy.html (2026-10-15)
- 패키지: kr.co.stargateedu.blog
- 시작 주소: https://blog.stargateedu.co.kr/app/
- 미리보기: https://blog.stargateshop.co.kr/app/

콘솔에 붙여 넣을 문구, 데이터 안전 답, 전체이용가 답은 `store/play-listing.md`에 있습니다.

## 화면

갤럭시 폴드7 접힘은 412×960, 펼침은 750×832 또는 984×1092입니다. 접힘에서는 글이 한 줄이고, 750px 이상에서는 두 칸, 900px 이상이면서 높이가 700px 이상이면 목록과 본문이 나란히 있습니다.

참고 캡처:

- `store/screenshots/04-fold7-cover.png`
- `store/screenshots/05-fold7-open-home.png`
- `store/screenshots/06-fold7-open-read.png`

Play에 올리는 전화 스크린샷 3장은 1080×1920이고 `01`부터 `03`입니다.

## 만든 App Bundle

파일은 `store/stargate-blog-1.0.0.aab`입니다. 2026-10-27 22:28 KST에 Bubblewrap 1.22.0으로 만들었습니다.

- 패키지: `kr.co.stargateedu.blog`
- 버전: 1.0.0 (versionCode 1)
- 시작 주소: `https://blog.stargateedu.co.kr/app/`
- 화면 방향: any
- SHA-256: `07a39666c321205e887f1eecbe76c32197b01527e1752bd9b3635742d8bf0a06`
- 빌드에 쓴 매니페스트: `store/twa-manifest.json`

서명 키는 이 저장소에 없습니다. 업로드 키 저장소와 비밀번호는 Google Drive의 `stargate-blog-upload.keystore`, `스타게이트 블로그 업로드 키.txt`에 있습니다. 업로드 인증서 SHA-256은 `8E:4B:84:DE:24:E9:F6:1E:69:95:F3:76:70:6B:DB:C2:6C:5E:19:2A:C6:BF:2B:7A:5A:20:79:C4:44:4A:DE:AD`입니다. assetlinks에 넣을 값은 Play Console의 앱 서명 인증서 SHA-256입니다.

`https://blog.stargateedu.co.kr/app/`는 2026-10-27 22:33 KST 기준으로 404입니다. 아이콘과 웹 매니페스트는 빌드할 때 GitHub raw 주소에서 받았습니다. 앱이 여는 주소는 블로그 도메인입니다.

## 콘솔에서 이어서 할 일

1. 기존 개발자 계정에서 앱을 만듭니다. 패키지 이름은 `kr.co.stargateedu.blog`입니다.
2. 프로덕션 트랙의 버전 수정 화면에서 `store/stargate-blog-1.0.0.aab`를 업로드합니다.
3. Play 앱 서명 인증서의 SHA-256을 `.well-known/assetlinks.json`에 넣습니다. 지금은 빈 배열입니다. `kr.co.stargateedu.twa`의 지문은 그대로 둡니다.
4. 그 자산 링크를 `blog.stargateedu.co.kr` 루트에 둡니다. 이 계정의 토큰으로는 `stargate-blog-hub`에 푸시하지 못합니다.
5. `app/`과 `feed.json`을 허브에 넣어 `https://blog.stargateedu.co.kr/app/`에서 열리게 합니다. 방문 수 실시간 조회는 그 출처만 허용합니다.
6. 스토어 등록 정보를 `store/play-listing.md`대로 채웁니다. 업로드가 끝나면 미리보기, 확인, 검토 전송을 이어서 합니다.
