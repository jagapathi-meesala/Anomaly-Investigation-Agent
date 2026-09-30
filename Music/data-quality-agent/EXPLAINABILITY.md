## Inputs and Data Sources

The agent accepts structured records supplied directly to its tools, together with validation rules such as required fields, allowed values, numeric ranges, and selected numeric fields. Data sources are therefore caller-provided records rather than an implicit database, network service, or hardcoded dataset, and the input mechanism is a framework-independent Python mapping.

The profiling tool uses the supplied records to calculate completeness, distinctness, observed Python-level types, and basic numeric statistics. The validation, anomaly detection, and reporting tools consume the same structured results and do not silently fetch external data.

### Input Requirements

Each record must be an object, and an input dataset must contain at least one record. Optional rules must use the documented object and array shapes so malformed requests are rejected instead of being interpreted loosely.

### Failure Handling

Invalid top-level arguments, malformed records, missing required tool arguments, and invalid rule configurations are rejected with structured tool errors. Tool execution failures are converted by the registry into an object containing `ok: false`, the tool name, and an error message.

## Decision and Reasoning

The agent decides data-quality findings by applying explicit deterministic rules rather than inventing a quality judgment. Required-field violations are identified when values are missing, range violations compare numeric values with caller-supplied bounds, allowed-value checks compare values against caller-supplied sets, and anomaly detection flags numeric values whose absolute z-score reaches the configured threshold.

The quality report combines the observed row count, validation violation count, and anomaly count into a deterministic quality score and status. A dataset with no detected violations or anomalies receives a `pass` status; otherwise the report uses `review`, while preserving the underlying findings so a human can inspect the evidence.

### Rules Applied

Profiling computes missing rate and unique rate from the records actually supplied. Anomaly detection uses population standard deviation and does not report a z-score when the numeric field has fewer than two usable values or zero variance.

### Expected Outputs

Every successful tool returns an object with `ok: true` and structured domain results. Validation returns individual violations, anomaly detection returns row and field findings, profiling returns per-column statistics, and reporting preserves the component results inside the final report.

### Worked Example

For records containing `age` values 20, 21, and 200, a caller can request anomaly detection for `age` with a z-score threshold. The tool evaluates those actual values and returns any observation that crosses the configured threshold instead of returning a predetermined example result.

## Limits and Constraints

The agent does not establish statistical causation, business correctness, or domain-specific truth from generic records. Its checks are limited to the rules supplied by the caller and the deterministic heuristics implemented by the individual tools, so a clean report does not prove that a dataset is fit for every downstream use.

The current implementation does not connect to databases, cloud storage, external APIs, or model providers, and it does not inspect arbitrary filesystem paths as part of normal tool execution. Email validation is intentionally lightweight, and z-score detection can miss anomalies when distributions are highly skewed or when the field has insufficient variance.

### Constraints

Runtime configuration is read from environment variables and is not embedded as production credentials or secret values. The core agent depends only on the local tool contract and registry, so framework-specific SDKs are deliberately outside the core implementation.

### Unsupported Behavior

The agent does not claim framework execution merely because adapter classes exist; those adapters provide a common invocation boundary and require the target framework to be integrated separately. It also does not claim HiDevs or OpenGAP CLI verification unless the corresponding external validation command actually succeeds.
