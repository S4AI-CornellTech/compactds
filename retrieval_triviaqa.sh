#!/bin/bash

if [ "$#" -ne 4 ]; then
  echo "Usage: bash $0 compactds_base_path output_dir \"nprobe_list\" \"n_docs_list\""
  echo "Example: bash $0 /path/to/compactds /path/to/output_dir \"8 16 32 64\" \"5 10 20 50\""
  exit 1
fi

compactds_base_path="$1"
output_dir="$2"
read -a nprobe_list <<< "$3"
read -a n_docs_list <<< "$4"

for p in "${nprobe_list[@]}"; do
  for n_docs in "${n_docs_list[@]}"; do
    python -m src.main_ric --config-name CompactDS \
      tasks.eval.search=true \
      datastore.embedding.passages_dir="$compactds_base_path/passages" \
      datastore.embedding.embedding_dir="$compactds_base_path/embeddings" \
      tasks.eval.task_name=lm-eval \
      evaluation.data.eval_data=../compactds_queries/triviaqa::olmes_q.jsonl \
      evaluation.eval_output_dir="$output_dir" \
      evaluation.search.n_docs=$n_docs \
      datastore.index.probe=$p
  done
done
