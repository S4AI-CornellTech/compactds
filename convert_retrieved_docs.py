import json
import re
import os
import glob
from typing import List

# Settings
INPUT_DIR    = "output/retrieved_results/_IVFPQ.65536.64.32"
OUTPUT_DIR   = "output/retrieved_results/_IVFPQ.65536.64.32/converted"
TOP_K_CTXS   = 5

# Utils
def to_plaintext(s: str) -> str:
    if s is None:
        return ""
    s = re.sub(r"\s+", " ", s)
    return s.strip()

def get_retrieval_text(item: dict) -> str:
    for key in ["retrieval text", "retrieval_text", "text"]:
        v = item.get(key)
        if isinstance(v, str):
            return v
    return ""

def convert_one_file(in_path: str, out_path: str, top_k_ctxs=TOP_K_CTXS) -> int:
    count = 0
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    with open(in_path, "r", encoding="utf-8") as fin, \
         open(out_path, "w", encoding="utf-8") as fout:

        fout.write("{\n")
        first = True

        for line in fin:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue

            ctxs = row.get("ctxs", [])
            if not isinstance(ctxs, list) or len(ctxs) == 0:
                continue

            use_ctxs = ctxs if top_k_ctxs is None else ctxs[:top_k_ctxs]
            texts = []
            for c in use_ctxs:
                if isinstance(c, dict):
                    t = get_retrieval_text(c)
                    if t:
                        texts.append(to_plaintext(t))
            texts = [t for t in texts if t]
            concat_text = " ".join(texts)

            count += 1
            key = str(count)

            if not first:
                fout.write(",\n")
            first = False
            fout.write(f'  "{key}": ')
            fout.write(json.dumps(concat_text, ensure_ascii=False))

        fout.write("\n}\n")

    return count

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    in_files: List[str] = sorted(glob.glob(os.path.join(INPUT_DIR, "**", "*.jsonl"), recursive=True))
    if not in_files:
        print(f"No .jsonl files found in: {INPUT_DIR}")
        return

    total_files = 0
    total_items = 0

    for in_path in in_files:
        base = os.path.basename(in_path)
        name, _ = os.path.splitext(base)
        out_path = os.path.join(OUTPUT_DIR, f"{name}.json")

        n = convert_one_file(in_path, out_path, TOP_K_CTXS)
        total_files += 1
        total_items += n
        print(f"[OK] {in_path} -> {out_path}  ({n} items)")

    print(f"\nDone. Converted {total_files} files, {total_items} total items.")

if __name__ == "__main__":
    main()
