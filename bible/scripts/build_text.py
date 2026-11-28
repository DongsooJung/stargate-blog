#!/usr/bin/env python3
"""개역한글 본문을 받아 앱 데이터로 만든다.

저작재산권이 끝난 『성경전서 개역한글판』 본문만 담는다.
난외주, 각주 풀이, 소제목은 본문이 아니므로 넣지 않는다.
절 번호가 붙어 있으면 「1-2」로 두고, 본문이 「(없음)」인 절은 그대로 둔다.
"""

from __future__ import annotations

import html
import json
import re
import ssl
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WWW = ROOT / "www"
CACHE = Path("/tmp/krv-han-html")
READER = "https://www.bskorea.or.kr/bible/korbibReadpage.php?version=HAN&book={book}&chap={chap}"

# 대한성서공회 개역한글 책 코드와 이름, 약칭, 장 수.
BOOKS = [
    ("gen", "창세기", "창", 50, "구약"),
    ("exo", "출애굽기", "출", 40, "구약"),
    ("lev", "레위기", "레", 27, "구약"),
    ("num", "민수기", "민", 36, "구약"),
    ("deu", "신명기", "신", 34, "구약"),
    ("jos", "여호수아", "수", 24, "구약"),
    ("jdg", "사사기", "삿", 21, "구약"),
    ("rut", "룻기", "룻", 4, "구약"),
    ("1sa", "사무엘상", "삼상", 31, "구약"),
    ("2sa", "사무엘하", "삼하", 24, "구약"),
    ("1ki", "열왕기상", "왕상", 22, "구약"),
    ("2ki", "열왕기하", "왕하", 25, "구약"),
    ("1ch", "역대상", "대상", 29, "구약"),
    ("2ch", "역대하", "대하", 36, "구약"),
    ("ezr", "에스라", "스", 10, "구약"),
    ("neh", "느헤미야", "느", 13, "구약"),
    ("est", "에스더", "에", 10, "구약"),
    ("job", "욥기", "욥", 42, "구약"),
    ("psa", "시편", "시", 150, "구약"),
    ("pro", "잠언", "잠", 31, "구약"),
    ("ecc", "전도서", "전", 12, "구약"),
    ("sng", "아가", "아", 8, "구약"),
    ("isa", "이사야", "사", 66, "구약"),
    ("jer", "예레미야", "렘", 52, "구약"),
    ("lam", "예레미야애가", "애", 5, "구약"),
    ("ezk", "에스겔", "겔", 48, "구약"),
    ("dan", "다니엘", "단", 12, "구약"),
    ("hos", "호세아", "호", 14, "구약"),
    ("jol", "요엘", "욜", 3, "구약"),
    ("amo", "아모스", "암", 9, "구약"),
    ("oba", "오바댜", "옵", 1, "구약"),
    ("jnh", "요나", "욘", 4, "구약"),
    ("mic", "미가", "미", 7, "구약"),
    ("nam", "나훔", "나", 3, "구약"),
    ("hab", "하박국", "합", 3, "구약"),
    ("zep", "스바냐", "습", 3, "구약"),
    ("hag", "학개", "학", 2, "구약"),
    ("zec", "스가랴", "슥", 14, "구약"),
    ("mal", "말라기", "말", 4, "구약"),
    ("mat", "마태복음", "마", 28, "신약"),
    ("mrk", "마가복음", "막", 16, "신약"),
    ("luk", "누가복음", "눅", 24, "신약"),
    ("jhn", "요한복음", "요", 21, "신약"),
    ("act", "사도행전", "행", 28, "신약"),
    ("rom", "로마서", "롬", 16, "신약"),
    ("1co", "고린도전서", "고전", 16, "신약"),
    ("2co", "고린도후서", "고후", 13, "신약"),
    ("gal", "갈라디아서", "갈", 6, "신약"),
    ("eph", "에베소서", "엡", 6, "신약"),
    ("php", "빌립보서", "빌", 4, "신약"),
    ("col", "골로새서", "골", 4, "신약"),
    ("1th", "데살로니가전서", "살전", 5, "신약"),
    ("2th", "데살로니가후서", "살후", 3, "신약"),
    ("1ti", "디모데전서", "딤전", 6, "신약"),
    ("2ti", "디모데후서", "딤후", 4, "신약"),
    ("tit", "디도서", "딛", 3, "신약"),
    ("phm", "빌레몬서", "몬", 1, "신약"),
    ("heb", "히브리서", "히", 13, "신약"),
    ("jas", "야고보서", "약", 5, "신약"),
    ("1pe", "베드로전서", "벧전", 5, "신약"),
    ("2pe", "베드로후서", "벧후", 3, "신약"),
    ("1jn", "요한1서", "요일", 5, "신약"),
    ("2jn", "요한2서", "요이", 1, "신약"),
    ("3jn", "요한3서", "요삼", 1, "신약"),
    ("jud", "유다서", "유", 1, "신약"),
    ("rev", "요한계시록", "계", 22, "신약"),
]

ALIASES = {
    "1jn": ["요한일서", "요한일"],
    "2jn": ["요한이서", "요한이"],
    "3jn": ["요한삼서", "요한삼"],
    "lam": ["예레미야 애가", "애가"],
    "jnh": ["요나"],
    "jhn": ["요한"],
    "1sa": ["삼상", "사무엘상"],
    "2sa": ["삼하", "사무엘하"],
    "1ki": ["왕상"],
    "2ki": ["왕하"],
    "1ch": ["대상"],
    "2ch": ["대하"],
    "1co": ["고전"],
    "2co": ["고후"],
    "1th": ["살전"],
    "2th": ["살후"],
    "1ti": ["딤전"],
    "2ti": ["딤후"],
    "1pe": ["벧전"],
    "2pe": ["벧후"],
    "psa": ["시편"],
    "sng": ["아가", "아"],
}


