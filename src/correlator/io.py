from __future__ import annotations

from pathlib import Path
import pandas as pd


REQUIRED_COLS = {"ts_ns", "event"}


def load_log_csv(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = [c.strip().lstrip("\ufeff") for c in df.columns]

    missing = REQUIRED_COLS - set(df.columns)
    if missing:
        raise ValueError(f"{path} missing required columns: {sorted(missing)}")

    df["ts_ns"] = pd.to_numeric(df["ts_ns"], errors="coerce")
    df = df.dropna(subset=["ts_ns"]).copy()
    df["ts_ns"] = df["ts_ns"].astype("int64")

    # Optional columns for nicer output
    for col in ["level", "detail"]:
        if col not in df.columns:
            df[col] = ""

    return df.sort_values("ts_ns").reset_index(drop=True)
