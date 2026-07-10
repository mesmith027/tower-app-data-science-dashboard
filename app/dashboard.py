"""
Dashboard: Streamlit UI layer for the data science dashboard.
"""

import logging

import pandas as pd
import streamlit as st

from tasks.visualizations import (
    fig_channel_breakdown,
    fig_correlation_heatmap,
    fig_monthly_trend,
    fig_region_category_heatmap,
    fig_revenue_by_category,
    fig_revenue_by_region,
    fig_revenue_distribution,
    fig_satisfaction_boxplot,
)

logger = logging.getLogger(__name__)


def _fmt_currency(value: float) -> str:
    if value >= 1_000_000:
        return f"${value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"${value / 1_000:.1f}K"
    return f"${value:.2f}"


def render_dashboard(data: dict) -> None:
    """Render the full Streamlit dashboard.

    Args:
        data: Output dictionary from run_pipeline().
    """
    st.set_page_config(
        page_title="Retail Sales Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # ── Sidebar ──────────────────────────────────────────────────────────────
    with st.sidebar:
        st.title("📊 Sales Dashboard")
        st.markdown("Synthetic retail sales data powered by **NumPy** & **Pandas**.")
        st.divider()

        df_full: pd.DataFrame = data["df"]
        all_categories = sorted(df_full["category"].unique())
        all_regions = sorted(df_full["region"].unique())
        all_channels = sorted(df_full["channel"].unique())

        selected_categories = st.multiselect(
            "Filter by Category", all_categories, default=all_categories
        )
        selected_regions = st.multiselect(
            "Filter by Region", all_regions, default=all_regions
        )
        selected_channels = st.multiselect(
            "Filter by Channel", all_channels, default=all_channels
        )

        st.divider()
        st.caption(f"Total rows in dataset: **{len(df_full):,}**")

    # Apply sidebar filters to raw df and recompute on-the-fly for charts
    from tasks.statistics import (
        compute_channel_breakdown,
        compute_correlation_matrix,
        compute_kpis,
        compute_monthly_trend,
        compute_region_category_pivot,
        compute_revenue_by_category,
        compute_revenue_by_region,
    )

    df: pd.DataFrame = df_full[
        df_full["category"].isin(selected_categories)
        & df_full["region"].isin(selected_regions)
        & df_full["channel"].isin(selected_channels)
    ].copy()

    if df.empty:
        st.warning("No data matches the current filters. Adjust the sidebar selections.")
        return

    kpis = compute_kpis(df)
    by_category = compute_revenue_by_category(df)
    by_region = compute_revenue_by_region(df)
    monthly_trend = compute_monthly_trend(df)
    channel_breakdown = compute_channel_breakdown(df)
    corr_matrix = compute_correlation_matrix(df)
    pivot = compute_region_category_pivot(df)

    # ── Header ───────────────────────────────────────────────────────────────
    st.title("🛒 Retail Sales Analytics Dashboard")
    st.markdown(
        f"Showing **{len(df):,}** of **{len(df_full):,}** orders "
        f"across **{df['category'].nunique()}** categories, "
        f"**{df['region'].nunique()}** regions, and "
        f"**{df['channel'].nunique()}** sales channels."
    )
    st.divider()

    # ── KPI Cards ────────────────────────────────────────────────────────────
    st.subheader("📌 Key Performance Indicators")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Total Revenue", _fmt_currency(kpis["total_revenue"]))
    c2.metric("Total Profit", _fmt_currency(kpis["total_profit"]))
    c3.metric("Total Orders", f"{kpis['total_orders']:,}")
    c4.metric("Avg Order Value", _fmt_currency(kpis["avg_order_value"]))
    c5.metric("Avg Profit Margin", f"{kpis['avg_profit_margin']:.1%}")
    c6.metric("Avg Satisfaction", f"{kpis['avg_customer_satisfaction']:.2f} / 5")

    st.divider()

    # ── Top Highlights ────────────────────────────────────────────────────────
    h1, h2, h3 = st.columns(3)
    h1.info(f"🏆 **Top Region:** {kpis['top_region']}")
    h2.info(f"🏅 **Top Category:** {kpis['top_category']}")
    h3.info(f"↩️ **Avg Return Rate:** {kpis['avg_return_rate']:.2%}")

    st.divider()

    # ── Time Series ──────────────────────────────────────────────────────────
    st.subheader("📈 Monthly Trends")
    st.plotly_chart(fig_monthly_trend(monthly_trend), use_container_width=True)

    st.divider()

    # ── Category & Region ────────────────────────────────────────────────────
    st.subheader("🏷️ Category & Region Breakdown")
    col_l, col_r = st.columns(2)
    with col_l:
        st.plotly_chart(fig_revenue_by_category(by_category), use_container_width=True)
    with col_r:
        st.plotly_chart(fig_revenue_by_region(by_region), use_container_width=True)

    st.divider()

    # ── Region × Category Heatmap ─────────────────────────────────────────────
    st.subheader("🗺️ Region × Category Revenue Heatmap")
    st.plotly_chart(fig_region_category_heatmap(pivot), use_container_width=True)

    st.divider()

    # ── Channel & Distributions ──────────────────────────────────────────────
    st.subheader("📦 Sales Channel & Order Distribution")
    col_a, col_b = st.columns(2)
    with col_a:
        st.plotly_chart(fig_channel_breakdown(channel_breakdown), use_container_width=True)
    with col_b:
        st.plotly_chart(fig_revenue_distribution(df), use_container_width=True)

    st.divider()

    # ── Satisfaction & Correlation ────────────────────────────────────────────
    st.subheader("😊 Customer Satisfaction & Feature Correlations")
    col_x, col_y = st.columns(2)
    with col_x:
        st.plotly_chart(fig_satisfaction_boxplot(df), use_container_width=True)
    with col_y:
        st.plotly_chart(fig_correlation_heatmap(corr_matrix), use_container_width=True)

    st.divider()

    # ── Raw Data Explorer ─────────────────────────────────────────────────────
    st.subheader("🔍 Raw Data Explorer")
    with st.expander("Show filtered dataset", expanded=False):
        st.dataframe(
            df.sort_values("date", ascending=False).reset_index(drop=True),
            use_container_width=True,
        )
        st.caption(f"{len(df):,} rows × {len(df.columns)} columns")

    # ── Category Stats Table ──────────────────────────────────────────────────
    with st.expander("Category aggregate statistics", expanded=False):
        display_cat = by_category.copy()
        display_cat["total_revenue"] = display_cat["total_revenue"].map("${:,.2f}".format)
        display_cat["total_profit"] = display_cat["total_profit"].map("${:,.2f}".format)
        display_cat["avg_margin"] = display_cat["avg_margin"].map("{:.1%}".format)
        display_cat["avg_satisfaction"] = display_cat["avg_satisfaction"].map("{:.2f}".format)
        st.dataframe(display_cat, use_container_width=True)
