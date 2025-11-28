from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


def load_inscriptions(path: str | Path) -> List[dict]:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "inscriptions" in data:
        return data["inscriptions"]
    raise ValueError("Unexpected JSON format: expected top-level key 'inscriptions'")


def compute_suffix_stats(
    inscriptions: List[dict],
    max_len: int = 5,
    key: str = "sign_ids",
):
    sign_total: Counter[str] = Counter()
    sign_final: Counter[str] = Counter()
    final_bigram: Counter[Tuple[str, str]] = Counter()
    final_trigram: Counter[Tuple[str, str, str]] = Counter()
    position_sum: Dict[str, int] = Counter()

    for ins in inscriptions:
        seq = [str(x) for x in ins.get(key) or []]
        L = len(seq)
        if L == 0 or L > max_len:
            continue

        sign_total.update(seq)
        for pos, s in enumerate(seq):
            position_sum[s] += pos

        last = seq[-1]
        sign_final[last] += 1

        if L >= 2:
            final_bigram[(seq[-2], seq[-1])] += 1
        if L >= 3:
            final_trigram[(seq[-3], seq[-2], seq[-1])] += 1

    return {
        "sign_total": sign_total,
        "sign_final": sign_final,
        "final_bigram": final_bigram,
        "final_trigram": final_trigram,
        "position_sum": position_sum,
    }


def write_suffix_stats_csv(
    stats: dict,
    path: str | Path,
    min_final: int = 3,
    suffix_ratio_threshold: float = 0.7,
):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    total = stats["sign_total"]
    final = stats["sign_final"]
    pos_sum = stats["position_sum"]

    with path.open("w", encoding="utf-8", newline="") as f:
        f.write("sign,total_count,final_count,final_ratio,avg_position,is_suffix_candidate\n")
        for sign, tot in total.most_common():
            fin = final.get(sign, 0)
            ratio = fin / tot if tot else 0.0
            avg_pos = pos_sum[sign] / tot if tot else 0.0
            is_candidate = int(fin >= min_final and ratio >= suffix_ratio_threshold)
            f.write(f"{sign},{tot},{fin},{ratio:.4f},{avg_pos:.4f},{is_candidate}\n")


def write_ngram_csv(counter: Counter, path: str | Path, header: str):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        f.write(header + ",count\n")
        for key, cnt in counter.most_common():
            key_str = " ".join(key) if isinstance(key, tuple) else str(key)
            f.write(f"{key_str},{cnt}\n")


def main(
    corpus_path: str = "data/raw/mahadevan_corpus.json",
    out_dir: str = "reports/indus",
    min_final: int = 3,
    suffix_ratio_threshold: float = 0.7,
):
    ins = load_inscriptions(corpus_path)
    stats = compute_suffix_stats(ins, max_len=5, key="sign_ids")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    #SADECE SUFFIX DOSYALARINI SİL (prefix 06–09)
    for p in out_dir.glob("0[6-9]_indus_*.csv"):
        p.unlink()

    # 06 – suffix stats
    write_suffix_stats_csv(
        stats,
        out_dir / "06_indus_suffix_stats_penta.csv",
        min_final=min_final,
        suffix_ratio_threshold=suffix_ratio_threshold,
    )

    # 07 – final bigrams
    write_ngram_csv(
        stats["final_bigram"],
        out_dir / "07_indus_final_bigram_penta.csv",
        "final_bigram",
    )

    # 08 – final trigrams
    write_ngram_csv(
        stats["final_trigram"],
        out_dir / "08_indus_final_trigram_penta.csv",
        "trigram_final",
    )

    print("Suffix analysis complete. Files written to:", out_dir)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default="data/raw/mahadevan_corpus.json")
    parser.add_argument("--out", default="reports/indus")
    parser.add_argument("--min-final", type=int, default=3)
    parser.add_argument("--suffix-ratio", type=float, default=0.7)
    args = parser.parse_args()

    main(
        corpus_path=args.corpus,
        out_dir=args.out,
        min_final=args.min_final,
        suffix_ratio_threshold=args.suffix_ratio,
    )
