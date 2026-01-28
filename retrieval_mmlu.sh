#!/bin/bash

PROBES=("1" "32" "64" "128" "256" "512")
FILES=$(ls queries/mmlu/*.jsonl | sort)


for p in "${PROBES[@]}"; do
  echo "==== Starting runs for probe=$p ===="
  for file in $FILES; do
    base="$(basename "$file")"
    name="${base%.jsonl}"
    echo "[probe=$p] Running eval with $file ..."
    python -m src.main_ric \
      --config-name CompactDS \
      tasks.eval.search=true \
      datastore.embedding.passages_dir=datastores/compactds/passages \
      datastore.embedding.embedding_dir=datastores/compactds/embeddings \
      tasks.eval.task_name=lm-eval \
      evaluation.data.eval_data="$file" \
      evaluation.search.n_docs=10 \
      datastore.index.probe="$p" \
      | tee "logs/run_mmlu_${name}_probe_${p}.log" || true
  done
done

echo "All runs finished."