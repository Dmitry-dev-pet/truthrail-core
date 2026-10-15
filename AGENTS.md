# AGENTS.md

## Purpose

This repository is the portable, user-agnostic Truthrail Core reference implementation.

## Reader versus contributor

If a user shared this repository with an AI assistant to understand or adopt Truthrail, the entry point is [AI_START_HERE.md](AI_START_HERE.md). The contribution rules below apply when **modifying Truthrail Core**, not when exploring the user's separate projects. Merely reading this repository does not authorize changes or privileged access.

## Change rules

1. Create a feature branch from current `main`.
2. Keep changes portable: do not add personal repository names, private URLs, real
   credential names, email addresses, account identifiers, or environment-specific
   infrastructure details.
3. Update executable schemas, examples, tests, and protocol documentation together
   when a protocol contract changes.
4. Run the full CI suite.
5. Merge only after CI is green.

## Architectural boundaries

- Assistant profiles own identity, goals, attention policy and skill IDs; they do not own implementation paths, runtime topology or operation contracts.
- Private Truthrail instances own user-specific durable state and routing overlays; they must not grow a second implementation of the portable protocol.
- Truthrail Core owns protocol schemas, semantic validation, portable skills and routing mechanism.
- Capabilities/control planes own concrete operation contracts and verification evidence.
- The only Python implementation namespace is `truthrail_core`; portable skills resolve by stable skill ID.
- Do not duplicate portable logic inside instance repositories or plugin adapters.

See [docs/boundaries-v0.3.md](docs/boundaries-v0.3.md).

## Protocol invariants

- Live target systems outrank cached or conversational state.
- Use the lowest sufficient execution level.
- Privileged operations come from live reviewed control-plane contracts.
- Only operations with `agent_routable: true` are AI-routable.
- Secret values are outside the protocol.
- `executed != verified`.
- Keep handoff packets bounded; do not forward complete chat histories.
- Do not introduce a generic privileged shell or universal executor.

## Versioning and migration

Version 0.5.0 retires historical package, CLI, configuration and schema-URN aliases.
Existing integrations pinned to earlier versions require an explicit migration before
updating their dependency. Document any breaking protocol identifier change and verify
all schemas, examples, skills, tests and downstream consumers together.
