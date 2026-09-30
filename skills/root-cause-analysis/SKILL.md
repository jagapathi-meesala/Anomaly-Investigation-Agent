---
name: root-cause-analysis
description: Rank observable contextual factors associated with detected anomalies.
---
# Root Cause Analysis

## Purpose
Identify contextual fields whose values differ around anomalous observations and rank them as candidate explanations.

## Inputs
Use the original records, metric name, value field, and anomaly indices from anomaly detection.

## Processing
Categorical fields are compared through mode differences and numeric fields through relative mean differences. The result is an association ranking rather than a causal claim.

## Outputs
Return candidate factors, association scores, anomalous values, and baseline summaries.

## Limitations
The method cannot establish causality, account for unobserved variables, or infer mechanisms that are absent from the supplied records.

## Expected Behavior
If no anomalies exist, return an empty candidate list. If context is insufficient, return only evidence supported by available fields.
