# Role Assignments

Modules are defined by natural system boundaries (see README architecture),
not split evenly for the sake of it. Map your actual teammates' strengths
onto these — merge or split modules depending on team size.

| Module | Owns | Best fit for someone who... |
|---|---|---|
| Data + Synthetic Generation | `data/generator/`, `src/ingestion/` | Likes data modeling, is comfortable owning the labeled-vs-unlabeled decision |
| Graph Engine | `src/graph/` | Enjoys graph theory / NetworkX, entity resolution logic |
| ML Core | `src/ml/` | Strongest in ML — owns whichever path (A/B) the team picks, plus SHAP |
| Risk Scoring | `src/scoring/` | Good at systems/integration thinking — this module depends on both graph and ML output |
| Dashboard | `dashboard/` | Frontend/UX instinct — this is what judges actually see and click |
| DevOps + Offline Packaging + Docs | `docker/`, `scripts/`, writeup, pitch | Detail-oriented, good at "make it actually work under constraints" — also naturally ends up owning the pitch narrative since they understand the whole system's constraints best |

TODO: fill in names once team roster is confirmed.
