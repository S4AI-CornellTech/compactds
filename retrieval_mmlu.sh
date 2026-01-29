#!/bin/bash

if [ "$#" -ne 5 ]; then
  echo "Usage: bash $0 compactds_base_path queries_path output_dir \"nprobe_list\" \"n_docs_list\""
  echo "Example: bash $0 /path/to/compactds /path/to/queries /path/to/output_dir \"1 32 64 128 256 512\" \"5 10 20 50\""
  exit 1
fi

compactds_base_path="$1"
queries_path="$2"
output_dir="$3"
read -a nprobe_list <<< "$4"
read -a n_docs_list <<< "$5"

FILES=$(ls "$queries_path"/mmlu/*.jsonl | sort)

for p in "${nprobe_list[@]}"; do
  echo "==== Starting runs for probe=$p ===="
  for n_docs in "${n_docs_list[@]}"; do
    for file in $FILES; do
      base="$(basename "$file")"
      name="${base%.jsonl}"
      echo "[probe=$p, n_docs=$n_docs] Running eval with $file ..."
      python -m src.main_ric \
        --config-name CompactDS \
        tasks.eval.search=true \
        datastore.embedding.passages_dir="$compactds_base_path/passages" \
        datastore.embedding.embedding_dir="$compactds_base_path/embeddings" \
        tasks.eval.task_name=lm-eval \
        evaluation.data.eval_data="$file" \
        evaluation.eval_output_dir="$output_dir" \
        evaluation.search.n_docs=$n_docs \
        datastore.index.probe="$p"
    done
  done
done

echo "All runs finished."