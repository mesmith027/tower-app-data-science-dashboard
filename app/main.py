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
# Make sure to import tower at the top of your file
import tower 

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
    
    # 1. Try to get the port from the Tower SDK
    assigned_port = tower.info.port()
    
    # 2. Fallback chain: Tower SDK -> OS Environment Variable -> Local Default (8501)
    if assigned_port:
        server_port = str(assigned_port)
    else:
        server_port = os.environ.get("PORT", "8501")

    # Dynamic path resolution for streamlit_app.py
    app_script = Path("streamlit_app.py").absolute()
    if not app_script.exists():
        app_script = Path(__file__).parent / "streamlit_app.py"

    env = os.environ.copy()
    env["NUM_ROWS"] = str(num_rows)
    env["RANDOM_SEED"] = str(random_seed)

    cmd = [
        sys.executable, "-m", "streamlit", "run",
        str(app_script),
        "--server.address=0.0.0.0",
        f"--server.port={server_port}",
        "--server.headless=true",
        "--server.enableCORS=false",
        "--server.enableXsrfProtection=false",
    ]

    logger.info("Launching Streamlit — NUM_ROWS=%d, RANDOM_SEED=%d, PORT=%s", num_rows, random_seed, server_port)
    logger.info("Command: %s", " ".join(cmd))
    logger.info("Streamlit app script: %s", app_script)

    result = subprocess.run(cmd, env=env, cwd=str(app_script.parent))
    sys.exit(result.returncode)


if __name__ == "__main__":
    main()
