# Aviation Fuel Prediction Project

This repository is organized into a clear backend/frontend/docs structure to support data analysis, modeling, and a simple frontend.

## Structure

```
backend/
  src/                  # Python source scripts
  data/                 # Input datasets (CSV)
  credentials/          # Private credentials (e.g., kaggle.json)
  reports/
    figures/            # Generated plots (PNG)
    results/            # Generated metrics/tables (CSV)
    presentations/      # Decks and related artifacts
frontend/
  public/               # Static assets (index.html)
  src/                  # Frontend source (App.jsx, App.css)
docs/                   # Project documentation (Markdown)
```

## Quickstart (Windows, Command Prompt)

1) Create and activate a virtual environment (manual setup):

```
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r backend\requirements.txt
```

2) Run scripts (examples):

```
# Exploratory data analysis and visualizations
python backend\src\eda_script.py
python backend\src\eda_visualizations.py

# Split dataset
python backend\src\split_dataset.py

# Train baseline models
python backend\src\train_models.py

# Train weather-enhanced models
python backend\src\train_weather_enhanced_models.py

# Evaluate / visualize model performance
python backend\src\model_performance_visualizations.py

# Integrate METAR weather (requires Internet)
python backend\src\integrate_metar.py

# Simulate weather integration flow
python backend\src\simulate_weather_integration.py

# CLI entrypoint (if provided by your workflow)
python backend\src\main.py
```

Generated outputs will appear under `backend/reports/figures` and `backend/reports/results` as configured by the scripts.

## Data and credentials

- Place CSV inputs in `backend/data`.
- Keep `backend/credentials/kaggle.json` private. Do not commit secrets.

## Frontend

The `frontend/public/index.html` can be opened directly in a browser for a static demo. If you plan to convert to a framework build (e.g., React tooling), initialize a project and move `frontend/src` accordingly.

### Open the frontend report

Option A — Open directly from file system (no server):

1. Navigate to `frontend/public`
2. Double-click `index.html` to open in your default browser

Note: Some browsers restrict local file access for certain features. If something doesn’t render as expected, use Option B.

## Notes

- Python 3.10+ recommended.
- If corporate proxies are used, configure `pip`/`requests` environment variables accordingly.


