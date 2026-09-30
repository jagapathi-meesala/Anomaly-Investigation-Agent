# RULES.md

1. Validate tool arguments before processing records.
2. Never fabricate missing values, source data, or validation results.
3. Never embed secrets, credentials, or private tokens in source code.
4. Do not treat a quality score as proof of business correctness.
5. Return structured errors for malformed requests.
6. Keep framework-specific dependencies outside the core and contracts.
7. Preserve deterministic behavior for identical inputs and rules.
