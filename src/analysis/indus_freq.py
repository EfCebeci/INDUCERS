from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import List, Tuple


def load_inscriptions(path: str | Path) -> List[dict]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "inscriptions" in data:
        return data["inscriptions"]
    raise ValueError("Unexpected JSON format: expected top-level key 'inscriptions'")


def iter_sign_sequences(inscriptions: List[dict], key: str = "sign_ids"):
    for ins in inscriptions:
        seq = ins.get(key) or []
        seq = [str(x) for x in seq]
        yield ins.get("id") or ins.get("insc_id"), seq


def compute_frequencies(inscriptions: List[dict], max_len: int = 5, key: str = "sign_ids"):
    sign_freq: Counter[str] = Counter()
    bigram_freq: Counter[Tuple[str, str]] = Counter()
    trigram_freq: Counter[Tuple[str, str, str]] = Counter()
    pos_freq: Counter[Tuple[int, str]] = Counter()
    suffix_freq: Counter[str] = Counter()

    for insc_id, seq in iter_sign_sequences(inscriptions, key=key):
        L = len(seq)
        if L == 0 or L > max_len:
            continue

        sign_freq.update(seq)

        for i, s in enumerate(seq):
            pos_freq[(i, s)] += 1
            if i == L - 1:
                suffix_freq[s] += 1

        for i in range(L - 1):
            bigram_freq[(seq[i], seq[i + 1])] += 1
        for i in range(L - 2):
            trigram_freq[(seq[i], seq[i + 1], seq[i + 2])] += 1

    return {
        "sign": sign_freq,
        "bigram": bigram_freq,
        "trigram": trigram_freq,
        "pos": pos_freq,
        "suffix": suffix_freq,
    }


def write_counter_csv(counter, path: str | Path, header: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(header + ",count\n")
        for key, cnt in counter.most_common():
            if isinstance(key, tuple):
                key_str = " ".join(key)
            else:
                key_str = str(key)
            f.write(f"{key_str},{cnt}\n")


def main(corpus_path: str = "data/raw/mahadevan_corpus.json", out_dir: str = "reports/indus"):
    ins = load_inscriptions(corpus_path)
    freqs = compute_frequencies(ins, max_len=5, key="sign_ids")

    out_dir = Path(out_dir)

    # SADECE FREQUENCY RAPORLARINI SİL (01–09 prefix)
    for p in out_dir.glob("0*_indus_*_penta.csv"):
        p.unlink()

    write_counter_csv(freqs["sign"], out_dir / "01_indus_sign_freq_penta.csv", "sign")
    write_counter_csv(freqs["bigram"], out_dir / "02_indus_bigram_freq_penta.csv", "bigram")
    write_counter_csv(freqs["trigram"], out_dir / "03_indus_trigram_freq_penta.csv", "trigram")
    write_counter_csv(freqs["suffix"], out_dir / "04_indus_suffix_sign_freq_penta.csv", "suffix")

    pos_path = out_dir / "05_indus_positional_freq_penta.csv"
    pos_counter = freqs["pos"]
    with pos_path.open("w", encoding="utf-8", newline="") as f:
        f.write("position,sign,count\n")
        for (pos, sign), cnt in sorted(pos_counter.items(), key=lambda x: (-x[1], x[0][0])):
            f.write(f"{pos},{sign},{cnt}\n")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default="data/raw/mahadevan_corpus.json")
    parser.add_argument("--out", default="reports/indus")
    args = parser.parse_args()

    main(corpus_path=args.corpus, out_dir=args.out)
