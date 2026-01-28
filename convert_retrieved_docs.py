import json
import re
import os

# ===== Settings =====
INPUT_JSONL = "results/retrieved_results/_IVFPQ.65536.64.1/triviaqa::olmes_q_retrieved_results.jsonl"
OUTPUT_JSON = "results/retrieved_results/_IVFPQ.65536.64.1/triviaqa::olmes_q_retrieved_results::_IVFPQ.65536.64.1.k5.json"
TOP_K_CTXS  = 5
# ======================

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
            if not isinstance(ctxs, list) or not ctxs:
                continue

            use_ctxs = ctxs if top_k_ctxs is None else ctxs[:top_k_ctxs]
            texts = []

            for c in use_ctxs:
                if isinstance(c, dict):
                    t = get_retrieval_text(c)
                    if t:
                        texts.append(to_plaintext(t))

            if not texts:
                continue

            count += 1
            if not first:
                fout.write(",\n")
            first = False

            fout.write(f'  "{count}": ')
            fout.write(json.dumps(" ".join(texts), ensure_ascii=False))

        fout.write("\n}\n")

    return count

def main():
    n = convert_one_file(INPUT_JSONL, OUTPUT_JSON, TOP_K_CTXS)
    print(f"[OK] {INPUT_JSONL} -> {OUTPUT_JSON} ({n} items)")

if __name__ == "__main__":
    main()
