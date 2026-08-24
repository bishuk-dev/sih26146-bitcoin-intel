# Team Role Assignments

The detailed team analysis, learning roadmaps, module ownership, integration contracts,
and demo plan now live in the static team website:

**[Open the SIH26146 Team Operating Manual](./index.html)**

The site is intentionally plain HTML/CSS/JS so the repository can be published directly
from GitHub Pages using the repository's `docs/` folder. It has no runtime CDN, framework,
or build step.

## Quick ownership map

| Member | Role | Owns |
|---|---|---|
| M1 | Data + Synthetic Generation | `data/generator/`, `src/ingestion/` |
| M2 | Graph + Entity Resolution | `src/graph/` |
| M3 | ML + Clustering | `src/ml/` |
| M4 | Risk + Integration | `src/scoring/`, `src/pipeline.py`, integration tests |
| M5 | Dashboard + Offline | `dashboard/`, `docker/`, `scripts/` |
| M6 | QA + Docs + Demo | `docs/`, QA matrix, demo script, judge Q&A |
