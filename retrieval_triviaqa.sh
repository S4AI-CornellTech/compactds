for p in 16 128; do
  python -m src.main_ric --config-name CompactDS \
    tasks.eval.search=true \
    datastore.embedding.passages_dir=/share5/akiho.kawada/compactds/datastores/compactds/passages/ \
    tasks.eval.task_name=lm-eval \
    evaluation.data.eval_data=queries/naturalqs::olmes_q.jsonl \
    evaluation.search.n_docs=50 \
    datastore.index.probe=$p \
    | tee logs/run_probe_$p.log || true
done