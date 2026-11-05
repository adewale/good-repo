# Review automation before copying it

Suppose a validation workflow declares unrestricted `push` and `pull_request`.
Updating a feature branch with an open PR starts both workflows. If both run the
same check with equivalent inputs and permissions, one may add no useful evidence.
Inspect event-dependent conditions, branch protection, and release consumers first.

For a repo whose policy is PR validation plus main and tag validation, an intended
event map could be:

| Event | Validation |
| --- | --- |
| Feature push with an open PR | PR run |
| Feature push without a PR | Deferred until PR, if the maintainer accepts this |
| Main push | Push run |
| Tag push | Push run, preserving the existing tag policy |

An explicit `push.branches: [main]` filter alone excludes tags. Retain the existing
tag patterns where tag validation is required. Do not change required check names
or drop merge-queue events while removing duplicate branch runs. A fork PR may
have different permissions from a push; matching step names do not prove equivalence.

Likewise, inspect an action's pinned documentation and implementation before adding
a cache around it. If it already caches the same artifacts, retain the extra cache
only when a different path, invalidation rule, or measured problem justifies it.
Separate validation from publishing before cutting events with release side effects.

A smaller YAML file is not the success criterion. The retained events must still
provide the repository's required evidence. Workflow lint checks syntax; verify
event coverage and required checks separately, then trial the change before rollout.
