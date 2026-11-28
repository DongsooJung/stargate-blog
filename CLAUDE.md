# 이 저장소에서 할 일

브랜치 `cursor/gaeyeok-hangul-reader-e23d`에서 이어서 한다. 풀 리퀘스트는 https://github.com/DongsooJung/stargate-blog/pull/5 이다. 앱을 처음부터 다시 만들지 않는다.

개역한글 읽기 앱을 구글 플레이에 올릴 수 있는 상태까지 끝낸다. 읽기 화면과 본문, WebView 껍데기, Gradle 8.13 래퍼는 이미 있다. 없는 것은 Android SDK로 만든 AAB, 서명한 업로드, 공개된 개인정보처리방침 주소, 플레이 콘솔 등록이다.

## 지키지 않으면 안 되는 것

- 본문 철자, 절 번호, 「(없음)」, 「1-2」처럼 붙은 번호를 고치지 않는다.
- 개역개정, 새번역, 공동번역, YouVersion 본문을 넣지 않는다.
- 패키지 이름은 `kr.co.stargateedu.bible`이다. 바꾸지 않는다.
- 인터넷 권한을 넣지 않는다.
- 블로그 앱 `android/`, 패키지 `kr.co.stargateedu.blog`, `kr.co.stargateedu.twa`는 건드리지 않는다.
- 업로드 키 `.jks`는 저장소에 커밋하지 않는다.
- 스토어 이름과 설명에 「공식」, 「개역개정」을 넣지 않는다.

## 이미 되어 있는 것

- `bible/www` : 열면 창세기 1장. 다시 열면 이 기기의 마지막 장. 책, 찾기, 글자 크기, 안내. 본문이 바뀌면 저장된 장 HTML 대신 `text.js`로 그 장을 다시 그린다.
- `bible/www/text.js` : 66권 1189장. 대한성서공회 개역한글 읽기 화면의 본문만. 난외주와 소제목은 없다.
- `bible/www/sw.js` : `/bible/www/`처럼 디렉터리 주소로 새로고침해도 오프라인에서 `index.html`을 연다.
- `bible/android` : targetSdk 36. 빌드할 때 `www`를 자산으로 복사한다. `./gradlew`는 Gradle 8.13을 받는다.
- `bible/www/privacy.html` : 개인정보처리방침 초안. 아직 공개 URL이 없다.
- `bible/store/play-listing.md` : 콘솔에 붙여 넣을 문구.
- `bible/store/screenshots/` : 1080×1920 초안 세 장. 브라우저로 만든 것이다.

확인:

```bash
python3 -m unittest discover -s bible/tests -p 'test_text.py' -v
python3 -m http.server 4173
```

`http://127.0.0.1:4173/bible/www/`에서 첫 화면 본문, 이전·다음 장, 찾기 `요 3:16`을 본다.

## 1. AAB

Android SDK 36이 있는 컴퓨터에서 `bible/android`를 연다.

1. SDK 36이 플러그인과 맞지 않으면 `bible/android/build.gradle`의 Android Gradle Plugin 버전만 올린다. 앱 코드와 본문은 그대로 둔다.
2. 업로드 키를 새로 만든다. 저장소에 넣지 않는다.
3. `bible/android`에서 `./gradlew :app:bundleRelease`를 실행한다.
4. 만든 앱을 지웠다가 비행기 모드에서 다시 설치한다. 창세기 1장이 바로 보여야 한다. 요한복음 3장으로 이동한 뒤 완전히 종료하고 다시 열면 그 장이 보여야 한다. 뒤로 가기는 찾기나 책 창을 닫고, 본문에서는 앱을 종료한다.

## 2. 개인정보처리방침

`bible/www/privacy.html`을 주식회사 별의문 사이트에 올려 누구나 여는 주소로 만든다. 예: `https://stargateedu.co.kr/bible-privacy.html`. 이 블로그 저장소만으로는 그 사이트를 고칠 수 없다. 플레이 콘솔에는 그 공개 주소를 넣는다.

## 3. 플레이 콘솔

기존 조직 개발자 계정에 새 앱을 추가한다. 계정을 새로 만들지 않는다.

- 개발자 이름: STARGATE
- 메일: ceo@stargateedu.co.kr
- 앱 이름: 개역한글
- 패키지: kr.co.stargateedu.bible
- 언어: 한국어
- 문구, 데이터 안전, 전체이용가: `bible/store/play-listing.md`를 그대로 옮긴다.
- 아이콘: `bible/www/icon-512.png`
- 스크린샷: `bible/store/screenshots`. 콘솔이 거절하거나 여백이 어색하면 실기기에서 같은 세 화면을 다시 찍는다.
- 조직 계정에 12명·14일 비공개 테스트가 없으면 내부 테스트 뒤 프로덕션으로 간다. 콘솔에 그 단계가 보이면 콘솔 문구를 따른다.
- 프로덕션 전에 1번의 비행기 모드 확인이 끝나 있어야 한다.

## 4. 본문을 고칠 때

종이 『성경전서 개역한글판』과 다른 절만 그 종이책을 보고 고친다. 다른 번역으로 메우지 않는다. `python3 bible/scripts/build_text.py`로 덮어쓰지 않는다. 고친 절은 `bible/www/text.js`에 반영한다. 창세기 1장이면 `bible/www/boot.js`의 첫 화면 HTML도 같이 고친다. 앱은 본문을 읽은 뒤 그 장을 `text.js`로 다시 그리므로, 첫 페인트용 `boot.js`와 본문 파일이 둘 다 맞아야 한다.
