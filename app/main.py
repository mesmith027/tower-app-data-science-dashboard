"""
Entrypoint: re-launches this project as a Streamlit app via subprocess.

Tower runs this file as a plain Python script. Streamlit must be started
through its own CLI (`streamlit run`), so this script does exactly that —
forwarding Tower parameters as environment variables to the child process.

Tower parameters:
  NUM_ROWS    — number of synthetic data rows (default: 1000)
  RANDOM_SEED — NumPy random seed for reproducibility (default: 42)
"""

import logging
import os
import subprocess
import sys
from pathlib import Path

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

    # Resolve streamlit_app.py relative to this file — guaranteed correct
    # regardless of what the Tower working directory is set to.
    app_script = Path(__file__).resolve().parent / "streamlit_app.py"

    env = os.environ.copy()
    env["NUM_ROWS"] = str(num_rows)
    env["RANDOM_SEED"] = str(random_seed)

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_script),
        "--server.address=0.0.0.0",
        "--server.port=8501",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
    ]

    logger.info("Launching Streamlit — NUM_ROWS=%d, RANDOM_SEED=%d", num_rows, random_seed)
    logger.info("Command: %s", " ".join(cmd))
    logger.info("Streamlit app script: %s", app_script)

    result = subprocess.run(cmd, env=env, cwd=str(app_script.parent))
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
