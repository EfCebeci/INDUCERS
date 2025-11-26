# reports/

This folder contains **derived** data products (CSV, figures, etc.).  
Source data lives in `data/`.

We keep Tamil and Indus analyses strictly separate.

```text
reports/
  figures/   # Tamil – treebank-based statistics
  indus/     # Indus – Mahadevan-based statistics
```

---

## Tamil (`reports/figures/`)

Produced from `TamilTB.v0.1.utf8.conll` via `src/analysis/stats.py`.

Example files:

* `00_INDUCERS_Rich_Dataframe.csv`
* `01_upos_frequency.csv`
* `02_lemma_frequency.csv`
* `03_deprel_frequency.csv`

---

## Indus (`reports/indus/`)

Produced from `mahadevan_corpus.json` via:

```bash
python -m src.analysis.indus_freq   --corpus data/raw/mahadevan_corpus.json --out reports/indus
python -m src.analysis.indus_suffix --corpus data/raw/mahadevan_corpus.json --out reports/indus
```

On each run, existing `reports/indus/*.csv` files are overwritten.

### File overview (≤ 5-sign inscriptions only):

* `01_indus_sign_freq_penta.csv`
* `02_indus_bigram_freq_penta.csv`
* `03_indus_trigram_freq_penta.csv`
* `04_indus_suffix_sign_freq_penta.csv`
* `05_indus_positional_freq_penta.csv`
* `06_indus_suffix_stats_penta.csv`
* `07_indus_final_bigram_penta.csv`
* `08_indus_final_trigram_penta.csv`
