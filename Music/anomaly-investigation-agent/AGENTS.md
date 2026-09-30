# Agents

## Operating Instructions
Use the repository manifest, SOUL.md, RULES.md, DUTIES.md, and skill documents as the behavioral contract. Invoke domain tools through their framework-independent contracts rather than embedding vendor-specific logic in the core.

## Execution Pattern
1. Validate the request.
2. Detect statistical anomalies.
3. If anomalies exist, rank observable contextual associations.
4. Build a traceable report.
5. State limitations and avoid causal overclaiming.

## Portability
The core can be wrapped by OpenAI, CrewAI, Claude Code, or Lyzr adapters, but those adapters intentionally contain no vendor SDK code in this repository. End-to-end vendor compatibility must be tested by the integrating environment before being claimed.
