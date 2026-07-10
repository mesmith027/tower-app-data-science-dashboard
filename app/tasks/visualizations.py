"""
Task: visualizations
Builds Plotly figures for the Streamlit dashboard.
"""

import logging

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

logger = logging.getLogger(__name__)

PALETTE = px.colors.qualitative.Plotly


def fig_monthly_trend(trend_df: pd.DataFrame) -> go.Figure:
    """Line chart: monthly revenue and profit over time.

    Args:
        trend_df: Output of compute_monthly_trend().

    Returns:
        Plotly Figure.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Scatter(
            x=trend_df["month"],
            y=trend_df["revenue"],
            name="Revenue",
            line=dict(color="#636EFA", width=2),
            mode="lines+markers",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=trend_df["month"],
            y=trend_df["profit"],
            name="Profit",
            line=dict(color="#00CC96", width=2, dash="dash"),
            mode="lines+markers",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Bar(
            x=trend_df["month"],
            y=trend_df["orders"],
            name="Orders",
            marker_color="rgba(180,180,180,0.35)",
            yaxis="y2",
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Monthly Revenue, Profit & Order Volume",
        xaxis_title="Month",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        height=420,
    )
    fig.update_yaxes(title_text="Amount ($)", secondary_y=False)
    fig.update_yaxes(title_text="Orders", secondary_y=True)
    return fig


def fig_revenue_by_category(cat_df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart: revenue and profit by category.

    Args:
        cat_df: Output of compute_revenue_by_category().

    Returns:
        Plotly Figure.
    """
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            y=cat_df["category"],
            x=cat_df["total_revenue"],
            name="Revenue",
            orientation="h",
            marker_color="#636EFA",
        )
    )
    fig.add_trace(
        go.Bar(
            y=cat_df["category"],
            x=cat_df["total_profit"],
            name="Profit",
            orientation="h",
            marker_color="#00CC96",
        )
    )
    fig.update_layout(
        title="Revenue & Profit by Category",
        barmode="group",
        xaxis_title="Amount ($)",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def fig_revenue_by_region(region_df: pd.DataFrame) -> go.Figure:
    """Pie chart: revenue share by region.

    Args:
        region_df: Output of compute_revenue_by_region().

    Returns:
        Plotly Figure.
    """
    fig = px.pie(
        region_df,
        names="region",
        values="total_revenue",
        title="Revenue Share by Region",
        color_discrete_sequence=PALETTE,
        hole=0.4,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(height=380)
    return fig


def fig_correlation_heatmap(corr_df: pd.DataFrame) -> go.Figure:
    """Heatmap of numeric feature correlations.

    Args:
        corr_df: Output of compute_correlation_matrix().

    Returns:
        Plotly Figure.
    """
    fig = go.Figure(
        data=go.Heatmap(
            z=corr_df.values,
            x=corr_df.columns.tolist(),
            y=corr_df.index.tolist(),
            colorscale="RdBu",
            zmid=0,
            text=corr_df.values.round(2),
            texttemplate="%{text}",
            showscale=True,
        )
    )
    fig.update_layout(title="Feature Correlation Heatmap", height=420)
    return fig


def fig_revenue_distribution(df: pd.DataFrame) -> go.Figure:
    """Histogram: distribution of per-order revenue by category.

    Args:
        df: Raw sales DataFrame.

    Returns:
        Plotly Figure.
    """
    fig = px.histogram(
        df,
        x="revenue",
        color="category",
        nbins=60,
        barmode="overlay",
        opacity=0.72,
        title="Order Revenue Distribution by Category",
        labels={"revenue": "Order Revenue ($)"},
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(height=400, bargap=0.05)
    return fig


def fig_region_category_heatmap(pivot_df: pd.DataFrame) -> go.Figure:
    """Heatmap: revenue by region × category.

    Args:
        pivot_df: Output of compute_region_category_pivot().

    Returns:
        Plotly Figure.
    """
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_df.values,
            x=pivot_df.columns.tolist(),
            y=pivot_df.index.tolist(),
            colorscale="Blues",
            text=pivot_df.values,
            texttemplate="$%{text:,.0f}",
            showscale=True,
        )
    )
    fig.update_layout(
        title="Revenue Heatmap: Region × Category",
        xaxis_title="Category",
        yaxis_title="Region",
        height=380,
    )
    return fig


def fig_channel_breakdown(channel_df: pd.DataFrame) -> go.Figure:
    """Bar chart: orders and average margin by channel.

    Args:
        channel_df: Output of compute_channel_breakdown().

    Returns:
        Plotly Figure.
    """
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(
        go.Bar(
            x=channel_df["channel"],
            y=channel_df["total_revenue"],
            name="Revenue",
            marker_color="#636EFA",
        ),
        secondary_y=False,
    )
    fig.add_trace(
        go.Scatter(
            x=channel_df["channel"],
            y=channel_df["avg_margin"] * 100,
            name="Avg Margin %",
            mode="markers+lines",
            marker=dict(size=12, color="#EF553B"),
            line=dict(color="#EF553B"),
        ),
        secondary_y=True,
    )
    fig.update_layout(
        title="Revenue & Average Margin by Sales Channel",
        height=380,
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    fig.update_yaxes(title_text="Revenue ($)", secondary_y=False)
    fig.update_yaxes(title_text="Avg Margin (%)", secondary_y=True)
    return fig


def fig_satisfaction_boxplot(df: pd.DataFrame) -> go.Figure:
    """Box plot: customer satisfaction distribution by category.

    Args:
        df: Raw sales DataFrame.

    Returns:
        Plotly Figure.
    """
    fig = px.box(
        df,
        x="category",
        y="customer_satisfaction",
        color="category",
        title="Customer Satisfaction by Category",
        labels={"customer_satisfaction": "Satisfaction (1–5)"},
        color_discrete_sequence=PALETTE,
    )
    fig.update_layout(height=400, showlegend=False)
    return fig
