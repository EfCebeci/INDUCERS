
# **INDUCERS**

> An AI lab to decipher lost languages. (YC W26)

INDUCERS is a ‘Hard Tech’ AI research lab on a mission to decipher lost languages.
We are starting with the Indus script — a 50-year-old academic problem.

This repository contains the core Python data pipeline and our initial experimental results that serve as **Proof of Execution** for our YC W26 application.

---

## **The 50-Year-Old Problem**

For half a century, academic analysis of the Indus script has been limited to classical frequency counts (N-grams).
This “flat data” approach has produced insights but not breakthroughs.

---

## **Our Solution: The Hard-Tech Hack**

We treat the problem not as linguistics, but as **computational epigraphy**.

Our hypothesis:
The key signal is hidden not in *frequency*, but in **structural and syntactic relationships** between signs.

Modern annotated corpora like Tamil TB (.conll) carry deep linguistic structure (e.g., `upos`, `deprel`, `features`).
Academia built this structure — but lacks the computational tooling to exploit it.

Our models (GNNs + Transformers) push the field from:

**“What comes next?” → “Why does this sign depend on that sign?”**

---

## **Our Model: Open-Core**

INDUCERS is a for-profit company funding an open research mission.

* **Product:** Paid API platform for structural analysis of ancient languages.
* **Mission:** Use revenue to open-source large-scale decipherment pipelines (Indus, Linear A, Proto-Elamite, Rongorongo…).

---

## **Current Status & Proof (This Repo)**

This repository is the live technical proof-of-execution.

1. **Data Pipeline → `src/analysis/stats.py`**
   Parses the Tamil `.conll` treebank and extracts structural features via `pandas` / `scikit-learn`.

2. **Experimental Outputs → `reports/`**
   CSV reports like:

   * `01_upos_frequency.csv`
   * `03_deprel_frequency.csv`
     These demonstrate quantifiable syntactic structure.

---

## **Our 3-Stage Roadmap**

### **Stage 1 — Nov 2025: The Semantic Bridge**

Finalize `indus_to_tamil_map.json`.
Bridge unsolved Indus signs to Dravidian grammatical structure.

### **Stage 2 — YC Batch: The Core AI Model**

Train first GNN/Transformer models for Indus structural prediction.
YC funding (~$125k) → GPU compute.

### **Stage 3 — Day 120: API Beta Launch**

Launch analysis API to university design partners.

---

# **Technical Usage (Data & Analysis)**

## **Raw Data**

Located in `data/raw/`:

* `TamilTB.v0.1.utf8.conll` — Tamil treebank
* `mahadevan_corpus.json` — normalized Mahadevan Indus corpus (single-file format)

---

## **Tamil Analysis**

* Script: `src/analysis/stats.py`
* Output: `reports/figures/*.csv`

---

## **Indus Analysis (≤5-sign inscriptions, “Pentagram”)**

Scripts:

* `src/analysis/indus_freq.py`
* `src/analysis/indus_suffix.py`

Output:

* `reports/indus/*.csv`
* All files overwritten each run (clean pipeline)

---

## **Run From Repo Root**

```bash
python -m src.analysis.indus_freq   --corpus data/raw/mahadevan_corpus.json --out reports/indus
python -m src.analysis.indus_suffix --corpus data/raw/mahadevan_corpus.json --out reports/indus
```

---

# **The Team**

* **Efe Cebeci** (CEO)
* **Furkan Doruk** (CTO)
