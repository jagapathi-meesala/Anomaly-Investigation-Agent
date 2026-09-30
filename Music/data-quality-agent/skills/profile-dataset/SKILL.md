---
name: profile-dataset
description: Profile structured records for completeness, uniqueness, types, and numeric statistics.
---
# Profile Dataset

## Purpose
Profile caller-provided records without fetching external data.

## Inputs
A non-empty `records` array containing objects.

## Processing
Calculate row and column counts, missingness, distinctness, observed types, and numeric min/max/mean where applicable.

## Outputs
Return a structured object containing `ok`, row count, column count, and per-column profiles.

## Limitations
The profile describes supplied records only and does not establish business correctness.

## Expected Behavior
Reject malformed records and produce deterministic results for identical input records.
