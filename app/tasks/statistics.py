"""
Task: statistics
Computes aggregate statistics from the sales DataFrame.
"""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def compute_kpis(df: pd.DataFrame) -> dict:
    """Compute top-level KPI metrics.

    Args:
        df: Sales DataFrame.

    Returns:
        Dictionary of KPI values.
    """
    top_region = df.groupby("region")["revenue"].sum().idxmax()
    top_category = df.groupby("category")["revenue"].sum().idxmax()
    return {
        "total_revenue": df["revenue"].sum(),
        "total_profit": df["profit"].sum(),
        "total_orders": len(df),
        "avg_order_value": df["revenue"].mean(),
        "avg_profit_margin": df["profit_margin"].mean(),
        "avg_customer_satisfaction": df["customer_satisfaction"].mean(),
        "avg_return_rate": df["return_rate"].mean(),
        "top_region": top_region,
        "top_category": top_category,
    }


def compute_revenue_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and profit by product category.

    Args:
        df: Sales DataFrame.

    Returns:
        DataFrame with per-category aggregates.
    """
    agg = (
        df.groupby("category")
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            avg_margin=("profit_margin", "mean"),
            num_orders=("revenue", "count"),
            avg_satisfaction=("customer_satisfaction", "mean"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    return agg


def compute_revenue_by_region(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by region.

    Args:
        df: Sales DataFrame.

    Returns:
        DataFrame with per-region aggregates.
    """
    agg = (
        df.groupby("region")
        .agg(
            total_revenue=("revenue", "sum"),
            total_profit=("profit", "sum"),
            num_orders=("revenue", "count"),
        )
        .reset_index()
        .sort_values("total_revenue", ascending=False)
    )
    return agg


def compute_monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Compute monthly revenue and profit trends.

    Args:
        df: Sales DataFrame.

    Returns:
        DataFrame indexed by month with revenue/profit totals.
    """
    trend = (
        df.groupby("month")
        .agg(
            revenue=("revenue", "sum"),
            profit=("profit", "sum"),
            orders=("revenue", "count"),
        )
        .reset_index()
        .sort_values("month")
    )
    return trend


def compute_channel_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate metrics by sales channel.

    Args:
        df: Sales DataFrame.

    Returns:
        DataFrame with per-channel aggregates.
    """
    agg = (
        df.groupby("channel")
        .agg(
            total_revenue=("revenue", "sum"),
            avg_margin=("profit_margin", "mean"),
            num_orders=("revenue", "count"),
        )
        .reset_index()
    )
    return agg


def compute_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """Compute correlation matrix for numeric features.

    Args:
        df: Sales DataFrame.

    Returns:
        Correlation matrix as a DataFrame.
    """
    numeric_cols = ["unit_price", "units_sold", "revenue", "profit", "profit_margin",
                    "customer_satisfaction", "return_rate"]
    return df[numeric_cols].corr().round(3)


def compute_region_category_pivot(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot table of revenue by region × category.

    Args:
        df: Sales DataFrame.

    Returns:
        Pivot DataFrame.
    """
    pivot = df.pivot_table(
        values="revenue", index="region", columns="category", aggfunc="sum", fill_value=0
    )
    return pivot.round(2)
