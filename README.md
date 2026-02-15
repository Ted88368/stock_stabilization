# Stock Stabilization Monitoring Skill

This OpenClaw skill monitors HK, US, and A-share stocks to detect if their price has stabilized (企稳). It uses the `kdata` library for data acquisition and analyzes price consolidation, volume trends, and moving averages.

## Project Structure

- `SKILL.md`: Skill definition and SOPs for OpenClaw.
- `scripts/main.py`: The entry point script that orchestrates data fetching and analysis.
- `scripts/stabilization.py`: Core logic for detecting stabilization patterns.
- `libs/`: Directory for the `kdata` wheel file (`kdata-3.0.3-py3-none-any.whl`).
- `SKILL.md`: Skill definition and SOPs for OpenClaw.
- `scripts/main.py`: The entry point script that orchestrates data fetching and analysis.
- `scripts/stabilization.py`: Core logic for detecting stabilization patterns.
- `libs/`: Directory for the `kdata` wheel file (`kdata-3.0.3-py3-none-any.whl`).
- `pyproject.toml`: Project configuration and dependencies managed by `uv`.

## Detection Logic

The skill evaluates stabilization based on four primary factors:
1.  **Price Consolidation**: Checks if the price has moved within a narrow range (e.g., < 5%) over the last 10 days.
2.  **Volume Trend**: Verifies if selling pressure has decreased (low volume relative to average).
3.  **MA Flattening**: Checks if short-term moving averages (5-day vs 10-day) are converging/flattening.
4.  **Trend Support**: Checks if the price is holding above key levels (e.g., 20-day SMA).

## Usage

### 1. Installation
The project uses `uv` for dependency management. To sync and install:
```bash
uv sync
```

### 2. Running the Monitor
Run the analysis for a specific stock using `uv run`:

- **Hong Kong**: `uv run scripts/main.py hk.0700`
- **US Stocks**: `uv run scripts/main.py us.AAPL`
- **A-Shares**: `uv run scripts/main.py sh.600000` or `sz.000001`

## Deployment

The skill checks for the `K_DATA_CENTER` environment variable. If it is not set, it defaults to `/opt/kdata_data`. To override this, set the variable in your environment:

```bash
export K_DATA_CENTER="/your/custom/path"
```

## Customization
You can adjust the stabilization thresholds (e.g., the 5% consolidation range) in `scripts/stabilization.py`.


