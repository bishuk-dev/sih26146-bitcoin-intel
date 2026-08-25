# SIH26146 Team Roles

Use `index.html` as the main team handbook.

| Member | Owns | Main files |
|---|---|---|
| M1 | Data + synthetic generator | `data/generator/*`, `src/ingestion/*` |
| M2 | Graph + entity resolution | `src/graph/*` |
| M3 | ML / detection | `src/ml/*`, ML experiments |
| M4 | Risk + integration | `src/scoring/*`, `src/pipeline.py` |
| M5 | Dashboard + offline deployment | `dashboard/*`, `docker/*`, `scripts/*` |
| M6 | QA + docs + demo | `docs/*`, QA matrix, demo script |

## Working rule

Every completed task should leave three things:

1. A code/documentation change committed on the member's branch.
2. A small test, sample output, screenshot, or other evidence that it works.
3. A hand-off note explaining what the next person can now use.

Do not wait for the entire project before testing your part.
