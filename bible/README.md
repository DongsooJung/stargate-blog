# 개역한글

앱을 열면 성경전서 개역한글판이 바로 보입니다. 처음에는 창세기 1장이고, 다시 열면 이 기기에서 마지막으로 읽던 장입니다. 본문은 앱 안에 있으므로 서버가 없어도 읽습니다.

## 로컬에서 보기

저장소 루트에서:

```bash
python3 -m unittest discover -s bible/tests -p 'test_text.py' -v
python3 -m http.server 4173
```

브라우저에서 `http://127.0.0.1:4173/bible/www/` 를 엽니다.

본문을 다시 만들 때:

```bash
python3 bible/scripts/build_text.py
```

받은 본문의 철자, 절 번호, 「(없음)」, 「1-2」처럼 붙은 번호는 고치지 않습니다. 난외주와 소제목은 넣지 않습니다.

## 안드로이드

플레이용 껍데기는 `bible/android`입니다. 패키지 이름은 `kr.co.stargateedu.bible`이고 targetSdk는 36입니다. 인터넷 권한은 없습니다. 빌드할 때 `www`를 앱 자산으로 복사합니다.

이 환경에는 안드로이드 SDK가 없어 AAB를 만들지 못했습니다. 콘솔 업로드, 서명, 개인정보처리방침 공개 주소는 `CLAUDE.md`의 순서대로 이어서 하면 됩니다.
