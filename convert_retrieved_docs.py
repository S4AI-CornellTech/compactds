import json
import re
import os
import argparse

TOP_K_CTXS = 5

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

    parser = argparse.ArgumentParser(description="Convert retrieved docs in a folder to plaintext JSON format.")
    parser.add_argument("--input-dir", type=str, help="Input folder containing .json files")
    parser.add_argument("--output-dir", type=str, help="Output folder for converted .json files")
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)
    input_files = [f for f in os.listdir(args.input_dir) if f.endswith('.json')]
    if not input_files:
        print(f"No .json files found in {args.input_dir}")
        return

    k_pattern = re.compile(r'_k_(\d+)_retrieved_doc_ids')
    for fname in input_files:
        in_path = os.path.join(args.input_dir, fname)
        # Change output name to _retrieved_doc_text.json
        if fname.endswith('_retrieved_doc_ids.json'):
            out_name = fname.replace('_retrieved_doc_ids.json', '_retrieved_doc_text.json')
        else:
            out_name = os.path.splitext(fname)[0] + "_retrieved_doc_text.json"
        out_path = os.path.join(args.output_dir, out_name)
        # Extract k from filename (required)
        match = k_pattern.search(fname)
        top_k_ctxs = int(match.group(1))
        n = convert_one_file(in_path, out_path, top_k_ctxs)
        print(f"[OK] {in_path} -> {out_path} (k={top_k_ctxs}, {n} items)")

if __name__ == "__main__":
    main()
