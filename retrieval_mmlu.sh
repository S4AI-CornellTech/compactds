#!/bin/bash

for file in $(ls queries/mmlu/*.jsonl | sort); do
    echo "Running eval with $file ..."
    python -m src.main_ric \
        --config-name CompactDS \
        tasks.eval.search=true \
        datastore.embedding.passages_dir=datastores/compactds/passages \
        datastore.embedding.embedding_dir=datastores/compactds/embeddings \
        tasks.eval.task_name=lm-eval \
        evaluation.data.eval_data="$file" \
        evaluation.search.n_docs=10
done
