---
name: anomaly-detection
description: Detect unusual numeric observations using robust statistical evidence.
---
# Anomaly Detection

## Purpose
Detect unusual observations in a supplied numeric series without assuming a particular model framework.

## Inputs
- A list of records containing a numeric value field.
- A metric label and optional value-field name.

## Processing
The skill computes the mean, population standard deviation, quartiles, IQR bounds, and absolute z-scores. An observation is flagged when it breaches the IQR fence or the configured z-score threshold.

## Outputs
Return anomaly indices, original records, evidence types, severity, and descriptive statistics.

## Limitations
This is statistical outlier detection, not proof of an operational incident. Small samples, non-stationary series, seasonality, and legitimate step changes can produce false positives.

## Expected Behavior
Reject malformed records and oversized inputs. Never silently coerce non-numeric values into numbers.
