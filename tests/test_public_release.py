import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class PublicRelease(unittest.TestCase):
    def test_asset_links_name_the_blog_package(self):
        payload = json.loads((ROOT / ".well-known" / "assetlinks.json").read_text(encoding="utf-8"))
        target = payload[0]["target"]
        self.assertEqual(target["namespace"], "android_app")
        self.assertEqual(target["package_name"], "kr.co.stargateedu.blog")
        self.assertIn("delegate_permission/common.handle_all_urls", payload[0]["relation"])

    def test_store_listing_uses_the_public_identity(self):
        text = (ROOT / "store" / "play-listing.md").read_text(encoding="utf-8")
        self.assertIn("STARGATE", text)
        self.assertIn("ceo@stargateedu.co.kr", text)
        self.assertIn("주식회사 별의문", text)
        self.assertIn("kr.co.stargateedu.blog", text)
        self.assertIn("https://blog.stargateedu.co.kr/app/", text)
        self.assertIn("kr.co.stargateedu.twa", text)

    def test_twa_opens_the_brand_origin(self):
        manifest = (ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml").read_text(encoding="utf-8")
        gradle = (ROOT / "android" / "app" / "build.gradle").read_text(encoding="utf-8")
        strings = (ROOT / "android" / "app" / "src" / "main" / "res" / "values" / "strings.xml").read_text(encoding="utf-8")
        self.assertIn("kr.co.stargateedu.blog", gradle)
        self.assertIn("blog.stargateedu.co.kr", manifest)
        self.assertIn('android:pathPrefix="/app/"', manifest)
        self.assertIn("https://blog.stargateedu.co.kr/app/", strings)


if __name__ == "__main__":
    unittest.main()
