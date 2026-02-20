"""
data_loader.py — Data loading, caching, and aggregation for the dashboard.

Each automation file has ~878 occupation-level rows. The main aggregation step
groups occupations into ~22 major categories. Streamlit caching avoids re-reading
files on every widget interaction.
"""
import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from typing import Optional

from config import SUM_COLS


# ── Raw Loading ────────────────────────────────────────────────────────────────

@st.cache_data(show_spinner=False)
def load_variant_raw(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load a pre-computed automation CSV and apply the standard quality filter:
        freq_sum_ai <= freq_sum_eco
    (Removes ~7 occupations where AI task frequency exceeds economy task frequency,
    which indicates a data quality issue.)

    Returns None if the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        return None

    df = pd.read_csv(path, low_memory=False)

    # Quality filter
    if "freq_sum_ai" in df.columns and "freq_sum_eco" in df.columns:
        df = df[df["freq_sum_ai"] <= df["freq_sum_eco"]].copy()

    return df


# ── Aggregation ────────────────────────────────────────────────────────────────

def aggregate_to_major_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Collapse occupation-level rows into major occupational category totals.

    - Workers / wages:  summed across occupations in each category
    - % tasks automated: recomputed as ratio of totals (not mean of percentages),
      which gives a properly employment-weighted aggregate
    """
    if df is None or df.empty or "major_occ_category" not in df.columns:
        return pd.DataFrame()

    # Only sum columns that actually exist in this file
    available_sum_cols = [c for c in SUM_COLS if c in df.columns]

    grouped = (
        df.groupby("major_occ_category")[available_sum_cols]
        .sum()
        .reset_index()
    )

    # Recompute % automated from component sums (avoids averaging-of-averages bias)
    for geo in ("nat", "ut"):
        ai_col    = f"ai_task_comp_{geo}"
        total_col = f"task_comp_{geo}"
        pct_col   = f"pct_automated_{geo}"
        if ai_col in grouped.columns and total_col in grouped.columns:
            grouped[pct_col] = (
                grouped[ai_col] / grouped[total_col].replace(0, np.nan) * 100
            )

    return grouped


# ── Main Entry Point for Charts ────────────────────────────────────────────────

def get_aggregated_data(
    file_path: str,
    geography: str,   # "National" | "Utah"
    sort_by: str,     # one of SORT_OPTIONS from config
    top_n: int,
) -> Optional[pd.DataFrame]:
    """
    Full pipeline: load → filter → aggregate → sort → top-N.

    Returns a DataFrame ready to hand to chart_builder, with rows in ascending
    order of the sort metric so horizontal bars read correctly (largest on top).
    Returns None if the file is missing.
    """
    raw = load_variant_raw(file_path)
    if raw is None:
        return None

    agg = aggregate_to_major_category(raw)
    if agg.empty:
        return None

    geo = "nat" if geography == "National" else "ut"

    # Resolve sort column
    sort_col_map = {
        "Workers Affected":   f"people_automated_{geo}",
        "Wages at Risk":      f"eco_value_{geo}",
        "% Tasks Automated":  f"pct_automated_{geo}",
    }
    sort_col = sort_col_map.get(sort_by, f"people_automated_{geo}")

    # Fallback if column missing
    if sort_col not in agg.columns:
        available = [c for c in agg.columns if "people_automated" in c]
        if not available:
            return None
        sort_col = available[0]

    result = (
        agg
        .sort_values(sort_col, ascending=False)
        .head(top_n)
        .sort_values(sort_col, ascending=True)   # ascending = largest bar at top
        .reset_index(drop=True)
    )

    return result


# ── File Availability Check ────────────────────────────────────────────────────

def check_variants_exist(variant_dict: dict) -> dict[str, bool]:
    """Return {variant_name: file_exists} for all variants in a dict."""
    return {name: Path(path).exists() for name, path in variant_dict.items()}
