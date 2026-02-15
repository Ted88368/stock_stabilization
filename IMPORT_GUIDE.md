# How to Import into OpenClaw

To use this stock stabilization skill within your OpenClaw environment, follow these steps:

## 1. Clone or Copy the Skill
Ensure the entire `stock_stabilization` directory is accessible by your OpenClaw agent.

## 2. Configure OpenClaw
OpenClaw typically loads skills by scanning a specific directory or by being pointed directly to a `SKILL.md` file.

### Option A: Local Skill Directory
If you have a local OpenClaw workspace, add the path to this directory in your agent's configuration:

```bash
# Example configuration in your OpenClaw environment
# skills_path: ["/path/to/your/skills", "/Users/hy/wk/github/stock_stabilization"]
```

### Option B: Direct Import
If your OpenClaw version supports individual skill loading, point it to the `SKILL.md` file:

```bash
openclaw load-skill /Users/hy/wk/github/stock_stabilization/SKILL.md
```

## 3. Verify Dependencies
OpenClaw will need to execute the Python scripts. Ensure `uv` is installed on the host machine where OpenClaw runs. The skill handles its own environment via `uv run`.

## 4. Usage in Chat
Once imported, you can talk to OpenClaw like this:
- "帮我监控港股 0700.HK" (Add to watchlist)
- "生成昨天的港股企稳报告" (Run report hk)
- "移除美股 TSLA" (Remove from watchlist)

The agent will use the SOPs defined in `SKILL.md` to call the appropriate commands.
