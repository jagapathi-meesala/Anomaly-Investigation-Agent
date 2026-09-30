---
name: validate-data
description: Validate records against explicit quality rules.
---
# Validate Data

## Purpose
Check caller-supplied quality constraints without inventing missing rules.

## Inputs
Records plus optional required fields, numeric ranges, allowed values, and email fields.

## Processing
Apply each supplied rule to each record and preserve row and field locations for violations.

## Outputs
Return validity, checked row count, violation count, and structured violations.

## Limitations
Email validation is intentionally lightweight and rules are limited to those supplied by the caller.

## Expected Behavior
Malformed rule structures are rejected rather than silently reinterpreted.
