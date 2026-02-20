"""
app.py — Automation Exposure Dashboard (main entry point)

Run with:  streamlit run dashboard/app.py

Layout
------
SIDEBAR  ──  Group A settings  |  Group B settings
MAIN     ──  [ Group A Charts ] | [ Group B Charts ]
              Workers             Workers
              Wages               Wages
              % Tasks             % Tasks

Each group has fully independent controls. This allows side-by-side comparison
of any combination of dataset variants, geographies, and parameters.

Planned features (stubs in sidebar):
  - Live parameter recalculation (directive threshold, scoring weights)
  - SOC hierarchy depth (major → broad → minor → occupation)
  - O*NET hierarchy level (GWA → IWA → DWA → Task)
"""
import sys
import os
from pathlib import Path

# Ensure the dashboard/ directory is on sys.path so local imports work
# whether Streamlit is launched as `streamlit run app.py` (from dashboard/)
# or `streamlit run dashboard/app.py` (from project root).
_DASHBOARD_DIR = Path(__file__).resolve().parent
if str(_DASHBOARD_DIR) not in sys.path:
    sys.path.insert(0, str(_DASHBOARD_DIR))

import streamlit as st
import pandas as pd

# ── Must be first Streamlit call ───────────────────────────────────────────────
st.set_page_config(
    page_title="Automation Exposure Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Local imports (relative to dashboard/ directory)
from config import (
    AEI_VARIANTS, MCP_VARIANTS, COLORS,
    SORT_OPTIONS, METRICS,
)
from data_loader import get_aggregated_data, check_variants_exist
from chart_builder import build_group_charts, _empty_chart
from live_compute import (
    render_aei_advanced_controls,
    render_mcp_advanced_controls,
    compute_aei_live,
    compute_mcp_live,
    live_compute_available,
)


# ── Styling ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Group header banners */
.group-header {
    font-size: 1.05rem;
    font-weight: 700;
    padding: 6px 10px;
    border-radius: 4px;
    margin-bottom: 6px;
    color: white;
}
.group-a { background-color: #3a5f83; }
.group-b { background-color: #4a7c6f; }

/* Tighter sidebar labels */
.stSidebar .stRadio label p,
.stSidebar .stSelectbox label p,
.stSidebar .stSlider label p {
    font-size: 0.82rem !important;
}

/* Divider between groups in sidebar */
.sidebar-divider {
    border: none;
    border-top: 1px solid #ddd;
    margin: 14px 0 12px 0;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Group Settings
# ══════════════════════════════════════════════════════════════════════════════

def render_group_sidebar(
    group_id: str,
    color_key: str,
    default_source: str,
    default_variant: str,
    default_geo: str,
    default_sort: str,
    default_top_n: int,
) -> dict:
    """
    Render all sidebar controls for one group and return a settings dict.

    Returns
    -------
    dict with keys:
        source_type, variant_name, file_path, geography, top_n,
        sort_by, color, use_live, live_params
    """
    color = COLORS[color_key]

    # Group header
    css_class = "group-a" if group_id == "A" else "group-b"
    st.sidebar.markdown(
        f'<div class="group-header {css_class}">Group {group_id}</div>',
        unsafe_allow_html=True,
    )

    # ── Data source type ──
    source_options = ["AEI (Claude usage data)", "MCP (Agent capability data)"]
    default_source_idx = 0 if default_source == "AEI" else 1
    source_type = st.sidebar.radio(
        "Data Source",
        source_options,
        index=default_source_idx,
        key=f"source_{group_id}",
        horizontal=True,
    )
    is_aei = source_type.startswith("AEI")
    variant_dict = AEI_VARIANTS if is_aei else MCP_VARIANTS
    variant_keys = list(variant_dict.keys())

    # ── Variant selection ──
    # Show which files are missing (grayed label) — Streamlit doesn't support
    # disabled options natively, so we just list all and show a warning later.
    default_var_idx = (
        variant_keys.index(default_variant)
        if default_variant in variant_keys
        else 0
    )
    selected_variant = st.sidebar.selectbox(
        "Dataset Variant",
        variant_keys,
        index=default_var_idx,
        key=f"variant_{group_id}",
    )
    file_path = variant_dict[selected_variant]

    # ── Geography ──
    geography = st.sidebar.radio(
        "Geography",
        ["National", "Utah"],
        index=0 if default_geo == "National" else 1,
        key=f"geo_{group_id}",
        horizontal=True,
    )

    # ── Top N ──
    top_n = st.sidebar.slider(
        "Top N categories",
        min_value=5, max_value=20, value=default_top_n, step=1,
        key=f"top_n_{group_id}",
    )

    # ── Sort by ──
    sort_by = st.sidebar.selectbox(
        "Rank categories by",
        SORT_OPTIONS,
        index=SORT_OPTIONS.index(default_sort) if default_sort in SORT_OPTIONS else 0,
        key=f"sort_{group_id}",
    )

    # ── Advanced: Live Recalculation ──
    live_available = live_compute_available()
    live_key = "aei" if is_aei else "mcp"

    use_live = False
    live_params = {}

    with st.sidebar.expander("⚙ Advanced: Live Parameters", expanded=False):
        if not live_available[live_key]:
            st.info(
                "Live recalculation requires additional source files. "
                "See `live_compute.py` for setup instructions. "
                "Pre-computed variants above are fully functional."
            )
        else:
            use_live = st.checkbox(
                "Enable live recalculation",
                value=False,
                key=f"live_{group_id}",
                help=(
                    "Overrides the variant selection above. "
                    "Recalculates automation scores from raw data using the parameters below."
                ),
            )
            if use_live:
                if is_aei:
                    live_params = render_aei_advanced_controls(group_id)
                else:
                    live_params = render_mcp_advanced_controls(group_id)

        # ── Future features (placeholder) ──
        st.markdown("---")
        st.caption("**Coming soon:**")
        st.caption("• SOC depth: Major → Broad → Minor → Occupation")
        st.caption("• O\\*NET hierarchy: GWA → IWA → DWA → Task")

    return {
        "group_id":       group_id,
        "source_type":    source_type,
        "variant_name":   selected_variant,
        "file_path":      file_path,
        "geography":      geography,
        "top_n":          top_n,
        "sort_by":        sort_by,
        "color":          color,
        "is_aei":         is_aei,
        "use_live":       use_live,
        "live_params":    live_params,
    }


# ── Sidebar header ─────────────────────────────────────────────────────────────
st.sidebar.title("Dashboard Settings")
st.sidebar.caption(
    "Configure each group independently to compare datasets, "
    "geographies, or parameter variations side by side."
)
st.sidebar.markdown("---")

settings_a = render_group_sidebar(
    group_id="A",
    color_key="group_a_primary",
    default_source="AEI",
    default_variant="AEI v2 (Base)",
    default_geo="National",
    default_sort="Workers Affected",
    default_top_n=10,
)

st.sidebar.markdown('<hr class="sidebar-divider">', unsafe_allow_html=True)

settings_b = render_group_sidebar(
    group_id="B",
    color_key="group_b_primary",
    default_source="MCP",
    default_variant="MCP | Mean rating ≥ 3",
    default_geo="National",
    default_sort="Workers Affected",
    default_top_n=10,
)


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADING
# ══════════════════════════════════════════════════════════════════════════════

def load_group_data(settings: dict) -> pd.DataFrame | None:
    """
    Load and aggregate data for one group, using either pre-computed
    variant or live recalculation depending on settings.
    """
    if settings["use_live"] and settings["live_params"]:
        # Live recalculation path
        lp = settings["live_params"]
        if settings["is_aei"]:
            raw = compute_aei_live(
                directive_threshold=lp.get("directive_threshold", 0),
                feedback_threshold=lp.get("feedback_threshold", 0),
                score_weights=lp.get("score_weights", (1, 1, 0.5, 0.5, 0.5)),
            )
        else:
            raw = compute_mcp_live(
                rating_threshold=lp.get("rating_threshold", 2),
                aggregation_method=lp.get("aggregation_method", "mean"),
            )
        if raw is not None:
            # raw is already occupation-level; run through aggregation
            from data_loader import aggregate_to_major_category
            agg = aggregate_to_major_category(raw)
            geo = "nat" if settings["geography"] == "National" else "ut"
            sort_col_map = {
                "Workers Affected":   f"people_automated_{geo}",
                "Wages at Risk":      f"eco_value_{geo}",
                "% Tasks Automated":  f"pct_automated_{geo}",
            }
            sort_col = sort_col_map.get(settings["sort_by"], f"people_automated_{geo}")
            if sort_col not in agg.columns:
                sort_col = [c for c in agg.columns if "people_automated" in c][0]
            return (
                agg
                .sort_values(sort_col, ascending=False)
                .head(settings["top_n"])
                .sort_values(sort_col, ascending=True)
                .reset_index(drop=True)
            )

    # Pre-computed variant path (default)
    return get_aggregated_data(
        file_path=settings["file_path"],
        geography=settings["geography"],
        sort_by=settings["sort_by"],
        top_n=settings["top_n"],
    )


# ══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT
# ══════════════════════════════════════════════════════════════════════════════

# ── Page header ────────────────────────────────────────────────────────────────
st.title("Automation Exposure Analysis")
st.markdown(
    "Compare automation exposure across datasets, geographies, and parameter choices. "
    "Each group has independent settings — configure both in the sidebar."
)

# ── Status / warnings ─────────────────────────────────────────────────────────
file_a_ok = Path(settings_a["file_path"]).exists()
file_b_ok = Path(settings_b["file_path"]).exists()
if not file_a_ok:
    st.warning(f"Group A: File not found — `{settings_a['file_path']}`")
if not file_b_ok:
    st.warning(f"Group B: File not found — `{settings_b['file_path']}`")

# ── Load data (both groups in parallel via Streamlit cache) ───────────────────
with st.spinner("Loading data…"):
    df_a = load_group_data(settings_a) if file_a_ok or settings_a["use_live"] else None
    df_b = load_group_data(settings_b) if file_b_ok or settings_b["use_live"] else None

# ── Build charts ──────────────────────────────────────────────────────────────
fig_a_workers, fig_a_wages, fig_a_tasks = build_group_charts(
    df=df_a,
    geography=settings_a["geography"],
    variant_name=settings_a["variant_name"],
    top_n=settings_a["top_n"],
    color=settings_a["color"],
)

fig_b_workers, fig_b_wages, fig_b_tasks = build_group_charts(
    df=df_b,
    geography=settings_b["geography"],
    variant_name=settings_b["variant_name"],
    top_n=settings_b["top_n"],
    color=settings_b["color"],
)

# ── Render layout ──────────────────────────────────────────────────────────────
col_a, col_b = st.columns(2, gap="medium")

with col_a:
    st.markdown(
        '<div class="group-header group-a">Group A</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig_a_workers, use_container_width=True, key="a_workers")
    st.plotly_chart(fig_a_wages,   use_container_width=True, key="a_wages")
    st.plotly_chart(fig_a_tasks,   use_container_width=True, key="a_tasks")

with col_b:
    st.markdown(
        '<div class="group-header group-b">Group B</div>',
        unsafe_allow_html=True,
    )
    st.plotly_chart(fig_b_workers, use_container_width=True, key="b_workers")
    st.plotly_chart(fig_b_wages,   use_container_width=True, key="b_wages")
    st.plotly_chart(fig_b_tasks,   use_container_width=True, key="b_tasks")

# ── Footnote ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.caption(
    "Dashboard built for the Anthropic Economic Index (AEI) project. "
    "Source: 2025 O\\*NET task data, 2024 BLS OEWS employment & wage data, "
    "AEI conversation data, MCP server classification pipeline."
)
