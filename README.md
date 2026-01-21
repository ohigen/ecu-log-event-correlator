# ECU Log Event Correlator

A small, self-contained Python tool that demonstrates how to correlate ECU log events across multiple sources using timestamps.

In production environments, commercial tools are typically used. This project focuses on a lightweight, tool-agnostic approach to quickly answer:

“What happened before or after this event across multiple logs?”

Note: All logs in this repository are synthetic and do not represent any proprietary system.

---

## Features

* Correlates events across multiple CSV logs around a specified anchor event
* Extracts events within a configurable +/- time window
* Produces a unified, time-aligned timeline for investigation
* Optional CSV output for further analysis

---

## Input Format

CSV columns:

* ts_ns (required): timestamp in nanoseconds
* event (required): event name
* level (optional)
* detail (optional)

---

## Quick Start

Install dependencies:

pip install -r requirements.txt

Run correlation:

python cli.py 
--logs data/ecu_a_log.csv data/ecu_b_log.csv 
--anchor FAULT_SET 
--window-ms 100

---

## Example Output

[ -50.000 ms] ecu_a_log: STATE_CHANGE [INFO] - IDLE->ACTIVE
[   0.000 ms] ecu_b_log: FAULT_SET [ERROR] - DTC=P0123
[  10.000 ms] ecu_a_log: RESET_REQUEST [WARN] - triggered by watchdog

---

## Typical Use Cases

* Debugging cross-ECU behaviors by correlating events around a fault trigger
* Investigating timing and ordering of events during bench or vehicle testing
* Supporting fast, repeatable triage workflows outside of proprietary toolchains

---

## Design Notes

* The implementation is intentionally kept small and readable
* Timestamp-based correlation is used to remain independent of specific vendors or tools
* The structure mirrors common system-level debugging workflows in automotive environments

This repository reflects practical investigation and debugging approaches commonly used in production automotive systems.
