# How to Import into OpenClaw

To use the **Stock Stabilization** skill within your OpenClaw environment, follow these steps to integrate, configure, and operate the tool.

---

## 1. Prerequisites

Before importing, ensure your host machine (where OpenClaw runs) meets the following requirements:
- **`uv` Package Manager**: The skill manages its Python environment via `uv run`. Ensure `uv` is installed and accessible in your system's `PATH`.

## 2. Clone or Copy the Skill

Ensure the entire `stock_stabilization` directory is accessible by your OpenClaw agent either locally or via a mounted volume.

## 3. Configure OpenClaw

OpenClaw typically loads skills by scanning a specific directory or by being pointed directly to a `SKILL.md` file.

### Option A: Local Skill Directory
If you have a local OpenClaw workspace, add the path to this directory in your agent's configuration file (e.g., `config.yaml`):

```yaml
# Example configuration in your OpenClaw environment
skills_path: 
  - "/path/to/your/skills"
  - "/absolute/path/to/stock_stabilization" # Update this path
```

### Option B: Direct Import
If your OpenClaw version supports individual skill loading via CLI, point it directly to the `SKILL.md` file:

```bash
openclaw load-skill /absolute/path/to/stock_stabilization/SKILL.md
```

## 4. Environment Variables Configuration

The skill relies on specific environment variables for data fetching and notification delivery. These must be configured in your OpenClaw environment (e.g., in your main project's `.env` file):

```env
# Required for Data Fetching
K_DATA_CENTER=/opt/kdata_data
# Optional: Set a custom path for the watchlist to avoid overwrites during skill updates
WATCHLIST_PATH=/absolute/path/to/safe/dir/watchlist.json
LONGPORT_APP_KEY=your_app_key
LONGPORT_APP_SECRET=your_app_secret
LONGPORT_ACCESS_TOKEN=your_access_token
TIINGO_API_KEYS=your_tiingo_api_key
```

## 5. Usage in Chat (SOPs)

Once imported, OpenClaw will use the Standard Operating Procedures (SOPs) defined in `SKILL.md` to trigger the commands. You can interact with the agent natively:

- **Add to Watchlist**: "帮我监控港股 00700.HK" (or "Add Tencent to the watchlist")
- **Run Reports**: "生成今天的港股企稳报告" (or "Generate the HK market report")
- **Remove from Watchlist**: "移除美股 TSLA" (or "Remove Tesla")

The agent will automatically process the request, generate the markdown summaries, and (if supported by the agent's tools) trigger Email/IM pushes for stabilized stocks based on the SOP instructions.
