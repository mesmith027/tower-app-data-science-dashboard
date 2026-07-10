# 📊 Data Science Dashboard — Tower App

An interactive Streamlit data science dashboard powered by **Pandas**, **NumPy**, and **Plotly**. Ships with a built-in synthetic retail sales dataset — no external data source required.

---

## Architecture

```
./
├── Towerfile                   # Tower app config & parameters
├── pyproject.toml              # Python dependencies
├── README.md
└── app/
    ├── main.py                 # Tower entrypoint — launches Streamlit
    ├── pipeline.py             # Orchestrates data generation & stats
    ├── dashboard.py            # Streamlit UI layer
    └── tasks/
        ├── generate_data.py    # Synthetic dataset generation (NumPy)
        ├── statistics.py       # Aggregate stat computations (Pandas)
        └── visualizations.py  # Plotly chart builders
```

---

## How the Pipeline Works

1. **`generate_data.py`** — Uses NumPy to generate a deterministic synthetic retail sales dataset with configurable row count and random seed. Fields: `date`, `category`, `region`, `channel`, `unit_price`, `units_sold`, `revenue`, `profit`, `profit_margin`, `customer_satisfaction`, `return_rate`.

2. **`statistics.py`** — Computes KPIs, category/region/channel aggregates, monthly trends, a correlation matrix, and a region × category pivot table using Pandas groupby operations.

3. **`visualizations.py`** — Builds Plotly figures (line charts, bar charts, heatmaps, histograms, box plots, pie charts) from the computed aggregates.

4. **`pipeline.py`** — Wires steps 1–2 together and returns a single results dictionary cached by Streamlit.

5. **`dashboard.py`** — Renders the full Streamlit UI: KPI cards, sidebar filters, and all charts.

---

## Dashboard Sections

| Section | Description |
|---|---|
| KPI Cards | Total revenue, profit, orders, avg order value, margin, satisfaction |
| Top Highlights | Top region, top category, avg return rate |
| Monthly Trends | Revenue + profit line chart with order volume bar overlay |
| Category & Region | Horizontal bar chart + donut pie chart |
| Region × Category Heatmap | Revenue breakdown across all region/category combos |
| Sales Channel | Revenue bar + avg margin scatter by channel |
| Order Revenue Distribution | Overlaid histogram by category |
| Customer Satisfaction | Box plots by category |
| Feature Correlations | Numeric correlation heatmap |
| Raw Data Explorer | Sortable/filterable raw data table |

---

## Parameters

| Name | Description | Default |
|---|---|---|
| `NUM_ROWS` | Number of synthetic data rows to generate | `1000` |
| `RANDOM_SEED` | NumPy random seed for reproducibility | `42` |

Parameters are set in the Tower UI or passed via `tower run --parameter=NUM_ROWS=5000`.

---

## No Secrets Required

This app uses only synthetic data and no external services — **no API keys or secrets are needed**.

---

## Deployment

### Option 1 — Deploy button (recommended)
Click the **Deploy** button below the chat in Tower Control. No terminal needed.

### Option 2 — Tower CLI
```bash
# 1. Download and unzip the project, then:
cd data-science-dashboard
pip install -U tower
tower login
tower deploy
tower run
# Or with custom params:
tower run --parameter=NUM_ROWS=5000 --parameter=RANDOM_SEED=99
```

Docs: https://docs.tower.dev

---

## Extending the App

- **Add a new chart:** create a new `fig_*` function in `tasks/visualizations.py` and call it from `dashboard.py`.
- **Add a new stat:** add a `compute_*` function in `tasks/statistics.py`, wire it in `pipeline.py`, and surface it in `dashboard.py`.
- **Swap in real data:** replace `generate_sales_data()` in `tasks/generate_data.py` with a real data loader (CSV, database, API). The rest of the pipeline remains unchanged as long as the returned DataFrame has the same column schema.
- **Increase dataset size:** set `NUM_ROWS` to a larger value (e.g. `100000`) at run time.
