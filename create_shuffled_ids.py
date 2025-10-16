import os
import glob
import re
import pickle
import numpy as np
from tqdm import tqdm

# Edit here
EMBED_GLOB_PATTERN = (
    "/share5/akiho.kawada/compactds/datastores/compactds/embeddings/**/*.pkl"
)

START_SHARD = 0
END_SHARD = 480  # exclusive

OUTPUT_PATH = f"shuffled_ids_{START_SHARD}_{END_SHARD-1}.npy"

# Edit end


def natural_key(name):
    b = os.path.basename(name)
    return [int(t) if t.isdigit() else t.lower() for t in re.findall(r"\d+|\D+", b)]


def count_in_pickle(path):
    with open(path, "rb") as f:
        # expected format: tuple (list of ids, numpy array of embeddings)
        _, embeddings = pickle.load(f)
    return len(embeddings)


def main():
    print("Phase 1: Counting total vectors...")

    all_paths = glob.glob(EMBED_GLOB_PATTERN, recursive=True)
    if not all_paths:
        raise SystemExit(f"No files matched the pattern: {EMBED_GLOB_PATTERN}")
    all_paths.sort(key=natural_key)

    target_paths = all_paths[START_SHARD:END_SHARD]

    print(
        f"Found {len(all_paths)} total files. Processing shards from {START_SHARD} to {END_SHARD-1} ({len(target_paths)} files)."
    )

    total_vectors = 0
    for path in tqdm(target_paths, desc="Counting vectors"):
        try:
            total_vectors += count_in_pickle(path)
        except Exception as e:
            print(f"\n[WARN] Could not process {path}: {e}")

    print(f"\nPhase 1 Complete. Total vectors found: {total_vectors:,}")

    if total_vectors == 0:
        raise SystemExit("No vectors found. Aborting ID generation.")

    print("\nPhase 2: Generating and shuffling IDs...")
    print("This may take a significant amount of memory and time.")

    try:
        ids = np.arange(total_vectors, dtype="int64")
    except MemoryError:
        gigs = (total_vectors * 8) / (1024**3)
        raise SystemExit(
            f"MemoryError: Failed to allocate array for {total_vectors:,} IDs. This would require approx. {gigs:.2f} GB of RAM."
        )

    print("Shuffling IDs...")
    np.random.shuffle(ids)

    print(f"Saving shuffled IDs to {OUTPUT_PATH}...")
    np.save(OUTPUT_PATH, ids)

    print("\nPhase 2 Complete. All done!")
    print(f"'{OUTPUT_PATH}' has been created successfully.")


if __name__ == "__main__":
    main()
