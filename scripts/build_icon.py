#!/usr/bin/env python3
"""별의문 런처 표시. 크림 바탕, 먹색 테두리, 다섯 꼭지 별."""

import math
import struct
import zlib
from pathlib import Path

INK = (28, 25, 21)
PAPER = (244, 241, 234)
ROOT = Path(__file__).resolve().parents[1]


def star_polygon(cx, cy, outer, inner, points=5):
    polygon = []
    for index in range(points * 2):
        radius = outer if index % 2 == 0 else inner
        angle = -math.pi / 2 + index * math.pi / points
        polygon.append((cx + radius * math.cos(angle), cy + radius * math.sin(angle)))
    return polygon


def inside(x, y, polygon):
    hit = False
    previous = len(polygon) - 1
    for index, (xi, yi) in enumerate(polygon):
        xj, yj = polygon[previous]
        crosses = (yi > y) != (yj > y)
        if crosses and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
            hit = not hit
        previous = index
    return hit


def color_at(x, y, size):
    frame = size * 0.07
    if x < frame or y < frame or x >= size - frame or y >= size - frame:
        return INK
    center = (size - 1) / 2
    polygon = star_polygon(center, center, size * 0.30, size * 0.125)
    return INK if inside(x, y, polygon) else PAPER


def render(size, samples=4):
    rows = []
    for y in range(size):
        row = []
        for x in range(size):
            total = [0, 0, 0]
            for sy in range(samples):
                for sx in range(samples):
                    color = color_at(x + (sx + 0.5) / samples, y + (sy + 0.5) / samples, size)
                    total[0] += color[0]
                    total[1] += color[1]
                    total[2] += color[2]
            count = samples * samples
            row.append(tuple(channel // count for channel in total))
        rows.append(row)
    return rows


def write_png(path: Path, rows) -> None:
    height = len(rows)
    width = len(rows[0])
    raw = bytearray()
    for row in rows:
        raw.append(0)
        for red, green, blue in row:
            raw.extend((red, green, blue))
    compressed = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    header = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", compressed) + chunk(b"IEND", b""))


def main() -> None:
    targets = [
        (ROOT / "app" / "icon-192.png", 192),
        (ROOT / "app" / "icon-512.png", 512),
        (ROOT / "android" / "app" / "src" / "main" / "res" / "drawable" / "ic_launcher.png", 192),
    ]
    cache = {}
    for path, size in targets:
        rows = cache.setdefault(size, render(size))
        write_png(path, rows)
        print(f"wrote {path} {size}x{size}")


if __name__ == "__main__":
    main()
