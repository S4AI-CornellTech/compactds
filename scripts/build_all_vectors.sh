#!/bin/bash
declare -A datastores=(
  ["high-quality_cc"]="c4_dclm_mixed"
  ["wikipedia_dpr"]="dpr_wiki"
  ["pubmed"]="pubmed"
  ["arxiv"]="rpj_arxiv"
  ["github"]="rpj_github"
  ["stackexchange"]="rpj_stackexchange"
  ["rpj_wikipedia"]="rpj_wikipedia"
  ["math"]="math"
  ["reddit"]="reddit_ai2"
  ["pes2o"]="pes2o"
)


# Check if an argument is passed
if [ $# -eq 0 ]; then
  echo "Usage: $0 <argument>"
  exit 1
fi

# Get the argument
download_dir=$1
output_dir=$2

# Process the argument
for config in "${!datastores[@]}"; do
  dir=${datastores[$config]}
  echo "Building vectors for: $config → $dir"
  python -m src.main_ric \
    --config-name "$config" \
    tasks.datastore.embedding=true \
    datastore.raw_data_path="$download_dir/$dir" \
    datastore.embedding.output_dir="$output_dir/$dir"
done
