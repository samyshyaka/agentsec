# AgentSec examples

The API-key-free end-to-end demonstration is run from the repository root:

```powershell
uv sync
uv run python scripts/agentsec.py demo
```

For the synthetic bank, hospital and municipal utility scenarios:

```powershell
uv run python scripts/agentsec.py blueprints
```

The demo uses scripted agents and mock tool callbacks. It does not contact
external services or operate real infrastructure. Its Scorecard number is a
measure of the current Bench scenario signals, not a certification or a
protection guarantee.
