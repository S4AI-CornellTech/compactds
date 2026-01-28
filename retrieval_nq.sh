#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: bash $0 \"nprobe_list\" \"n_docs_list\""
  echo "Example: bash $0 \"1 32 64 128 256 512\" \"5 10 20 50\""
  exit 1
fi

read -a nprobe_list <<< "$1"
read -a n_docs_list <<< "$2"

for p in "${nprobe_list[@]}"; do
  for n_docs in "${n_docs_list[@]}"; do
    python -m src.main_ric --config-name CompactDS \
      tasks.eval.search=true \
      datastore.embedding.passages_dir=datastores/compactds/passages \
      datastore.embedding.embedding_dir=datastores/compactds/embeddings \
      tasks.eval.task_name=lm-eval \
      evaluation.data.eval_data=queries/naturalqs::olmes_q.jsonl \
      evaluation.eval_output_dir=/share/suh-scrap/mts247/rag-selector/docids/compactds \
      evaluation.search.n_docs=$n_docs \
      datastore.index.probe=$p
  done
done
