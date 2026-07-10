"""
Streamlit app entry point — invoked by main.py via `streamlit run`.

This file is owned entirely by the Streamlit runtime, which eliminates
the "missing ScriptRunContext" warning that occurs when Streamlit UI
calls are made from inside a plain Python script or thread.
"""

import logging
import os

import streamlit as st

from pipeline import run_pipeline
from dashboard import render_dashboard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
)
logger = logging.getLogger(__name__)


def _get_int(name: str, default: int) -> int:
    raw = os.environ.get(name) or os.environ.get(f"TOWER_PARAM_{name}") or str(default)
    try:
        return int(raw)
    except ValueError:
        return default


num_rows = _get_int("NUM_ROWS", 1000)
random_seed = _get_int("RANDOM_SEED", 42)


@st.cache_data(show_spinner="Generating synthetic data and computing statistics…")
def _cached_pipeline(n: int, seed: int) -> dict:
    return run_pipeline(num_rows=n, random_seed=seed)


data = _cached_pipeline(num_rows, random_seed)
render_dashboard(data)
