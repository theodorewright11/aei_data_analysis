# Automation Exposure Dashboard

Interactive Streamlit dashboard for comparing automation exposure metrics across datasets, geographies, and parameter variations.

## Quick Start

```bash
# From the project root (automation_exposure_analysis/)
cd dashboard
pip install -r requirements.txt
streamlit run app.py
```

Then open http://localhost:8501 in your browser.

## What It Shows

**6 charts across 2 independent groups (3 charts each):**
- Workers Affected — number of workers in occupations with substantial AI task exposure
- Wages at Risk — annual wages of those workers ($B)
- % Tasks Automated — share of occupational tasks covered by AI/MCP capabilities

**Per-group controls (sidebar):**
| Control | Options |
|---|---|
| Data Source | AEI (Claude usage data) or MCP (agent capability data) |
| Dataset Variant | 11 AEI variants, 12 MCP variants |
| Geography | National or Utah |
| Top N | 5–20 major occupational categories |
| Sort By | Workers / Wages / % Tasks |

## Dataset Variants

### AEI Variants (`data/automation_tasks_imputed_v*.csv`)
| Variant | Description |
|---|---|
| AEI v1 (Base) | Original AEI automation scoring |
| AEI v2 (Base) | Updated AEI scoring methodology |
| Mask directive > 0.1/0.25/0.5 | Exclude low-directive tasks |
| Mask feedback+directive | Multi-signal masking |
| Score (w1,w2,w3,w4,w5) | Alternative scoring weight combinations |

### MCP Variants (`data/mcp_variations/`)
| Variant | Description |
|---|---|
| Mean rating ≥ 1–5 | Average MCP rating threshold to include tasks |
| Max rating ≥ 1–5 | Maximum MCP rating threshold |
| Weighted (mean/max) | Rating-weighted aggregation |

## File Structure

```
dashboard/
├── app.py            # Main Streamlit app (entry point)
├── config.py         # Paths, colors, variant definitions, metrics
├── data_loader.py    # Data loading (cached) + aggregation logic
├── chart_builder.py  # Plotly horizontal bar chart functions
├── live_compute.py   # Live parameter recalculation (stub — see TODOs)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Future Features (Placeholders in Sidebar)

- **SOC hierarchy depth**: Currently shows Major Occupational Groups only. Future: Broad Group → Minor Group → Detailed Occupation
- **O\*NET hierarchy level**: Future: aggregate by GWA → IWA → DWA → Task instead of occupation
- **Live recalculation**: Drag sliders for masking thresholds and scoring weights to recompute on the fly. Requires completing the TODOs in `live_compute.py` — see that file for instructions.

## Completing Live Recalculation

To enable live parameter adjustment:

1. Open `live_compute.py`
2. Identify the source data file with per-task directive/feedback/automation scores (likely `tasks_final_v2.csv`)
3. Look up the exact scoring formula in `scripts/data_merge.ipynb`
4. Fill in the TODO stubs in `compute_aei_live()` and `compute_mcp_live()`

Once those functions return a valid DataFrame, the "Advanced: Live Parameters" expander in the sidebar will activate automatically.
