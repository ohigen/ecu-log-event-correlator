from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List
import pandas as pd


@dataclass(frozen=True)
class SourceLog:
    name: str
    df: pd.DataFrame  # columns: ts_ns, event, level, detail


def _find_anchor_times(df: pd.DataFrame, anchor_event: str) -> List[int]:
    return df.loc[df["event"] == anchor_event, "ts_ns"].astype("int64").tolist()


def correlate(
    logs: Iterable[SourceLog],
    anchor_event: str,
    window_ms: float,
    occurrence: int = 1,
) -> pd.DataFrame:
    """
    Correlate events across multiple logs around an anchor event.

    - anchor_event: event name to anchor on (e.g., FAULT_SET)
    - window_ms: include events within +/- window_ms
    - occurrence: 1-based index of anchor occurrence (e.g., 1 => first anchor)
    """
    logs = list(logs)
    if not logs:
        raise ValueError("No logs provided")

    # Pick the first log that contains the anchor
    anchor_ts = None
    anchor_src = None
    for log in logs:
        times = _find_anchor_times(log.df, anchor_event)
        if len(times) >= occurrence:
            anchor_ts = times[occurrence - 1]
            anchor_src = log.name
            break

    if anchor_ts is None:
        raise ValueError(f"Anchor event '{anchor_event}' not found in provided logs")

    window_ns = int(window_ms * 1e6)
    t_min = anchor_ts - window_ns
    t_max = anchor_ts + window_ns

    rows = []
    for log in logs:
        w = log.df[(log.df["ts_ns"] >= t_min) & (log.df["ts_ns"] <= t_max)].copy()
        if w.empty:
            continue
        w["source"] = log.name
        w["delta_ms"] = (w["ts_ns"] - anchor_ts) / 1e6
        rows.append(w)

    if not rows:
        # No events in window
        return pd.DataFrame(columns=["delta_ms", "source", "event", "level", "detail", "ts_ns"])

    out = pd.concat(rows, ignore_index=True)
    out = out.sort_values(["delta_ms", "source", "event"]).reset_index(drop=True)

    # Helpful metadata (not required)
    out.attrs["anchor_ts_ns"] = anchor_ts
    out.attrs["anchor_event"] = anchor_event
    out.attrs["anchor_source"] = anchor_src

    return out
