# Anomaly Investigation Agent

A framework-independent Python agent for investigating unusual observations in structured time-series or event data.

## Purpose
The agent detects statistical anomalies, ranks observable contextual factors associated with anomalous records, and produces a structured report that distinguishes evidence from candidate explanations.

## Architecture
- `core/`: orchestration and dynamic tool registry.
- `contracts/`: framework-neutral tool metadata, validation, execution, and error contracts.
- `tools/`: deterministic domain implementations plus MCP-compatible YAML descriptions.
- `skills/`: Agent Skills-compatible capability instructions.
- `adapters/`: neutral adapter boundary for OpenAI, CrewAI, Claude Code, and Lyzr hosts.
- `config/`: environment-backed runtime settings.
- `verification/`: readiness and manifest validation assets.

## Installation
Use Python 3.10+ and install `requirements.txt` in an isolated environment.

```bash
python -m pip install -r requirements.txt
```

## Configuration
Runtime values are read from environment variables. Supported variables are `AGENT_LOG_LEVEL`, `AGENT_MAX_ROWS`, `AGENT_Z_SCORE_THRESHOLD`, `AGENT_IQR_MULTIPLIER`, and `AGENT_MAX_CANDIDATES`.

## Tools
1. `detect-anomalies` — IQR and z-score detection.
2. `investigate-root-cause` — observable contextual association ranking.
3. `build-anomaly-report` — structured evidence report.

## Skills
- `anomaly-detection`
- `root-cause-analysis`
- `anomaly-reporting`

## Usage
```python
from core.agent_core import AnomalyInvestigationAgent
agent = AnomalyInvestigationAgent()
result = agent.investigate(
    rows=[
        {"timestamp": "2026-01-01", "value": 10, "service": "api"},
        {"timestamp": "2026-01-02", "value": 11, "service": "api"},
        {"timestamp": "2026-01-03", "value": 10, "service": "api"},
        {"timestamp": "2026-01-04", "value": 100, "service": "worker"},
    ], metric="latency_ms")
```

## Testing
Run `pytest -q` and `python verification/readiness_audit.py`. The suite covers tools, contracts, registry behavior, adapters, security, documentation, and OpenGAP manifest rules.

## Portability
The core is independent of OpenAI, Claude, CrewAI, and Lyzr SDKs. Four adapter classes expose a common invocation boundary; they are integration points, not vendor certification.

## Limitations
The statistical methods identify unusual observations and contextual associations. They do not prove root cause, retrieve external telemetry, model complex seasonality, or perform autonomous remediation.

## OpenGAP
The manifest targets OpenGAP/gitagent specification `0.1.0` and uses schema-supported properties documented by the inspected official specification.
