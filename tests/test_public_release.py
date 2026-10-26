import json
import struct
import unittest
import zlib
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
        self.assertIn("앱이 사용자 데이터를 수집하거나 공유하나요: 아니요.", text)
        self.assertIn("전체이용가", text)
        self.assertIn("SHA-256은 비어 있습니다", text)
        for name in ("01-home-posts.png", "02-article.png", "03-channels.png"):
            width, height = png_size(ROOT / "store" / "screenshots" / name)
            self.assertEqual((width, height), (1080, 1920))

    def test_twa_opens_the_brand_origin(self):
        manifest = (ROOT / "android" / "app" / "src" / "main" / "AndroidManifest.xml").read_text(encoding="utf-8")
        gradle = (ROOT / "android" / "app" / "build.gradle").read_text(encoding="utf-8")
        strings = (ROOT / "android" / "app" / "src" / "main" / "res" / "values" / "strings.xml").read_text(encoding="utf-8")
        self.assertIn("kr.co.stargateedu.blog", gradle)
        self.assertIn("blog.stargateedu.co.kr", manifest)
        self.assertIn('android:pathPrefix="/app/"', manifest)
        self.assertIn("https://blog.stargateedu.co.kr/app/", strings)

    def test_launcher_icon_is_a_star_on_paper(self):
        for name, size in (("icon-192.png", 192), ("icon-512.png", 512)):
            rows = png_rows(ROOT / "app" / name)
            self.assertEqual(len(rows), size)
            self.assertEqual(len(rows[0]), size)
            self.assertLess(luma(rows[size // 2][size // 2]), 80)
            self.assertGreater(luma(rows[int(size * 0.16)][size // 2]), 180)
            self.assertLess(luma(rows[2][2]), 80)
        launcher = png_rows(ROOT / "android" / "app" / "src" / "main" / "res" / "drawable" / "ic_launcher.png")
        self.assertEqual(len(launcher), 192)
        self.assertEqual(launcher[96][96], png_rows(ROOT / "app" / "icon-192.png")[96][96])


def png_size(path):
    data = path.read_bytes()
    if data[12:16] != b"IHDR":
        raise AssertionError(path.name)
    return struct.unpack(">II", data[16:24])


def png_rows(path):
    data = path.read_bytes()
    width, height = png_size(path)
    body = bytearray()
    index = 8
    while index < len(data):
        length = struct.unpack(">I", data[index : index + 4])[0]
        tag = data[index + 4 : index + 8]
        chunk = data[index + 8 : index + 8 + length]
        if tag == b"IDAT":
            body.extend(chunk)
        index += 12 + length
    raw = zlib.decompress(bytes(body))
    stride = width * 3
    rows = []
    cursor = 0
    for _ in range(height):
        if raw[cursor] != 0:
            raise AssertionError(path.name)
        cursor += 1
        row = [tuple(raw[cursor + column * 3 : cursor + column * 3 + 3]) for column in range(width)]
        rows.append(row)
        cursor += stride
    return rows


def luma(pixel):
    red, green, blue = pixel
    return (red + green + blue) / 3


if __name__ == "__main__":
    unittest.main()
