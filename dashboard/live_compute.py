"""
live_compute.py — Live (on-the-fly) automation score computation.

STATUS: Partially implemented. Pre-computed variant loading is fully working.
        Live recalculation is stubbed — see TODOs below.

ARCHITECTURE OVERVIEW
---------------------
Live recalculation starts from the raw occupation-level task data (tasks_final.csv
or a v2-style source) and re-applies masking + scoring weights in real time, so
users can drag sliders and immediately see how choices affect the results.

The key parameters that live recalculation exposes:
  AEI data:
    - directive_threshold : float (0–1) — mask tasks below this directive score
    - feedback_threshold  : float (0–1) — mask tasks below this feedback score
    - score_weights       : tuple of 5 floats — weights for (auto, aug, ...)

  MCP data:
    - rating_threshold    : int (1–5) — minimum MCP task rating to include
    - aggregation_method  : "mean" | "max" — how to collapse multiple MCP ratings

HOW TO COMPLETE THIS
--------------------
1. Identify the source data file that contains per-task directive/feedback scores
   before masking. This is likely `tasks_final_v2.csv` or a file produced by an
   earlier step in `scripts/data_merge.ipynb`.

2. Find the exact formula used to compute `ai_task_comp_nat/ut` from:
   - task frequency ratings
   - directive / feedback scores
   - automation / augmentation scores
   - scoring weights
   Look in the "automation scoring" cells of data_merge.ipynb.

3. Replace the TODO stubs below with that formula.

4. For MCP, find the intermediate file that has per-task MCP ratings before
   aggregation (likely `data/mcp_tasks_final.csv` or `task_results_2026-02-18.csv`)
   and apply the threshold filter live.
"""
from __future__ import annotations

import pandas as pd
import numpy as np
import streamlit as st
from pathlib import Path
from typing import Optional

from config import ROOT, DATA_DIR
from data_loader import aggregate_to_major_category


# ── Source Data Paths ──────────────────────────────────────────────────────────
# Update these once you identify the correct intermediate files.
AEI_SOURCE_FILE = DATA_DIR / "tasks_final_v2.csv"        # TODO: confirm path
MCP_SOURCE_FILE  = DATA_DIR / "mcp_tasks_final_2026-02-18.csv"  # task-level MCP ratings


# ── AEI Live Compute ───────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Computing custom AEI scores…", ttl=300)
def compute_aei_live(
    directive_threshold: float = 0.0,
    feedback_threshold: float = 0.0,
    score_weights: tuple[float, ...] = (1.0, 1.0, 0.5, 0.5, 0.5),
) -> Optional[pd.DataFrame]:
    """
    Recompute AEI automation exposure with custom masking and scoring weights.

    Parameters
    ----------
    directive_threshold : Tasks with directive_score < threshold are excluded (set to 0).
    feedback_threshold  : Tasks with feedback_score < threshold are excluded.
    score_weights       : Tuple of 5 floats weighting each automation signal.
                          Default (1, 1, 0.5, 0.5, 0.5) matches the v2 base file.

    Returns
    -------
    Occupation-level DataFrame with the same structure as pre-computed variants,
    or None if source file is missing.
    """
    if not AEI_SOURCE_FILE.exists():
        return None

    # TODO: Load raw task data with per-task directive/feedback/automation scores
    # df = pd.read_csv(AEI_SOURCE_FILE)

    # TODO: Apply masking
    # mask = (df['directive_score'] >= directive_threshold) & \
    #        (df['feedback_score'] >= feedback_threshold)
    # df.loc[~mask, 'auto_contribution'] = 0

    # TODO: Apply scoring weights
    # w1, w2, w3, w4, w5 = score_weights
    # df['ai_task_comp_nat'] = (
    #     w1 * df['signal_1_nat'] +
    #     w2 * df['signal_2_nat'] + ...
    # ) * df['freq_weight']

    # TODO: Aggregate to occupation level (groupby soc_code_2019)
    # Then compute pct_automated, people_automated, eco_value using the same
    # formulas as data_merge.ipynb

    # TODO: Apply quality filter (freq_sum_ai <= freq_sum_eco)

    # Placeholder: return None so the UI falls back gracefully
    return None


