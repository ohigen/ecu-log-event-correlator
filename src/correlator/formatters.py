from __future__ import annotations

import pandas as pd


def to_timeline_text(df: pd.DataFrame) -> str:
    """
    Format correlated events as a simple timeline text.
    Expected columns: delta_ms, source, event, level, detail
    """
    if df.empty:
        return "(no events in window)"

    lines = []
    for _, r in df.iterrows():
        delta = r["delta_ms"]
        src = r["source"]
        evt = r["event"]
        lvl = r.get("level", "")
        detail = r.get("detail", "")
        lvl_str = f" [{lvl}]" if str(lvl).strip() else ""
        detail_str = f" - {detail}" if str(detail).strip() else ""
        lines.append(f"[{delta:>8.3f} ms] {src}: {evt}{lvl_str}{detail_str}")
    return "\n".join(lines)
