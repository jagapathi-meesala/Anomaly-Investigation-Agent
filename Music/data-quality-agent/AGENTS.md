# AGENTS.md

## Operating Model

This repository defines a framework-independent Data Quality Agent. Runtime orchestration should discover tools through `core.agent_core.ToolRegistry` and execute them through their framework-neutral contract.

## Integration Boundary

OpenAI SDK, CrewAI, Claude Code, and Lyzr integrations are represented by adapter interfaces in `adapters/`. These classes delegate to the same registry and do not make a claim that the external framework SDK is installed or tested.

## Change Discipline

Changes to a tool must update its tests and its skill documentation when behavior changes. Do not add runtime secrets or framework-specific dependencies to the core.
