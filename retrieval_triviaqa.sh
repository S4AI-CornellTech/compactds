#!/bin/bash

#SBATCH --job-name rag-selector                         # Job name
#SBATCH --mail-type=ALL                      # Request status by email
#SBATCH --mail-user=mts247@cornell.edu        # Email address to send results to.
#SBATCH --get-user-env
#SBATCH --mem=200G
#SBATCH -t 10000:00:00
#SBATCH --gres=gpu:1
#SBATCH --partition=gupta
#SBATCH --nodelist=yosemite
#SBATCH --cpus-per-task=32

for p in 32; do
  python -m src.main_ric --config-name CompactDS \
    tasks.eval.search=true \
    datastore.embedding.passages_dir=/share/suh-scrap/mts247/rag-selector/indices/compactds/datastore_pq64/passages \
    datastore.embedding.embedding_dir=/share/suh-scrap/mts247/rag-selector/indices/compactds/datastore_pq64/embeddings \
    tasks.eval.task_name=lm-eval \
    evaluation.data.eval_data=../compactds_queries/triviaqa::olmes_q.jsonl \
    evaluation.eval_output_dir=/share/suh-scrap/mts247/rag-selector/docids/compactds \
    evaluation.search.n_docs=10 \
    datastore.index.probe=$p 
done
