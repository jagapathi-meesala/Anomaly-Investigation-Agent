---
name: anomaly-reporting
description: Convert statistical evidence and candidate causes into a structured investigation report.
---
# Anomaly Reporting

## Purpose
Produce a consistent report that preserves anomaly evidence and clearly separates observations from candidate explanations.

## Inputs
The report requires a metric name, detected anomaly records, and ranked candidate causes.

## Processing
The skill counts anomalies by severity and combines detection evidence with association findings. It explicitly states that candidate causes require contextual confirmation.

## Outputs
Return a structured summary, counts, candidate causes, anomaly details, and a confidence limitation note.

## Limitations
The report is only as complete as the supplied observations and contextual fields. It does not independently retrieve telemetry or verify external events.

## Expected Behavior
Do not invent causes, missing data, timestamps, or external evidence.