def fetch(book: str, chap: int) -> str:
    CACHE.mkdir(parents=True, exist_ok=True)
    path = CACHE / f"{book}-{chap}.html"
    if path.exists() and path.stat().st_size > 500:
        return path.read_text(encoding="utf-8")
    url = READER.format(book=book, chap=chap)
    req = urllib.request.Request(url, headers={"User-Agent": "krv-reader-build/1.0"})
    last = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=40, context=ssl.create_default_context()) as res:
                raw = res.read().decode("utf-8", "replace")
            if 'class="number"' not in raw:
                raise RuntimeError("verse markup missing")
            path.write_text(raw, encoding="utf-8")
            return raw
        except Exception as exc:  # noqa: BLE001 — retry network and markup failures
            last = exc
            time.sleep(0.4 * (attempt + 1))
    raise RuntimeError(f"{book} {chap}: {last}")


def plain(fragment: str) -> str:
    fragment = re.sub(r"<div id=['\"]D_[\s\S]*?</div>", "", fragment)
    fragment = re.sub(r"<a\b[^>]*class=comment[\s\S]*?</a>", "", fragment)
    fragment = re.sub(r"<a\b[^>]*>[\s\S]*?</a>", "", fragment)
    fragment = re.sub(r"<br\s*/?>", " ", fragment, flags=re.I)
    fragment = re.sub(r"<[^>]+>", "", fragment)
    fragment = html.unescape(fragment).replace("\xa0", " ")
    fragment = re.sub(r"\s+", " ", fragment).strip()
    return fragment


def parse_chapter(page: str) -> list[dict]:
    start = page.find('id="tdBible1"')
    if start < 0:
        start = page.find('class="number"')
    chunk = page[start:]
    chunk = re.sub(r"<font class=\"smallTitle\">[\s\S]*?</font>", "", chunk)
    matches = re.findall(
        r'<span class="number">\s*([0-9]+(?:-[0-9]+)?)\s*(?:&nbsp;|\s)*</span>(.*?)</span>',
        chunk,
        flags=re.S,
    )
    verses = []
    for label, body in matches:
        text = plain(body)
        if not text:
            raise RuntimeError(f"empty verse {label}")
        verses.append({"n": label, "t": text})
    if not verses:
        raise RuntimeError("no verses parsed")
    return verses


def chapter_html(verses: list[dict]) -> str:
    parts = []
    for verse in verses:
        parts.append(
            f'<p class="v" id="v-{verse["n"]}"><sup>{escape(verse["n"])}</sup>{escape(verse["t"])}</p>'
        )
    return "".join(parts)


def escape(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build() -> dict:
    jobs = [(book, name, abbr, testament, chap) for book, name, abbr, count, testament in BOOKS for chap in range(1, count + 1)]
    found: dict[tuple[str, int], list[dict]] = {}
    errors = []
    with ThreadPoolExecutor(max_workers=8) as pool:
        future_map = {
            pool.submit(fetch, book, chap): (book, chap)
            for book, _name, _abbr, _testament, chap in jobs
        }
        done = 0
        for future in as_completed(future_map):
            book, chap = future_map[future]
            done += 1
            try:
                found[(book, chap)] = parse_chapter(future.result())
            except Exception as exc:  # noqa: BLE001
                errors.append(f"{book} {chap}: {exc}")
            if done % 100 == 0 or done == len(jobs):
                print(f"fetched {done}/{len(jobs)}", file=sys.stderr)
    if errors:
        raise SystemExit("\n".join(errors[:20]))

    books = []
    for book, name, abbr, count, testament in BOOKS:
        chapters = []
        for chap in range(1, count + 1):
            chapters.append(found[(book, chap)])
        item = {
            "i": book,
            "n": name,
            "a": abbr,
            "g": testament,
            "c": chapters,
        }
        extra = ALIASES.get(book)
        if extra:
            item["k"] = extra
        books.append(item)
    return {
        "v": 1,
        "work": "성경전서 개역한글판",
        "publisher": "대한성서공회",
        "published": "1961-07-10",
        "note": "난외주와 소제목은 빼었다. 절이 붙어 있으면 번호도 붙여 적었다.",
        "books": books,
    }


def write_outputs(data: dict) -> None:
    WWW.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    (WWW / "bible.json").write_text(payload, encoding="utf-8")
    (WWW / "text.js").write_text("window.KRV=" + payload + ";\n", encoding="utf-8")
    genesis = data["books"][0]["c"][0]
    boot = {
        "v": 1,
        "title": "창세기 1장",
        "id": "gen",
        "ch": 1,
        "html": chapter_html(genesis),
    }
    (WWW / "boot.js").write_text(
        "window.KRV_BOOT=" + json.dumps(boot, ensure_ascii=False, separators=(",", ":")) + ";\n",
        encoding="utf-8",
    )
    verses = sum(len(ch) for book in data["books"] for ch in book["c"])
    print(f"books {len(data['books'])} chapters {sum(len(b['c']) for b in data['books'])} verses {verses}")


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        data = json.loads((WWW / "bible.json").read_text(encoding="utf-8"))
        write_outputs(data)
        return
    write_outputs(build())


if __name__ == "__main__":
    main()
