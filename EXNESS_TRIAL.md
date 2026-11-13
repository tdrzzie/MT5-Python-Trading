# Exness cent trial: MT5-Python-Trading

Reserved magic: **26111302**. Only `exness_trial.py` is the guarded trial entry point. Original entry points are not approved for this shared-account trial.

The shared package and tracker live in the sibling `Monn/exness_arena` directory. Clone these forks as sibling folders. The launcher sets the repo identity before importing trading modules. Runtime account pins, initial equity, risk budgets, journal and credentials are excluded from Git.

Status: closed-bar adapter implemented; must pass read-only preflight and shared safety tests before activation.

Guarded strategy adapters use the original strategy classes: Monn MACross (10/20 SMA, 100-SMA and candle filters), or MT5-Python-Trading CrossOverStrategy (20/50 SMA). Both use closed M15 bars on EURUSDc and XAUUSDc. Monn retains its configured 0.25% price stop; the crossover adapter adds a mandatory 2-ATR stop and 2R target because the original multi-symbol runner sends no stop. These adapters are distinct experiment configurations, not an unmodified upstream performance claim.

Shared limits: fixed stop-risk cap of 0.10% of starting account equity per ready bot; reserve 10% for execution drift; one position per bot; total stop-risk cap 0.20%; per-bot cumulative loss budget 0.50%; account-wide equity decline gate 1%; at most 10 entries per bot; maximum 0.10 cent lots per order. Skip if minimum volume exceeds budget. No pending orders, stop removal, stop widening, or cross-bot position changes. No upward rounding or account switching. Missing account state, stale quotes/tracker, and unknown order results block new entries.

The account-wide gate includes external position P&L and is an entry halt, not a guaranteed loss ceiling or automatic liquidation. Stop gaps/slippage can exceed estimated risk. Existing positions are excluded from bot results. Equal risk caps do not guarantee equal exposure or trade counts. Sampled drawdown is measured every 10 seconds. No API costs are incurred by the two initial rule-based adapters.

From the workspace parent, use the isolated Python environment and the scripts in `Monn/exness_arena`. Dashboard: http://127.0.0.1:8765 . Run `python -m exness_arena.control pause` with `Monn` on PYTHONPATH to stop new entries and exit runners without closing positions. Tracker remains read-only and continues reporting. There is no automatic restart or automatic halt reset. Keep Windows and MT5 running.
