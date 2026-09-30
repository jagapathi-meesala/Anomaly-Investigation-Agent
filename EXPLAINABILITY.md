# Explainability

## Inputs and Data Sources
The agent accepts structured records supplied directly by the caller, with a numeric metric field and optional contextual fields such as service, region, status, or timestamp. The data source is therefore the caller-provided dataset; the agent does not silently fetch telemetry, credentials, external APIs, or hidden data. Input mechanisms are the framework-neutral tool contract and the adapter request object, both of which validate required fields before execution.

### Input Requirements
Each detection request must contain at least three records, a non-empty metric name, and a numeric value field in every record. Root-cause analysis additionally uses anomaly indices produced by detection and examines only contextual fields actually present in the supplied records.

### Failure Handling
Malformed rows, missing value fields, unexpected fields, non-numeric values, and oversized datasets are rejected with structured validation errors. The agent does not coerce unsafe or ambiguous values merely to make an analysis complete.

## Decision and Reasoning
Anomaly detection uses two independent statistical signals: an interquartile-range fence and an absolute z-score threshold, then records which signal(s) support each flagged observation. Candidate causes are ranked by observable association: numeric context is compared through relative mean differences, while categorical context is compared through mode differences; these scores are evidence rankings, not causal proof.

### Rules Applied
An observation is anomalous when it falls below Q1 minus the configured IQR multiplier times IQR, above Q3 plus that multiplier times IQR, or beyond the configured absolute z-score threshold when the standard deviation is non-zero. A report preserves the original anomaly record, index, value, evidence type, severity, descriptive statistics, candidate causes, and an explicit statement that contextual confirmation is required.

### Expected Outputs
The detection tool returns anomaly records and descriptive statistics. The root-cause tool returns ranked candidate factors, association scores, anomalous values, and baseline summaries, while the reporting tool combines these into a structured investigation report.

### Worked Example
For a series containing a stable baseline and one substantially larger observation, the detector can flag that observation because it breaches the IQR fence and/or z-score threshold. If anomalous rows also consistently show a different service or region value, that contextual field can receive a higher association score, but the report still treats it as a candidate explanation rather than a proven cause.

## Limits and Constraints
The agent cannot establish causality, explain events absent from the supplied data, or independently verify an operational incident. Non-stationarity, seasonality, small samples, legitimate step changes, correlated fields, missing context, and data-quality problems can create false positives or misleading associations.

### Constraints
Runtime limits are controlled through environment variables for maximum rows, statistical thresholds, candidate count, and logging level. The core implementation has no dependency on OpenAI, Claude, CrewAI, Lyzr, or any other model framework, and adapter classes do not claim that vendor SDK integration has been end-to-end tested here.

### Unsupported Behavior
The agent does not retrieve external observability data, perform automated remediation, alter production systems, or infer hidden causes from unstated context. It also does not treat statistical association as proof of causation or invent missing measurements.
