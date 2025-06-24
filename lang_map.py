# lang_map.py
import random

def generate_language_map():
    charset = []
    blocks = [
        range(0x0900, 0x0900 + 200),   # Devanagari
        range(0x4E00, 0x4E00 + 1000),  # Chinese Hanzi
        range(0x0B80, 0x0B80 + 200),   # Tamil
        range(0x0370, 0x0370 + 100),   # Greek
        range(0x0590, 0x0590 + 100),   # Hebrew
        range(0x0E00, 0x0E00 + 100),   # Thai
        range(0xAC00, 0xAC00 + 300),   # Korean Hangul
        range(0x0600, 0x0600 + 100),   # Arabic
        range(0x0400, 0x0400 + 100),   # Cyrillic
    ]

    for block in blocks:
        for cp in block:
            ch = chr(cp)
            if ch not in charset:
                charset.append(ch)
            if len(charset) == 256:
                break
        if len(charset) == 256:
            break

    # Ensure exactly 256 unique characters (one per byte)
    charset = charset[:256]
    return {str(i): charset[i] for i in range(256)}
