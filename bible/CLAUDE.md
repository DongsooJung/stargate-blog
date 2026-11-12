# Claude에게 넘기는 일

여기까지는 코드와 본문 데이터를 만들어 두었다. 아래는 이 환경에서 권한이 없거나 도구가 없어 하지 못한 일이다. 저장소를 연 Claude는 이 파일의 순서만 처리한다.

본문 철자, 절 번호, 「(없음)」, 「1-2」 같은 붙은 번호는 고치지 마라. 개역개정, 새번역, 공동번역, YouVersion 본문을 넣지 마라. 패키지 이름 `kr.co.stargateedu.bible`을 바꾸지 마라. 인터넷 권한을 넣지 마라. 블로그 앱 `android/`와 패키지 `kr.co.stargateedu.blog`는 건드리지 마라.

## 이미 되어 있는 것

- `bible/www` : 첫 화면이 창세기 1장인 읽기 앱. 다시 열면 기기에 저장된 마지막 장. 책, 찾기, 글자 크기, 안내.
- `bible/www/text.js` : 66권 1189장. 대한성서공회 개역한글 읽기 화면에서 본문만 옮겼고 난외주와 소제목은 뺐다.
- `bible/android` : WebView 껍데기. targetSdk 36. 빌드 시 `www`를 자산으로 복사한다. 인터넷 권한 없음.
- `bible/www/privacy.html` : 개인정보처리방침 초안.
- `bible/store/play-listing.md` : 콘솔에 붙여 넣을 문구.

확인:

```bash
python3 -m unittest discover -s bible/tests -p 'test_text.py' -v
python3 -m http.server 4173
```

`http://127.0.0.1:4173/bible/www/` 에서 첫 화면 본문, 이전·다음 장, 찾기 `요 3:16`, 비행기 모드에 해당하는 네트워크 차단 뒤 새로고침을 확인한다.

## 1. AAB 만들기

이 환경에는 Android SDK가 없다. Android Studio가 있는 컴퓨터에서 `bible/android`를 연다.

1. SDK 36과 맞는 빌드 도구를 설치한다.
2. `bible/android/build.gradle`의 Android Gradle Plugin이 SDK 36을 받지 못하면, 그 플러그인 버전만 올린다. 앱 코드와 본문은 그대로 둔다.
3. 업로드 키를 새로 만든다. 저장소에 `.jks`를 커밋하지 않는다.
4. `./gradlew :app:bundleRelease`로 AAB를 만든다.
5. 만든 앱을 비행기 모드에서 지웠다가 다시 설치한다. 창세기 1장이 바로 보여야 한다. 요한복음 3장으로 이동한 뒤 앱을 완전히 종료하고 다시 열면 그 장이 보여야 한다. 뒤로 가기는 찾기 창을 닫고, 본문에서는 앱을 종료한다.

## 2. 개인정보처리방침 공개

`bible/www/privacy.html`을 주식회사 별의문 사이트에 올려 누구나 여는 주소로 만든다. 예: `https://stargateedu.co.kr/bible-privacy.html`. 이 저장소의 토큰으로는 그 사이트를 고칠 수 없다. 플레이 콘솔의 개인정보처리방침 칸에는 그 공개 주소를 넣는다.

## 3. 플레이 콘솔

기존 조직 개발자 계정에 새 앱을 만든다.

- 앱 이름: 개역한글
- 패키지: kr.co.stargateedu.bible
- 기본 스토어 언어: 한국어
- 문구, 데이터 안전, 전체이용가 답: `bible/store/play-listing.md`
- 이름과 설명에 「공식」, 「개역개정」을 넣지 않는다.
- 스크린샷 초안은 `bible/store/screenshots`에 있다. 브라우저로 만든 1080×1920 초안이다. 콘솔이 거절하거나 여백이 어색하면 실기기에서 같은 세 화면을 다시 찍어 바꾼다.
- 아이콘은 `bible/www/icon-512.png`.
- 조직 계정에 12명·14일 비공개 테스트 단계가 없으면 내부 테스트 뒤 프로덕션으로 간다. 콘솔에 그 단계가 보이면 콘솔 문구를 따른다.
- 프로덕션 전에 위 1번의 비행기 모드 확인이 끝나 있어야 한다.

## 4. 본문 대조는 종이 성경으로만

디지털 본문은 대한성서공회 개역한글 읽기 화면과 맞게 옮겨 두었다. 종이 『성경전서 개역한글판』과 다르다고 의심되는 절이 있으면, 그 절만 종이책을 보고 고친다. 다른 번역으로 메우지 않는다. 고친 뒤에는 `python3 bible/scripts/build_text.py`로 덮어쓰지 말고, 고친 절을 `text.js`와 `boot.js`에 함께 반영한다. 창세기 1장을 고쳤다면 `boot.js`도 같이 고친다.
