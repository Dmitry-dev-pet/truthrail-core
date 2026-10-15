# Truthrail boundaries v0.3

Truthrail has four separate concerns. Keeping them separate is a compatibility and
security property, not only a code-organization preference.

```text
assistant profile
      |
      v
private Truthrail instance
      |
      v
Truthrail Core
      |
      v
capabilities / reviewed control planes
```

## 1. Assistant profile

The assistant profile describes identity and behavior:

- display name and role;
- goals and attention policy;
- enabled skill **IDs**;
- behavioral rules.

It does not own protocol implementation, credential values, runtime topology, workflow
paths, issue triggers, runner labels, or operation contracts. A skill ID is resolved by
Truthrail Core or the host integration.

Renaming an assistant never changes authority.

## 2. Private Truthrail instance

A private instance owns user-specific durable state and routing overlays:

- project inventory and aliases;
- durable context, decisions, goals and constraints;
- assistant profile;
- capability references and credential metadata;
- run-ledger state and references to authoritative systems.

An instance may keep host-specific adapters needed by a consumer, but it must
not maintain an independent copy of the Truthrail protocol implementation or portable
schemas. Freshness-sensitive state remains authoritative in the live target system.

## 3. Truthrail Core

Core owns portable mechanism:

- protocol schemas and semantic validation;
- execution-level and lifecycle semantics;
- portable assistant skills;
- instance validation/bootstrap rules;
- capability routing/admission/policy helpers;
- compatibility adapters.

The Python implementation and import namespace is `truthrail_core`. The supported
command-line interface is `truthrail`. Keep one canonical implementation.


## 4. Capabilities and control planes

Capabilities own the concrete operation surface. A reviewed control plane publishes its
live operation contract, including admission, execution venue, required permissions and
verification evidence.

Core routes to capabilities; it does not copy their operation lists. Assistant profiles
do not hard-code their workflow paths or triggers.

## Canonical implementation

The public Core contains one Python package and one set of versioned schemas.
Private instances retain user-specific state and adapters; they do not fork Core.
The old technical aliases were retired in the 0.5.0 migration. Projects pinned
to earlier versions must update imports and configuration deliberately.

## Lifecycle invariant

Boundary cleanup does not change the execution lifecycle:

```text
executing -> executed -> verifying -> verified
```

`executed` records that an executor completed its operation. Only independent
acceptance evidence may move the run to `verified`.
