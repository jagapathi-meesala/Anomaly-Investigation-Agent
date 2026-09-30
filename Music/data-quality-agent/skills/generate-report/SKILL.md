---
name: generate-report
description: Combine data quality findings into a deterministic report.
---
# Generate Report

## Purpose
Aggregate profiling, validation, and anomaly results into one inspectable quality report.

## Inputs
Three structured result objects: `profile`, `validation`, and `anomalies`.

## Processing
Combine row counts and detected issue counts into a deterministic score and status while preserving source results.

## Outputs
Return status, quality score, counts, and the original component results.

## Limitations
The score is an indicator of detected issues, not a guarantee of business or regulatory fitness.

## Expected Behavior
Reject missing or non-object component results and preserve the supplied evidence.
