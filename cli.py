from __future__ import annotations

import argparse
from pathlib import Path

from src.correlator.io import load_log_csv
from src.correlator.correlate import SourceLog, correlate
from src.correlator.formatters import to_timeline_text


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="ECU Log Event Correlator")
    p.add_argument("--logs", nargs="+", required=True, help="List of CSV log files")
    p.add_argument("--names", nargs="*", default=None, help="Optional names for logs (same order as --logs)")
    p.add_argument("--anchor", required=True, help="Anchor event name (e.g., FAULT_SET)")
    p.add_argument("--window-ms", type=float, default=100.0, help="Correlation window in ms (+/-)")
    p.add_argument("--occurrence", type=int, default=1, help="Anchor occurrence index (1-based)")
    p.add_argument("--out", default=None, help="Optional output CSV path")
    p.add_argument("--format", choices=["text", "csv"], default="text", help="Output format")
    return p.parse_args()


def main() -> int:
    args = parse_args()
    log_paths = [Path(p) for p in args.logs]

    if args.names and len(args.names) != len(log_paths):
        raise ValueError("--names must have the same length as --logs")

    logs = []
    for i, p in enumerate(log_paths):
        name = args.names[i] if args.names else p.stem
        df = load_log_csv(p)
        logs.append(SourceLog(name=name, df=df))

    df_out = correlate(
        logs=logs,
        anchor_event=args.anchor,
        window_ms=args.window_ms,
        occurrence=args.occurrence,
    )

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df_out.to_csv(out_path, index=False)

    if args.format == "csv":
        print(df_out.to_csv(index=False), end="")
    else:
        print(to_timeline_text(df_out))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
