mkdir -p logs

for p in 1 32 64 128 256 512; do
  python -m src.main_ric --config-name CompactDS \
    tasks.eval.search=true \
    datastore.embedding.passages_dir=datastores/compactds/passages \
    datastore.embedding.embedding_dir=datastores/compactds/embeddings \
    tasks.eval.task_name=lm-eval \
    evaluation.data.eval_data=queries/naturalqs::olmes_q.jsonl \
    evaluation.search.n_docs=10 \
    datastore.index.probe=$p \
    | tee logs/run_probe_$p.log || true
done
