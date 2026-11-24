# Contributing

Thanks for helping improve AgentSec. Keep changes focused and preserve the
reproducibility and provenance of existing research artifacts.

## Development workflow

1. Create a feature branch from `main`; do not push directly to `main`.
2. Make one focused change per pull request.
3. Add or update tests for behavior you change. Prefer deterministic, offline
   tests; live-provider tests must be explicitly opted into and must not be
   required in CI.
4. Update the relevant project README or documentation when commands,
   behavior, limitations, or scenario coverage change.
5. Never commit API keys, populated `.env` files, or other credentials.
6. Put new research results under `research/`. Do not overwrite or alter
   existing raw data, published results, or their reproducibility references.

From the repository root, install the local projects, run the tests and
scenario validation, and launch the integrated demo:

```powershell
uv sync
uv run python scripts/agentsec.py test
uv run python scripts/agentsec.py validate
uv run python scripts/agentsec.py demo
```

The default test and demo paths are local and do not call paid APIs. Live model
comparisons require the explicit `--live` option; see the root README.

## Pull request checklist

- [ ] Tests pass for the changed project; run the root test command for
  cross-project changes.
- [ ] Run `uv run python scripts/agentsec.py validate` when scenario ground
  truth, mappings, or demo behavior changes.
- [ ] Documentation reflects any user-visible changes and does not overstate
  security capabilities or scenario coverage.
- [ ] No credentials, generated demo outputs, or unintended research-result
  changes are included.
- [ ] Any live API or external-service verification is clearly identified;
  ordinary tests remain offline and do not incur charges.
