"""
config.py — Dashboard configuration: paths, colors, variant definitions, metrics.

All DATA_DIR paths resolve relative to this file's location (dashboard/ → ../data/).
"""
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"
VARIATIONS_DIR = DATA_DIR / "v2_auto_aug_variations"
MCP_DIR = DATA_DIR / "mcp_variations"

# ── Colors ─────────────────────────────────────────────────────────────────────
COLORS = {
    "group_a_primary": "#3a5f83",
    "group_a_light": "#5a80a8",
    "group_b_primary": "#4a7c6f",
    "group_b_light": "#6a9c8f",
    "grid": "rgba(200,200,200,0.35)",
    "axis": "#aaa",
}

CHART_NOTE = (
    "Note: Assumes all tasks take equal time. Excludes occupations with data quality issues. "
    "Based on 2025 O*NET task data and 2024 BLS employment & wage data."
)

# ── AEI Dataset Variants ───────────────────────────────────────────────────────
AEI_VARIANTS = {
    "AEI v1 (Base)": str(DATA_DIR / "automation_tasks_imputed_v1.csv"),
    "AEI v2 (Base)": str(DATA_DIR / "automation_tasks_imputed_v2.csv"),
    # Masking variants
    "AEI v2 | Mask directive > 0.1":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_mask_directive_gt_0.1.csv"),
    "AEI v2 | Mask directive > 0.25":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_mask_directive_gt_0.25.csv"),
    "AEI v2 | Mask directive > 0.5":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_mask_directive_gt_0.5.csv"),
    "AEI v2 | Mask feedback+directive > 0.5":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_mask_feedback_directive_gt_0.5.csv"),
    "AEI v2 | Mask feedback+directive > median":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_mask_feedback_directive_above_median.csv"),
    "AEI v2 | Mask feedback+directive+iter > 0.67":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_mask_feedback_directive_task_iter_gt_0.67.csv"),
    # Scoring weight variants
    "AEI v2 | Score (1, 1, 0, 0, 0)":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_score_1_1_0_0_0.csv"),
    "AEI v2 | Score (0.8, 1, 0.5, 0.2, 0.2)":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_score_.8_1_.5_.2_.2.csv"),
    "AEI v2 | Score (1, 1, 0.5, 0.5, 0.5)":
        str(VARIATIONS_DIR / "automation_tasks_imputed_v2_score_1_1_.5_.5_.5.csv"),
}

# ── MCP Dataset Variants ───────────────────────────────────────────────────────
MCP_VARIANTS = {
    # Mean aggregation across MCPs
    "MCP | Mean rating ≥ 1": str(MCP_DIR / "automation_mcp_mean_ge_1.csv"),
    "MCP | Mean rating ≥ 2": str(MCP_DIR / "automation_mcp_mean_ge_2.csv"),
    "MCP | Mean rating ≥ 3": str(MCP_DIR / "automation_mcp_mean_ge_3.csv"),
    "MCP | Mean rating ≥ 4": str(MCP_DIR / "automation_mcp_mean_ge_4.csv"),
    "MCP | Mean rating ≥ 5": str(MCP_DIR / "automation_mcp_mean_ge_5.csv"),
    "MCP | Mean Weighted":   str(MCP_DIR / "automation_mcp_mean_weighted.csv"),
    # Max aggregation across MCPs
    "MCP | Max rating ≥ 1":  str(MCP_DIR / "automation_mcp_max_ge_1.csv"),
    "MCP | Max rating ≥ 2":  str(MCP_DIR / "automation_mcp_max_ge_2.csv"),
    "MCP | Max rating ≥ 3":  str(MCP_DIR / "automation_mcp_max_ge_3.csv"),
    "MCP | Max rating ≥ 4":  str(MCP_DIR / "automation_mcp_max_ge_4.csv"),
    "MCP | Max rating ≥ 5":  str(MCP_DIR / "automation_mcp_max_ge_5.csv"),
    "MCP | Max Weighted":    str(MCP_DIR / "automation_mcp_max_weighted.csv"),
}

ALL_VARIANTS = {**AEI_VARIANTS, **MCP_VARIANTS}

# ── Metrics Definition ─────────────────────────────────────────────────────────
# Each metric defines the raw (occupation-level) columns and display formatting.
# After groupby major_occ_category, "workers" and "wages" are summed;
# "tasks" is recomputed as sum(ai_task_comp) / sum(task_comp) * 100.
METRICS = {
    "workers": {
        "label":       "Workers Affected",
        "nat_col":     "people_automated_nat",
        "ut_col":      "people_automated_ut",
        "format":      "number",
        "x_label":     "Number of Workers",
        "unit_scale":  1,
    },
    "wages": {
        "label":       "Wages at Risk",
        "nat_col":     "eco_value_nat",
        "ut_col":      "eco_value_ut",
        "format":      "currency_B",
        "x_label":     "Annual Wages at Risk ($B)",
        "unit_scale":  1e9,
    },
    "tasks": {
        "label":       "% Tasks Automated",
        "nat_col":     "pct_automated_nat",
        "ut_col":      "pct_automated_ut",
        "ai_nat":      "ai_task_comp_nat",
        "total_nat":   "task_comp_nat",
        "ai_ut":       "ai_task_comp_ut",
        "total_ut":    "task_comp_ut",
        "format":      "percent",
        "x_label":     "% of Tasks Automated",
        "unit_scale":  1,
    },
}

# Columns to sum when aggregating to major category level
SUM_COLS = [
    "people_automated_nat", "people_automated_ut",
    "eco_value_nat", "eco_value_ut",
    "ai_task_comp_nat", "ai_task_comp_ut",
    "task_comp_nat", "task_comp_ut",
    "tot_emp_nat", "tot_emp_ut",
]

# Sort options exposed in sidebar
SORT_OPTIONS = ["Workers Affected", "Wages at Risk", "% Tasks Automated"]

SORT_COL_MAP = {
    "Workers Affected":   {"nat": "people_automated_nat", "ut": "people_automated_ut"},
    "Wages at Risk":      {"nat": "eco_value_nat",         "ut": "eco_value_ut"},
    "% Tasks Automated":  {"nat": "pct_automated_nat",     "ut": "pct_automated_ut"},
}
