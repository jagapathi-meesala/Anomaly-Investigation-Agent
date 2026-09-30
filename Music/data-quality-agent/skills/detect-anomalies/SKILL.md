---
name: detect-anomalies
description: Detect unusually distant numeric observations using z-scores.
---
# Detect Anomalies

## Purpose
Identify numeric observations that cross a caller-selected z-score threshold.

## Inputs
Records, a non-empty list of numeric field names, and an optional positive threshold.

## Processing
Compute the population mean and standard deviation for usable numeric values and compare each numeric observation with the threshold.

## Outputs
Return anomaly count and row, field, value, z-score, and threshold for each finding.

## Limitations
The method can be weak for skewed distributions and cannot detect anomalies when a field has zero variance.

## Expected Behavior
Use only values present in the supplied records and never manufacture observations.
