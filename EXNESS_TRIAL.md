# Exness cent trial: MT5-Python-Trading

Only `exness_trial.py` is the guarded live entry point. Original upstream entry points bypass this shared-account trial and must not be used. The shared execution package and tracker live in sibling `Monn/exness_arena`; keep the five forks in sibling folders.

## Enabled deployment

This repo is enabled in the live configuration, with 4 enabled profiles: `crossover`, `smc`, `trend_breakout`, `combined`.

Across the five repos there are 31 enabled profiles (Monn: 8, MT5-Python-Trading: 4, mt5_live_trading_bot: 8, tradingbot: 10, Forex-Trading-Bot: 1). Enabled configuration is not a claim of current process health or profitability. Consult the dashboard for running, quarantined and halted status.

Broker pair discovery is enabled; the current watchlist contains 35 instruments. Inventory refreshes every minute. Compatible strategies scan discovered tradable cent currency, metal and crypto pairs plus the five approved oil/index CFDs: `UKOILc`, `USOILc`, `USTECc`, `US30c`, and `US500c`. Sunrise retains eight pair-specific profiles; Aurum `managed_gold` is gold-only. Disabled/close-only symbols, unapproved non-pair contracts and conversion indicators cannot receive new entries. Monn, MT5-Python-Trading, Aurum (except gold-only `managed_gold`) and SuperTrend include all five CFDs; Sunrise has no original oil/index profile and remains restricted to its eight original instruments. Each CFD signal must still pass broker history, stop valuation, minimum-volume, margin, spread and session/order checks; inclusion does not guarantee an entry. Broker specifications checked on 2026-11-13: oil minimum volume is 0.01; `USTECc`/`US30c` minimum volume is 0.05 and `US500c` is 0.14. Index-specific ceilings are configured at those broker minimums; all other symbols retain the default lot ceiling shown below. Index entries are eligible only when the actual broker-valued stop risk fits the unchanged 3.50 USC per-position ceiling, its existing 10% execution reserve and remaining loss headroom. The guard never rounds volume upward or tightens a strategy stop merely to fit a lot minimum. A later increase in broker minimum volume causes entries to be skipped until explicitly reviewed; ceilings do not rise automatically. Contract specifications can change; the live guard always rechecks broker limits. Missing history is reported per strategy/pair. See `Monn/STRATEGY_PROFILES.md` for strategy magics, pair scopes and execution conventions, and `Monn/exness_arena/compatibility.json` for exclusions. Claude Trader is skipped; EA31337 remains blocked and is not part of this five-repo deployment.

## Current shared trading rules

These rules apply to all five repositories. Numeric values and enabled profiles are rendered from the local live settings; execution semantics are maintained alongside `Monn/exness_arena/guard.py`. USC means US cents (100 USC = USD 1).

| Rule | Current setting |
|---|---|
| Per-position stop-risk ceiling | 3.50 USC for every strategy |
| Combined open-risk cap | Disabled (`total_risk_budget_usc: null`); no combined open-risk cap |
| Default maximum order volume | 0.01 cent lots; unchanged for forex, metals, crypto and oil |
| Index-specific lot ceilings | US30c: 0.05, US500c: 0.14, USTECc: 0.05 cent lots; broker minimum/step still apply |
| Strategy loss budget | 5.2444 USC |
| Repository loss backstop | 5.2444 USC shared by that repo's strategies |
| Account drawdown entry halt | 1% equity decline from the preserved trial baseline |
| Quote age ceiling | 30 seconds |
| Position-count ceiling | None per strategy, pair, repository or account |
| Position-rule scope | Repository + strategy + pair + direction |

A strategy may hold a first buy and first sell on the same pair together. Every additional position in a direction requires **every existing position from that same strategy on that pair and direction** to be individually profitable after swap and known opening fees. Zero, negative or non-finite net profit blocks additions. A profitable basket cannot hide a losing position. Other strategies have independent position rules; an opposite signal does not automatically close existing positions.

Every new entry needs a fresh qualifying closed M15 signal and must fit the per-position ceiling and remaining strategy/repo loss headroom. Sizing reserves 10% for execution drift, rounds volume down and skips signals when the broker's minimum volume cannot fit. Entry margin must not exceed 10% of free margin, and spread must not exceed 15% of stop distance. Equal ceilings do not imply equal exposure or trade counts.

Strategy/repo loss checks use booked deal P&L including swap, commissions and fees since the preserved trial start; they are net-loss thresholds, not gross-loss counters. Profits do not raise the configured ceilings. The account equity gate also includes manual/external positions. Loss gates block new entries; they do not automatically liquidate the book or guarantee a maximum realized loss. Stops may slip or gap.

Every position requires a broker-valued server-side stop. Stop removal/widening, pending entries, upward lot rounding, account switching and changes to sibling-strategy/manual positions are prohibited. Existing manual positions remain outside bot results. All registered trial positions retain ownership and stop validation, including positions from subsequently disabled strategies.

