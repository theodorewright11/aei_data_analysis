"""
chart_builder.py — Plotly horizontal bar chart creation.

Style matches the executive summary notebook:
  - Horizontal bar charts, categories on y-axis
  - Labels inside bars (white text) showing value + share of total
  - Professional blue palette, clean white background
  - Consistent number formatting (workers: comma, wages: $B, tasks: %)
"""
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from typing import Optional

from config import COLORS, CHART_NOTE


# ── Formatting Helpers ─────────────────────────────────────────────────────────

def fmt(value: float, format_type: str) -> str:
    """Format a raw value for display on chart labels."""
    if pd.isna(value) or value is None:
        return "N/A"
    if format_type == "number":
        return f"{value:,.0f}"
    elif format_type == "currency_B":
        return f"${value / 1e9:.2f}B"
    elif format_type == "currency_M":
        return f"${value / 1e6:.1f}M"
    elif format_type == "percent":
        return f"{value:.1f}%"
    return str(value)


def bar_label(value: float, total: float, format_type: str) -> str:
    """
    Compose the inside-bar label:
      - For workers/wages: '{formatted_value} ({share_of_total}%)'
      - For %: '{value}%'  (already a percentage, no share needed)
    """
    if format_type == "percent":
        return fmt(value, "percent")
    share = (value / total * 100) if total and total > 0 else 0
    return f"{fmt(value, format_type)} ({share:.1f}%)"


# ── Core Chart Function ────────────────────────────────────────────────────────

def make_horizontal_bar(
    df: pd.DataFrame,
    value_col: str,
    category_col: str,
    title: str,
    subtitle: str,
    color: str,
    format_type: str,
    x_label: str,
    unit_scale: float = 1,
    height: Optional[int] = None,
    show_note: bool = False,
    show_pct_share: bool = True,
) -> go.Figure:
    """
    Build a styled horizontal bar chart.

    Parameters
    ----------
    df            : DataFrame (rows already sorted ascending so top bar = largest)
    value_col     : Column holding the numeric values to plot
    category_col  : Column with category names (y-axis)
    title         : Bold chart title
    subtitle      : Smaller subtitle line (dataset / geo / top-N description)
    color         : Hex color for bars
    format_type   : "number" | "currency_B" | "percent"
    unit_scale    : Divide raw values by this before plotting (e.g. 1e9 for billions)
    height        : Figure height in pixels (auto-calculated if None)
    show_note     : Whether to display the data footnote at the bottom
    show_pct_share: Show share-of-total in labels (disabled for % charts)
    """
    if df is None or df.empty:
        return _empty_chart(title)

    if value_col not in df.columns:
        return _empty_chart(f"{title} — column '{value_col}' not found")

    # Scale values for display
    raw_values = df[value_col].fillna(0)
    plot_values = raw_values / unit_scale if unit_scale > 1 else raw_values
    categories = df[category_col]
    total_raw = raw_values.sum()

    # Build text labels for inside bars
    labels = [
        bar_label(v, total_raw, format_type)
        for v in raw_values
    ]

    # Auto-height: ~30px per bar + margins
    n = len(df)
    if height is None:
        height = max(320, 32 * n + 140)
    bottom_margin = 90 if show_note else 30

    # Hover text
    hover = [
        f"<b>{cat}</b><br>"
        f"{x_label}: {fmt(v * unit_scale, format_type)}<br>"
        f"Share of total: {(v * unit_scale / total_raw * 100):.1f}%"
        if total_raw > 0 else f"<b>{cat}</b>"
        for cat, v in zip(categories, plot_values)
    ]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=plot_values,
        y=categories,
        orientation="h",
        marker=dict(color=color, line=dict(width=0)),
        text=labels,
        textposition="inside",
        insidetextanchor="middle",
        textfont=dict(color="white", size=10, family="Arial"),
        hovertext=hover,
        hoverinfo="text",
        cliponaxis=False,
    ))

    # Footnote annotation
    annotations = []
    if show_note:
        annotations.append(dict(
            text=CHART_NOTE,
            xref="paper", yref="paper",
            x=0, y=-0.16,
            showarrow=False,
            font=dict(size=8.5, color="#888"),
            align="left",
            xanchor="left",
        ))

    fig.update_layout(
        title=dict(
            text=(
                f"<b>{title}</b>"
                f"<br><span style='font-size:11px;color:#777'>{subtitle}</span>"
            ),
            font=dict(size=14, color="#222"),
            x=0,
            xanchor="left",
            pad=dict(b=4),
        ),
        xaxis=dict(
            title=dict(text=x_label, font=dict(size=11, color="#555")),
            showgrid=True,
            gridcolor=COLORS["grid"],
            gridwidth=1,
            zeroline=True,
            zerolinecolor="#ccc",
            tickfont=dict(size=10, color="#555"),
        ),
        yaxis=dict(
            title="",
            tickfont=dict(size=10, color="#333"),
            automargin=True,
        ),
        height=height,
        margin=dict(l=10, r=30, t=75, b=bottom_margin),
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False,
        annotations=annotations,
        bargap=0.25,
    )

    return fig


# ── Group Builder ──────────────────────────────────────────────────────────────

def build_group_charts(
    df: Optional[pd.DataFrame],
    geography: str,
    variant_name: str,
    top_n: int,
    color: str,
) -> tuple[go.Figure, go.Figure, go.Figure]:
    """
    Build all three charts (workers, wages, tasks) for one dashboard group.

    Returns (fig_workers, fig_wages, fig_tasks).
    """
    geo = "nat" if geography == "National" else "ut"
    subtitle = f"{variant_name}  ·  {geography}  ·  Top {top_n}"

    if df is None or df.empty:
        return (
            _empty_chart("Workers Affected"),
            _empty_chart("Wages at Risk"),
            _empty_chart("% Tasks Automated"),
        )

    from config import METRICS

    charts = {}
    for metric_key in ("workers", "wages", "tasks"):
        m = METRICS[metric_key]
        col = m["nat_col"] if geo == "nat" else m["ut_col"]

        charts[metric_key] = make_horizontal_bar(
            df=df,
            value_col=col,
            category_col="major_occ_category",
            title=m["label"],
            subtitle=subtitle,
            color=color,
            format_type=m["format"],
            x_label=m["x_label"],
            unit_scale=m["unit_scale"],
            show_note=(metric_key == "tasks"),   # footnote on bottom chart only
            show_pct_share=(metric_key != "tasks"),
        )

    return charts["workers"], charts["wages"], charts["tasks"]


# ── Empty / Error Chart ────────────────────────────────────────────────────────

def _empty_chart(title: str, message: str = "No data available") -> go.Figure:
    fig = go.Figure()
    fig.add_annotation(
        text=message,
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=13, color="#aaa"),
    )
    fig.update_layout(
        title=dict(text=f"<b>{title}</b>", font=dict(size=14, color="#555")),
        height=320,
        plot_bgcolor="white",
        paper_bgcolor="white",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig
