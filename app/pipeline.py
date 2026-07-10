"""
Pipeline: orchestrates data generation and stat computation.
"""

import logging

import pandas as pd

from tasks.generate_data import generate_sales_data
from tasks.statistics import (
    compute_channel_breakdown,
    compute_correlation_matrix,
    compute_kpis,
    compute_monthly_trend,
    compute_region_category_pivot,
    compute_revenue_by_category,
    compute_revenue_by_region,
)

logger = logging.getLogger(__name__)


def run_pipeline(num_rows: int = 1000, random_seed: int = 42) -> dict:
    """Run the full data pipeline and return all computed artifacts.

    Args:
        num_rows: Number of synthetic rows to generate.
        random_seed: NumPy random seed.

    Returns:
        Dictionary containing the raw DataFrame and all aggregate results.
    """
    logger.info("Starting pipeline — num_rows=%d, seed=%d", num_rows, random_seed)

    df = generate_sales_data(num_rows=num_rows, random_seed=random_seed)

    results = {
        "df": df,
        "kpis": compute_kpis(df),
        "by_category": compute_revenue_by_category(df),
        "by_region": compute_revenue_by_region(df),
        "monthly_trend": compute_monthly_trend(df),
        "channel_breakdown": compute_channel_breakdown(df),
        "correlation_matrix": compute_correlation_matrix(df),
        "region_category_pivot": compute_region_category_pivot(df),
    }

    logger.info("Pipeline complete.")
    return results