Missing account/history state, unavailable stop valuation, stale quotes, a missing/stale tracker heartbeat (90 seconds), unexpected trial pending orders and ambiguous submissions block new risk. Strategy evaluation failures quarantine only that strategy. Halts, quarantines, loss history and equity baselines never reset automatically on restart or a rule change.

### Stop-loss and take-profit policy

Original protection is used where the source strategy supplies executable price rules. Strategies without standalone price protection retain the explicit existing safety fallback; they are not described as having unique native SL/TP. A missing or invalid supported native stop skips the signal. All levels remain subject to the same broker validation and 3.50 USC risk ceiling; stops are never changed just to force a trade to fit.

| Strategy group | Protection mode for new entries | Source rules and limitations |
|---|---|---|
| Monn | original | All eight configured strategy orders retain their original SL and optional TP, including original fix_order/max_sl_pct configuration. No TP is added when absent. |
| mt5_live_trading_bot | original | All eight Sunrise profiles retain their original stop_level and take_level. |
| Forex-Trading-Bot | original | SuperTrend retains its original average-line TP and reward/1.2 SL formula. |
| tradingbot/donchian | original stop, no fixed TP | Native Donchian state machine exposes its fixed original entry-close +/- stop_atr * ATR(atr_n) stop: defaults 2.5 * ATR(48). Reuse that original signal-entry anchor for additions, not a new ATR stop. Convert mid level to bid/ask trigger using current half-spread. No fixed TP exists, so new orders carry TP=0. Missing/invalid native stops skip entries without fallback. The broker stop can trigger intrabar; upstream state uses closed-bar comparisons. |
| tradingbot/other | explicit protective fallback | ema_cross, tsmom, kalman_trend, zscore_fade, rsi2, bollinger_revert, vol_squeeze, orb and managed_gold expose forecasts/state exits rather than standalone broker SL/TP rules. Retain the existing 2 * ATR(14) SL and 4 * ATR(14) TP. |
| MT5-Python-Trading | explicit protective fallback | crossover, smc, trend_breakout and combined expose direction only. Original multi_symbol_robot sends sl=None/tp=None; its stop_loss_pips is a sizing input, not an attached protection rule. Retain existing 2 * ATR(14) SL and 4 * ATR(14) TP. |
| migration | new entries only | Existing broker positions keep their SL/TP. No stop widening/removal, mass position updates, forecast/time/channel liquidation, risk-budget change, halt reset, ownership change or decision replay. Dynamic/signal exits are not represented as invented static TP prices. |

Every strategy has a stable identity and magic in `Monn/exness_arena/registry.json`. The shared journal attributes deals and positions by original opening ownership and stable position ID, including partial closes and manual exits. Results remain separate by repository and strategy. The tracker exports `results.csv`, `strategies.csv` and `positions.csv` under the local `Monn/.exness-arena/` directory.

## Research logging and shadow testing

The local `Monn/.exness-arena/research.sqlite3` records durable decisions (including no-signal outcomes), exact compressed closed-bar inputs, quotes/contracts, available features, blocked proposals, code/configuration/dependency/artifact versions and sampled live trade paths. New live trades are linked by their actual opening order/deal; older unmatched versions remain unknown. The live journal and ownership records remain separate.

Paper-only shadows compare the proposed exit with 1R and 3R targets using the same stop and risk-sized volume, with a 24-hour elapsed-time horizon checked on eligible closed bars. They continue observing proposals while the live drawdown halt remains enforced. These are independent per-signal counterfactuals, not a portfolio simulation: they do not simulate live loss/addition gates. Results include spread but exclude fees, swap and extra slippage. Conservative OHLC handling and sampled paths limit precision. No variant changes live parameters or places an order. See `Monn/RESEARCH.md` for schemas, methodology, limitations and export commands. The dashboard and `/api/research` show paper results separately from live performance.

## Operation and documentation

Dashboard: http://127.0.0.1:8765 . Runtime settings, account pins, credentials, baseline and journal stay local in `Monn/.exness-arena/` and are excluded from Git. The local settings are authoritative; these guides intentionally omit account identifiers and credentials.

Use `Monn/restart_exness_trial.ps1` for preflight and a controlled restart that preserves broker positions, ownership and loss records. With `Monn` on `PYTHONPATH`, `python -m exness_arena.control pause` blocks new entries and exits strategy runners; server-side stops remain and the tracker continues. Keep Windows and MT5 running. There is no automatic restart or automatic halt reset.

Whenever trading rules change, update their implementation and this shared policy template, render all five guides with `python Monn/sync_trading_docs.py`, and verify `python Monn/sync_trading_docs.py --check` against the live settings. Update `Monn/STRATEGY_PROFILES.md` and compatibility/registry details when strategy scope changes. Confirm the live dashboard agrees with the intended policy before reporting deployment complete. Commit and push the documentation with the rule change; never publish private runtime files.
