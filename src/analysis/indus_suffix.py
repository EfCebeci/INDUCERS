from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Dict, List, Tuple


def load_inscriptions(path: str | Path) -> List[dict]:
    """
    mahadevan_corpus.json içinden inscriptions listesini yükler.
    """
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
    """
    max_len uzunluğa kadar olan yazıtlar için:
      - sign_total: işaret toplam görülme sayısı
      - sign_final: işaretin son pozisyonda görülme sayısı
      - final_bigram: son iki işaret bigram frekansı
      - final_trigram: son üç işaret trigram frekansı
      - position_sum: her işaret için pozisyonların toplamı (ortalama pozisyon hesaplamak için)
    """
    sign_total: Counter[str] = Counter()
    sign_final: Counter[str] = Counter()
    final_bigram: Counter[Tuple[str, str]] = Counter()
    final_trigram: Counter[Tuple[str, str, str]] = Counter()
    position_sum: Dict[str, int] = Counter()

    for ins in inscriptions:
        seq = [str(x) for x in ins.get(key) or []]
        L = len(seq)
        # Pentagrama kadar: sadece 1–max_len arası uzunlukları al
        if L == 0 or L > max_len:
            continue

        # Toplam frekans ve pozisyon toplamı
        sign_total.update(seq)
        for pos, s in enumerate(seq):
            position_sum[s] += pos

        # Terminal işaret
        last = seq[-1]
        sign_final[last] += 1

        # Son bigram
        if L >= 2:
            final_bigram[(seq[-2], seq[-1])] += 1

        # Son trigram
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
    """
    Her işaret için:
      - total_count
      - final_count
      - final_ratio (final_count / total_count)
      - avg_position
      - is_suffix_candidate (1/0)
    yazar.
    """
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
    """
    Bigram / trigram counter'ı:
      <header>,count
    formatında yazar.
    """
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
    max_len: int = 5,
    min_final: int = 3,
    suffix_ratio_threshold: float = 0.7,
):
    inscriptions = load_inscriptions(corpus_path)
    stats = compute_suffix_stats(inscriptions, max_len=max_len, key="sign_ids")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    #SADECE SUFFIX DOSYALARINI SİL (06–08 prefix, *_penta.csv)
    for p in out_dir.glob("0[6-8]_indus_*_penta.csv"):
        p.unlink()

    # 06 – suffix istatistikleri
    write_suffix_stats_csv(
        stats,
        out_dir / "06_indus_suffix_stats_penta.csv",
        min_final=min_final,
        suffix_ratio_threshold=suffix_ratio_threshold,
    )

    # 07 – final bigramlar
    write_ngram_csv(
        stats["final_bigram"],
        out_dir / "07_indus_final_bigram_penta.csv",
        "final_bigram",
    )

    # 08 – final trigramlar
    write_ngram_csv(
        stats["final_trigram"],
        out_dir / "08_indus_final_trigram_penta.csv",
        "final_trigram",
    )

    print(f"Suffix analysis complete (≤{max_len} signs). Files written to: {out_dir}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", default="data/raw/mahadevan_corpus.json")
    parser.add_argument("--out", default="reports/indus")
    parser.add_argument("--max-len", type=int, default=5)
    parser.add_argument("--min-final", type=int, default=3)
    parser.add_argument("--suffix-ratio", type=float, default=0.7)
    args = parser.parse_args()

    main(
        corpus_path=args.corpus,
        out_dir=args.out,
        max_len=args.max_len,
        min_final=args.min_final,
        suffix_ratio_threshold=args.suffix_ratio,
    )