# ── MCP Live Compute ───────────────────────────────────────────────────────────

@st.cache_data(show_spinner="Computing custom MCP scores…", ttl=300)
def compute_mcp_live(
    rating_threshold: float = 2.0,
    aggregation_method: str = "mean",
) -> Optional[pd.DataFrame]:
    """
    Recompute MCP automation exposure with a custom rating threshold and
    aggregation method.

    Parameters
    ----------
    rating_threshold    : Minimum MCP task rating (1–5) to include. Tasks where
                          all MCPs rated below this are excluded.
    aggregation_method  : "mean" | "max" — how to combine ratings from multiple MCPs.

    Returns
    -------
    Occupation-level DataFrame with the same structure as pre-computed variants,
    or None if source file is missing.
    """
    if not MCP_SOURCE_FILE.exists():
        return None

    # TODO: Load task-level MCP ratings
    # df = pd.read_csv(MCP_SOURCE_FILE)

    # TODO: Filter by threshold
    # if aggregation_method == "mean":
    #     valid = df['mean_rating'] >= rating_threshold
    # elif aggregation_method == "max":
    #     valid = df['max_rating'] >= rating_threshold
    # df = df[valid].copy()

    # TODO: Map ratings to automation scores and aggregate to occupation level

    return None


# ── UI Components ──────────────────────────────────────────────────────────────

def render_aei_advanced_controls(group_id: str) -> dict:
    """
    Render AEI live-recalc sliders in the sidebar.
    Returns a dict of parameter values (or None values if not active).
    """
    st.sidebar.caption("**AEI — Custom Parameters**")

    directive_thresh = st.sidebar.slider(
        "Directive mask threshold",
        min_value=0.0, max_value=1.0, value=0.0, step=0.05,
        key=f"dir_thresh_{group_id}",
        help="Tasks with directive score below this are excluded from AI automation count.",
    )
    feedback_thresh = st.sidebar.slider(
        "Feedback mask threshold",
        min_value=0.0, max_value=1.0, value=0.0, step=0.05,
        key=f"fb_thresh_{group_id}",
        help="Tasks with feedback score below this are excluded.",
    )

    st.sidebar.caption("Scoring weights  (auto, aug, w3, w4, w5)")
    cols = st.sidebar.columns(5)
    weights = []
    defaults = [1.0, 1.0, 0.5, 0.5, 0.5]
    labels = ["w1", "w2", "w3", "w4", "w5"]
    for i, (col, label, default) in enumerate(zip(cols, labels, defaults)):
        w = col.number_input(
            label, min_value=0.0, max_value=2.0,
            value=default, step=0.1,
            key=f"weight_{i}_{group_id}",
        )
        weights.append(w)

    return {
        "directive_threshold": directive_thresh,
        "feedback_threshold": feedback_thresh,
        "score_weights": tuple(weights),
    }


def render_mcp_advanced_controls(group_id: str) -> dict:
    """
    Render MCP live-recalc controls in the sidebar.
    Returns a dict of parameter values.
    """
    st.sidebar.caption("**MCP — Custom Parameters**")

    agg_method = st.sidebar.radio(
        "Aggregation method",
        ["mean", "max"],
        horizontal=True,
        key=f"mcp_agg_{group_id}",
    )
    rating_thresh = st.sidebar.slider(
        "Minimum rating threshold",
        min_value=1.0, max_value=5.0, value=2.0, step=0.5,
        key=f"mcp_thresh_{group_id}",
        help="Tasks where no MCP achieves this rating are excluded.",
    )

    return {
        "rating_threshold": rating_thresh,
        "aggregation_method": agg_method,
    }


def live_compute_available() -> dict:
    """Check which live compute source files are present."""
    return {
        "aei": AEI_SOURCE_FILE.exists(),
        "mcp": MCP_SOURCE_FILE.exists(),
    }
