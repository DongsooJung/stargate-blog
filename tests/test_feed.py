import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FEED = json.loads((ROOT / "app" / "feed.json").read_text(encoding="utf-8"))


class FeedContract(unittest.TestCase):
    def test_catalog_shape(self):
        self.assertEqual(len(FEED["channels"]), 8)
        self.assertEqual(len(FEED["topics"]), 5)
        home = [post for post in FEED["posts"] if post["onHome"]]
        self.assertEqual(len(home), 20)
        published = [post["publishedAt"] for post in home]
        self.assertEqual(published, sorted(published, reverse=True))

    def test_read_modes(self):
        home = [post for post in FEED["posts"] if post["onHome"]]
        naver = [post for post in home if post["channelId"].startswith("naver")]
        self.assertTrue(naver)
        self.assertTrue(all(post["read"] == "external" and not post["bodyHtml"] for post in naver))
        inside = [post for post in home if post["channelId"] in {"blogger", "tistory"}]
        self.assertTrue(all(post["read"] == "in-app" and post["bodyHtml"] for post in inside))
        self.assertTrue(all("<script" not in post["bodyHtml"].lower() for post in inside))

    def test_notion_archive_is_in_app_and_stale_file(self):
        notion = [post for post in FEED["posts"] if post["channelId"] == "notion"]
        self.assertEqual(len(notion), 6)
        self.assertEqual(len({post["id"] for post in notion}), 6)
        self.assertTrue(all(post["read"] == "in-app" and post["bodyHtml"] for post in notion))
        self.assertTrue(FEED["notionArchive"]["generatedAt"].startswith("2026-09-12 20:47"))
        self.assertEqual(FEED["hub"]["proposalBaseline"], "2026-10-24 06:04 KST")

    def test_external_channels_and_phase_boundaries(self):
        by_id = {channel["id"]: channel for channel in FEED["channels"]}
        for channel_id in ("youtube", "instagram", "math", "naver-market", "naver-lab"):
            self.assertEqual(by_id[channel_id]["read"], "external")
        self.assertEqual(FEED["daily"]["phase"], 4)
        self.assertIn("kr.co.stargateedu.twa", FEED["web"]["play"])
        self.assertEqual(FEED["publisher"]["name"], "STARGATE")
        self.assertEqual(FEED["publisher"]["email"], "ceo@stargateedu.co.kr")
        self.assertEqual(FEED["web"]["origin"], "https://blog.stargateedu.co.kr/app/")
        statuses = {row["id"]: row["status"] for row in FEED["collection"]["channels"]}
        self.assertEqual(statuses["notion"], "archive")
        self.assertEqual(statuses["youtube"], "origin-only")
        self.assertEqual(FEED["collection"]["missing"], [])
        self.assertEqual(FEED["collection"]["notionStatus"], "unchanged-file")
        self.assertNotIn("editor", json.dumps(FEED, ensure_ascii=False).lower())


if __name__ == "__main__":
    unittest.main()
