for p in 16 128; do
    echo "Running with probe = $p ..."
    for file in $(ls queries/mmlu/*.jsonl | sort); do
        echo "Running eval with $file ..."
        python -m src.main_ric \
            --config-name CompactDS \
            tasks.eval.search=true \
            datastore.embedding.passages_dir=/share5/akiho.kawada/compactds/datastores/compactds/passages/ \
            datastore.index.probe=$p \
            tasks.eval.task_name=lm-eval \
            evaluation.data.eval_data="$file" \
            evaluation.search.n_docs=50 \
        || true
    done
done
