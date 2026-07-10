"""
Task: generate_data
Generates a synthetic retail sales dataset using NumPy.
"""

import logging
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

CATEGORIES = ["Electronics", "Clothing", "Food & Beverage", "Home & Garden", "Sports"]
REGIONS = ["North", "South", "East", "West", "Central"]
CHANNELS = ["Online", "In-Store", "Wholesale"]


def generate_sales_data(num_rows: int = 1000, random_seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic retail sales dataset.

    Args:
        num_rows: Number of rows to generate.
        random_seed: NumPy random seed for reproducibility.

    Returns:
        DataFrame with synthetic retail sales data.
    """
    logger.info("Generating synthetic sales data: %d rows, seed=%d", num_rows, random_seed)
    rng = np.random.default_rng(random_seed)

    # Date range: last 2 years from a fixed reference point
    start_date = datetime(2022, 1, 1)
    date_offsets = rng.integers(0, 730, size=num_rows)
    dates = [start_date + timedelta(days=int(d)) for d in date_offsets]

    categories = rng.choice(CATEGORIES, size=num_rows)
    regions = rng.choice(REGIONS, size=num_rows)
    channels = rng.choice(CHANNELS, size=num_rows, p=[0.45, 0.40, 0.15])

    # Base price varies by category
    category_base_price = {
        "Electronics": 250,
        "Clothing": 60,
        "Food & Beverage": 25,
        "Home & Garden": 90,
        "Sports": 75,
    }
    base_prices = np.array([category_base_price[c] for c in categories], dtype=float)
    noise = rng.normal(loc=1.0, scale=0.25, size=num_rows)
    unit_price = np.clip(base_prices * noise, 5, 2000).round(2)

    units_sold = rng.integers(1, 50, size=num_rows)
    revenue = (unit_price * units_sold).round(2)

    # Profit margin: varies by category and channel
    base_margin = {
        "Electronics": 0.18,
        "Clothing": 0.42,
        "Food & Beverage": 0.30,
        "Home & Garden": 0.35,
        "Sports": 0.38,
    }
    channel_margin_adj = {"Online": 0.05, "In-Store": 0.0, "Wholesale": -0.08}
    margins = np.array(
        [
            base_margin[cat] + channel_margin_adj[ch]
            for cat, ch in zip(categories, channels)
        ],
        dtype=float,
    )
    margin_noise = rng.normal(loc=0.0, scale=0.03, size=num_rows)
    profit_margin = np.clip(margins + margin_noise, 0.02, 0.75).round(4)
    profit = (revenue * profit_margin).round(2)

    customer_satisfaction = np.clip(rng.normal(loc=4.1, scale=0.6, size=num_rows), 1, 5).round(1)
    return_rate = np.clip(rng.beta(a=1.5, b=10, size=num_rows), 0, 1).round(4)

    df = pd.DataFrame(
        {
            "date": pd.to_datetime(dates),
            "category": categories,
            "region": regions,
            "channel": channels,
            "unit_price": unit_price,
            "units_sold": units_sold,
            "revenue": revenue,
            "profit": profit,
            "profit_margin": profit_margin,
            "customer_satisfaction": customer_satisfaction,
            "return_rate": return_rate,
        }
    )
    df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    df["year"] = df["date"].dt.year

    logger.info("Data generation complete. Shape: %s", df.shape)
    return df
