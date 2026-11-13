# Trading rule documentation

Whenever changing trading rules, risk budgets, loss gates, position/ownership rules or enabled strategy/pair scope, keep the five active repositories' `EXNESS_TRIAL.md` files and `Monn/STRATEGY_PROFILES.md` aligned with the deployed local settings and shared execution guard. This is a standing user instruction.

The active sibling repositories are Monn, MT5-Python-Trading, mt5_live_trading_bot, tradingbot (Aurum), and Forex-Trading-Bot. Maintain shared policy wording in `Monn/sync_trading_docs.py`; run `python Monn/sync_trading_docs.py` from the workspace parent, then `python Monn/sync_trading_docs.py --check`. Update the strategy catalog, registry and compatibility details when relevant. Review execution semantics against the actual guard; generation checks settings and template consistency, not code behavior. Verify live dashboard settings and health before claiming a rule change is deployed. Commit and push affected docs alongside the implementation.

Never commit credentials, account identifiers, runtime settings, journals or live position data. Documentation work must not reset loss history, equity baselines, ownership or halts, restart bots, or change live rules.
