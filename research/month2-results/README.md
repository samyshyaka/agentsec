# Month 2 results

Results for the three Month 2 experiments: robustness runs on a second model, a non-OpenAI model family, and the AgentDojo overlap comparison. Prepared by Kelvin, 27 October 2026.

## Files

| File | What it is |
|---|---|
| `Month2_Results.xlsx` | Summary tables with rates and 95% intervals. Start here. |
| `groq_tables_final.csv` | All result tables (72 rows), including per attack family. |
| `ad_banking_120b_pairs.csv` | AgentDojo results, 24 task pairs (banking suite, gpt-oss-120b, no defence). |
| `pilot_groq_robust_main.jsonl` | Raw runs, gpt-oss-20b, main set (15 scenarios x 4 repetitions). |
| `pilot_groq_robust_ext60.jsonl` | Raw runs, gpt-oss-20b, extended set (60 scenarios x 4), 960 runs. |
| `pilot_groq_qwen_main.jsonl` | Raw runs, Qwen3.8-27B, main set (15 scenarios x 4 repetitions). |
| `groq_tables_v2.py` | Script that builds the tables from the raw files. |

## Headline results

| Experiment | No defence (C0) | Full defence (C4) |
|---|---|---|
| gpt-oss-20b, extended set: attacks that succeeded | 194 / 240 (80.8%) | 23 / 240 (9.6%) |
| gpt-oss-20b, main set | 21 / 60 (35.0%) | 0 / 60 (upper bound 18.1%) |
| Qwen3.8-27B, main set | 15 / 60 (25.0%) | 0 / 60 (upper bound 18.1%) |
| AgentDojo banking subset, no defence (gpt-oss-120b) | 19 / 24 attacker goals achieved | not tested |

Benign task completion was unchanged by the defence in every comparison. The AgentDojo comparison is partial and is not a ranking of benchmarks.

## Notes on the raw files

- One run per line (JSON). Files only ever have lines added.
- Only lines with `status` equal to `ok` are counted. Failed calls stay in the file as errors, are ignored in every count, and were re-run.
- The main set and the extended set are reported separately and not pooled.

## Rebuild the tables (optional)

Needs Python 3 and nothing else:

```
python groq_tables_v2.py rebuilt.csv pilot_groq_robust_main.jsonl pilot_groq_robust_ext60.jsonl pilot_groq_qwen_main.jsonl
```

`rebuilt.csv` should match `groq_tables_final.csv`. Intervals use a scenario-cluster bootstrap (5,000 resamples, seed 20261012); cells with no successes show an exact upper bound, 1 - 0.05^(1/k), with scenarios as the independent units.

## Protocol deviations

Every departure from the Paper 1 protocol is numbered in `DEVIATIONS.md` in the reproducibility package (17 entries).

This folder contains results only. It contains no keys or credentials.
