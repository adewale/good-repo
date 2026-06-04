# Skill Repo Best Practices

Use this reference when auditing or configuring an Agent Skill repository. It combines the Agent Skills/Pi package conventions with patterns observed across `github.com/adewale` skill repos.

## Optimal structure

Separate the **installable skill** from repo-only development artifacts.

```text
my-skill-repo/
├── .claude-plugin/
│   └── marketplace.json              # Claude plugin / skills CLI metadata
├── .github/workflows/ci.yml           # Repo validation, not part of runtime skill
├── README.md                          # Human-facing repo front door
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md                    # If accepting outside PRs
├── package.json                       # npm/pi package metadata when distributed
├── skills/
│   └── my-skill/                      # Directory name matches SKILL.md `name`
│       ├── SKILL.md                   # Required runtime instructions
│       ├── references/                # Loaded on demand by task
│       ├── scripts/                   # Runtime helper scripts, if useful
│       └── assets/                    # Templates/images/data, if useful
├── evals/                             # Repo-only skill behavior tests
├── examples/ or docs/                 # Repo-only examples, recipes, reports
└── scripts/                           # Repo-only validation/development scripts
```

For `good-repo`, the optimized variant is:

```text
skills/good-repo/SKILL.md
skills/good-repo/references/*.md
skills/good-repo/scripts/check-repo-readiness.sh
skills/good-repo/scripts/audit-github-owner.py
evals/evals.json
docs/recipes.md
docs/sample-audits.md
docs/adewale-repos-assessment.md
docs/lessons-learned.md
```

The `skills/good-repo/` directory is what a user installs. The `docs/`, `evals/`, `.github/`, and root metadata are for humans, package managers, and maintainers.

## Discovery and packaging rules

- Use top-level `skills/` plural. Pi and the `npx skills` ecosystem discover `skills/<name>/SKILL.md` reliably.
- The skill directory name should match frontmatter `name` exactly. Pi is lenient, but the Agent Skills standard and other harnesses are stricter.
- Keep `SKILL.md` frontmatter minimal and valid: `name`, `description`, optional `license`, `compatibility`, `metadata`.
- Keep the description trigger-rich and under 1024 characters. Say when to use the skill, not just what it is.
- Add `.claude-plugin/marketplace.json` when targeting Claude/plugin installation.
- Add `package.json` metadata for npm/pi distribution. For Pi packages, include `pi.skills` or use conventional `skills/` directory discovery.

## SKILL.md design

Good `SKILL.md` files are short, navigable, and operational.

- Keep under ~500 lines when possible.
- Put detailed doctrine into `references/`.
- Use decision trees and verb tables rather than long prose.
- Include safety rails and stop/ask rules.
- Include output formats when the skill produces structured artifacts.
- Make the model load only the relevant references for a task.
- Add anti-patterns with concrete bad/good examples.

Patterns observed:

- `slide-maker` uses a phase table: load different references only when entering each phase.
- Cloudflare skills use decision trees to route the agent to the right product/reference.
- `good-pr` uses checklist + template + example so the skill produces a concrete artifact.
- `anti-slop-writing` keeps runtime doctrine separate from evals, rejected edits, runbooks, and lessons.

## Reference files

Organize references by user task, not implementation structure.

Good reference categories:

- `quality-checklist.md` — scoring/rubric.
- `anti-patterns.md` — named smells and smallest fixes.
- `github-settings.md` — external settings and commands.
- `repo-anatomy.md` — class-specific structures.
- `*-exemplar.md` — model repos and transferable patterns.
- `skill-repo-best-practices.md` — skill-specific packaging and eval guidance.

For files over ~300 lines, include a table of contents. Keep examples close to the rule they demonstrate.

## Scripts

Runtime scripts belong inside `skills/<name>/scripts/` when the skill may ask the agent to run them in a target repo.

Use scripts for mechanical checks only:

- JSON/YAML parse validation.
- homepage URL drift detection.
- repo readiness smoke checks.
- owner-wide metadata collection.
- link or file-presence checks.

Do not put broad, destructive, or credential-mutating operations in scripts. Remote GitHub settings should remain advisory unless the user explicitly approves mutation.

Repo-only development scripts can live in root `scripts/`, but if the agent needs to run the script as part of skill behavior, keep it inside the installable skill directory.

## Evals

For skill repos, evals are proof. They should test behavior that generic prompting often misses.

Recommended shape:

```text
evals/evals.json
```

Each case should include:

- `prompt`
- `expected_output`
- discriminating assertions
- optional fixture files

Good assertions are specific enough that a baseline no-skill run may fail. Avoid assertions that merely check for generic words.

Patterns to copy:

- `good-pr` evals test subtle review behavior: bad assertions, missing repro steps, visual evidence, first-time contributor trust.
- `anti-slop-writing` uses tune/holdout splits, adversarial false-positive cases, failure corpora, and rejected-edit logs.
- `python-workers-skill` notes that baseline-vs-skill comparison is needed to prove the skill adds value.

## Human-facing docs

A strong skill repo usually needs:

- `README.md` — install, usage, examples, what is runtime vs repo-only.
- `CHANGELOG.md` — changes to doctrine, scripts, evals, compatibility.
- `CONTRIBUTING.md` — required eval/doc updates for changes.
- `docs/recipes.md` — copy-paste prompts/workflows.
- `docs/lessons-learned.md` or root `Lessons_learned.md` — why doctrine changed and what not to overgeneralize.

Do not put repo-only eval process, old results, or lengthy research into `SKILL.md` unless the agent needs it at runtime.

## Marketplace metadata

Claude plugin metadata should use the `plugins` array and `./`-prefixed paths:

```json
{
  "name": "my-skill",
  "description": "What it does",
  "plugins": [
    {
      "name": "my-skill",
      "source": "./",
      "skills": ["./skills/my-skill"]
    }
  ]
}
```

Common mistakes:

- `skill/` singular instead of `skills/`.
- parent directory name does not match frontmatter `name`.
- flat marketplace manifest with no `plugins` array.
- skill paths missing `./`.
- giant `SKILL.md` with all doctrine in one file.
- evals inside the runtime skill directory when they are not needed at runtime.

## Acceptance checklist for skill repo layout

- [ ] `skills/<name>/SKILL.md` exists.
- [ ] `<name>` matches frontmatter `name`.
- [ ] `description` is trigger-rich and under 1024 characters.
- [ ] `SKILL.md` is under ~500 lines or strongly justified.
- [ ] Detailed guidance lives in `references/`.
- [ ] Runtime helper scripts live in `skills/<name>/scripts/`.
- [ ] Repo-only evals live outside the installable skill directory.
- [ ] `.claude-plugin/marketplace.json` points to `./skills/<name>` when Claude/plugin distribution matters.
- [ ] `package.json` includes clear package metadata and Pi/npm distribution fields when relevant.
- [ ] README states what gets installed vs what is for development.
- [ ] CI validates JSON, scripts, internal links, and skill-specific eval/metadata files.
