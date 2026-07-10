"""
Entrypoint: launches the Streamlit data science dashboard.

Tower parameters:
  NUM_ROWS    — number of synthetic data rows (default: 1000)
  RANDOM_SEED — NumPy random seed for reproducibility (default: 42)
"""

import logging
import os
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def _get_int_param(name: str, default: int) -> int:
    """Read a Tower integer parameter from env, with legacy fallback."""
    raw = (
        os.environ.get(name)
        or os.environ.get(f"TOWER_PARAM_{name}")
        or str(default)
    )
    try:
        return int(raw)
    except ValueError:
        logger.warning("Invalid value for %s: %r — using default %d", name, raw, default)
        return default


def main() -> None:
    num_rows = _get_int_param("NUM_ROWS", 1000)
    random_seed = _get_int_param("RANDOM_SEED", 42)

    logger.info("Launching dashboard — NUM_ROWS=%d, RANDOM_SEED=%d", num_rows, random_seed)

    # Import here so Streamlit's module watcher sees them after env is set
    import streamlit as st
    from pipeline import run_pipeline
    from dashboard import render_dashboard

    @st.cache_data(show_spinner="Generating synthetic data and computing statistics…")
    def _cached_pipeline(n: int, seed: int) -> dict:
        return run_pipeline(num_rows=n, random_seed=seed)

    data = _cached_pipeline(num_rows, random_seed)
    render_dashboard(data)


if __name__ == "__main__":
    main()
