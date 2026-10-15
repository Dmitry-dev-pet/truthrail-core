# Portable skill audit — Truthrail Core 0.5.0

Truthrail's portable skills are instructions and routing contracts, not executors or authorization.

## Canonical registry

The bundle `skills/default-assistant.yaml` contains nine stable skill IDs:

| Group | Skills |
| --- | --- |
| Default | `rebuild-context`, `recent-activity`, `capability-route`, `orchestrate-action` |
| Setup | `bootstrap-instance` |
| Optional | `activate-capability`, `attention-inbox`, `daily-brief`, `quota-guard` |

Every ID must have exactly one `skills/<id>/SKILL.md` with matching YAML
frontmatter `name` and a non-empty description and body. Undeclared or missing
skills are errors.

## Behavioral boundaries

- A public Core link provides instructions, never credentials or write permission.
- An installed skill does not guarantee that any provider connection is active.
- Writes require explicit user authorization for the operation and target, plus the
  live capability or reviewed control-plane contract and provider permissions.
- Routes prefer the least privileged ready capability; a missing tool must not cause
  silent escalation to unrestricted shell, credentials or a different account.
- Freshness-sensitive facts must be verified against their owning provider.
- Successful execution is not accepted completion until the acceptance evidence
  is checked independently. Never promote `executed` directly to `verified`.
- No skill stores or forwards credential values or whole chat histories.
- Named assistant profiles reference only portable skill IDs, not plugin paths.

The public tests check the bundle and skill source contracts, while adapters
installed in individual AI hosts require their own compatibility, release, and
fresh-session discovery checks. Updating this repository does not update a
previously installed host plugin.
