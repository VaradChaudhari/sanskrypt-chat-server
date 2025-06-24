# smt_generator.py

import json
import random

def generate_devanagari_map(file_path="devanagari_map.json"):
    devanagari_chars = [chr(cp) for cp in range(0x0900, 0x097F + 1)]
    extended_chars = (devanagari_chars * ((256 // len(devanagari_chars)) + 1))[:256]
    random.shuffle(extended_chars)
    devanagari_map = {str(i): extended_chars[i] for i in range(256)}

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(devanagari_map, f, ensure_ascii=False, indent=2)

    return devanagari_map
