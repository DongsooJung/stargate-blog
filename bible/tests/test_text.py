import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TEXT = (ROOT / "www" / "text.js").read_text(encoding="utf-8")
DATA = json.loads(TEXT.removeprefix("window.KRV=").rstrip().rstrip(";"))
BOOKS = {book["i"]: book for book in DATA["books"]}


def verse(book, chapter, number):
    for item in BOOKS[book]["c"][chapter - 1]:
        if item["n"] == str(number):
            return item["t"]
    raise AssertionError(f"{book} {chapter}:{number}")


class BibleText(unittest.TestCase):
    def test_canon_shape(self):
        self.assertEqual(len(DATA["books"]), 66)
        self.assertEqual(sum(len(book["c"]) for book in DATA["books"]), 1189)
        self.assertEqual(BOOKS["gen"]["n"], "창세기")
        self.assertEqual(len(BOOKS["gen"]["c"]), 50)
        self.assertEqual(len(BOOKS["psa"]["c"]), 150)
        self.assertEqual(len(BOOKS["rev"]["c"]), 22)
        self.assertEqual(DATA["work"], "성경전서 개역한글판")

    def test_known_verses_keep_the_1961_wording(self):
        self.assertEqual(verse("gen", 1, 1), "태초에 하나님이 천지를 창조하시니라")
        self.assertEqual(
            verse("jhn", 3, 16),
            "하나님이 세상을 이처럼 사랑하사 독생자를 주셨으니 이는 저를 믿는 자마다 멸망치 않고 영생을 얻게 하려 하심이니라",
        )
        self.assertEqual(verse("psa", 23, 1), "여호와는 나의 목자시니 내가 부족함이 없으리로다")
        self.assertEqual(verse("mat", 18, 11), "(없음)")
        self.assertTrue(verse("gen", 2, 12).startswith("그 땅의 금은 정금이요"))
        self.assertNotIn("진주", verse("gen", 2, 12))

    def test_joined_and_absent_numbers_stay_intact(self):
        labels = [item["n"] for item in BOOKS["isa"]["c"][29]]
        self.assertEqual(labels[0], "1-2")
        absent = [
            item["t"]
            for book in DATA["books"]
            for chapter in book["c"]
            for item in chapter
            if item["t"] == "(없음)"
        ]
        self.assertGreaterEqual(len(absent), 10)

    def test_no_markup_or_other_translation_names(self):
        for book in DATA["books"]:
            for chapter in book["c"]:
                for item in chapter:
                    self.assertNotIn("<", item["t"])
                    self.assertNotIn("&nbsp;", item["t"])
                    self.assertNotIn("개역개정", item["t"])

    def test_boot_is_genesis_one(self):
        boot = json.loads(
            (ROOT / "www" / "boot.js").read_text(encoding="utf-8").removeprefix("window.KRV_BOOT=").rstrip().rstrip(";")
        )
        self.assertEqual(boot["title"], "창세기 1장")
        self.assertIn("태초에 하나님이 천지를 창조하시니라", boot["html"])
        self.assertIn('id="v-1"', boot["html"])
