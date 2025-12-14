  python -m src.main_ric --config-name CompactDS \
    tasks.eval.search=true \
    tasks.eval.task_name=lm-eval \
    evaluation.data.eval_data=queries/triviaqa::olmes_q.jsonl \
    +evaluation.search.cache_query_embedding=true \
    +evaluation.search.cache_query_embedding_only=true \
    +evaluation.search.query_embedding_save_path=datastores/compactds/embeddings/triviaqa_olmes_q_embeddings.npy 
