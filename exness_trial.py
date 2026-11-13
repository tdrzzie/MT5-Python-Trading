"""Guarded Exness cent trial entry point. See EXNESS_TRIAL.md."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "Monn"))
from exness_arena.runner import main

if __name__ == "__main__":
    main('MT5-Python-Trading')
