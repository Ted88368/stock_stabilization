# Stock Stabilization Monitoring Skill

This OpenClaw skill monitors HK, US, and A-share stocks to detect if their price has stabilized (企稳). It uses the `kdata` library for data acquisition and analyzes price consolidation, volume trends, and moving averages.

## Project Structure

- `SKILL.md`: Skill definition and SOPs for OpenClaw.
- `scripts/main.py`: The entry point script that orchestrates data fetching and analysis.
- `scripts/stabilization.py`: Core logic for detecting stabilization patterns.
- `libs/`: Directory for the `kdata` wheel file (`kdata-3.0.3-py3-none-any.whl`).
- `SKILL.md`: Skill definition and SOPs for OpenClaw.
- `scripts/main.py`: The entry point script with subcommand support (`add`, `remove`, `report`).
- `scripts/stabilization.py`: Core logic for detecting stabilization patterns.
- `libs/`: Directory for the `kdata` wheel file.
- `watchlist.json`: Persistent list of monitored stocks.
- `pyproject.toml`: Project configuration managed by `uv`.

## Detection Logic

The skill evaluates stabilization based on price consolidation, volume trends, moving averages, and trend support.

## Usage

### 1. Watchlist Management
Add or remove stocks from your daily monitoring list:
```bash
uv run scripts/main.py add hk.0700          # HK
uv run scripts/main.py add sh.600519       # A-share (Shanghai)
uv run scripts/main.py add sz.000001       # A-share (Shenzhen)
uv run scripts/main.py remove us.AAPL      # US
```

### 2. Daily Report
Analyze all stocks or specific markets:
```bash
uv run scripts/main.py report       # All markets
uv run scripts/main.py report hk    # HK only
uv run scripts/main.py report us    # US only
uv run scripts/main.py report as    # A-shares only
```


### 3. Quick Analysis
Analyze a single stock without adding it to the watchlist:
```bash
uv run scripts/main.py us.TSLA
```

## Deployment
Ensure `K_DATA_CENTER` is set, or it defaults to `/opt/kdata_data`.

## Importing to OpenClaw
For detailed instructions on how to use this skill with the OpenClaw agent, see [IMPORT_GUIDE.md](file:///Users/hy/wk/github/stock_stabilization/IMPORT_GUIDE.md).

## Customization
Adjust thresholds in `scripts/stabilization.py`.




