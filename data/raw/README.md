# data/raw/

Raw input files for the INDUCERS pipeline.

## Files

- `TamilTB.v0.1.utf8.conll`  
  Tamil treebank in CoNLL-U format.

- `mahadevan_corpus.json`  
  Normalized Indus corpus. Single file with all inscriptions.

### `mahadevan_corpus.json` schema

Top-level keys:

- `schema_version`
- `source`
- `sign_inventory` – list of sign definitions
- `inscriptions` – list of inscription objects

Each **sign** in `sign_inventory`:

- `sign_id`: internal stable ID, e.g. `"S001"`
- `mahadevan_no`: integer, Mahadevan sign number
- `canonical`: string code, e.g. `"001"`
- `variants`: list of variant codes
- `notes`: optional comment

Each **inscription** in `inscriptions`:

- `id`: inscription ID, e.g. `"M-0001"`
- `length`: number of signs
- `sign_ids`: list of canonical sign IDs
- `variant_ids`: list of variant codes (same length as `sign_ids`)
- `metadata`: optional fields such as `mahadevan_index`, `site`, `medium`, `side`, `line`, `dating`, `references`
- `image_refs`: optional list of `{id, type, path, bbox}`
- `labels`: optional analysis labels such as `is_pentagram` or `suffix_span`