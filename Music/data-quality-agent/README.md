# Data Quality Agent

A portable Python implementation for deterministic dataset profiling, rule-based validation, numeric anomaly detection, and structured quality reporting.

## Architecture

`DataQualityAgent` uses a dynamic `ToolRegistry`, a framework-independent `Tool` contract, and adapter boundaries for OpenAI SDK, CrewAI, Claude Code, and Lyzr. Domain behavior lives in small tools under `tools/`; reusable behavior is documented under `skills/`.

## Installation

Use Python 3.10+ and install the pinned development dependencies from `requirements.txt`:

```bash
python -m pip install -r requirements.txt
```

## Configuration

Runtime settings are environment-backed. Copy `.env.example` into your environment and provide concrete values without committing secrets.

## Tools

- `profile-dataset` — field-level completeness, distinctness, type, and numeric statistics.
- `validate-data` — required fields, numeric ranges, allowed values, and lightweight email checks.
- `detect-anomalies` — deterministic numeric z-score anomaly detection.
- `generate-quality-report` — combines component results into a structured report.

## Skills

- `profile-dataset`
- `validate-data`
- `detect-anomalies`
- `generate-report`

## Usage

```python
from core.agent_core import DataQualityAgent

agent = DataQualityAgent()
result = agent.execute("profile-dataset", {"records": [{"id": 1, "age": 20}, {"id": 2, "age": 21}]})
print(result)
```

## Testing

Run `pytest -q` and `python verification/readiness_audit.py`.

## Portability

The core contract does not import OpenAI, CrewAI, Anthropic, Lyzr, LangChain, or other agent frameworks. Adapter classes expose the same registry boundary to four named integration targets without claiming that those SDKs are installed.

## Limitations

The implementation works on structured records supplied by the caller. It does not connect to external databases or APIs, and its quality score is a deterministic indicator of detected issues rather than proof of business correctness.

## OpenGAP

The root manifest declares OpenGAP `0.1.0` and references only files that exist in this repository. External CLI validation is reported separately from local tests and readiness checks.
