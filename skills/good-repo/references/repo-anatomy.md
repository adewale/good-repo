# Anatomy of an Effective GitHub Repo

A GitHub repository is not just source code. It is an adoption funnel, documentation surface, trust signal, contribution queue, and maintenance record.

Not every repo needs every file. Pick the anatomy that matches the project class.

## Universal front-door files

| File / surface | Purpose | Include when |
| --- | --- | --- |
| `README.md` | Orientation: what, why, install, usage, proof, links | Always |
| `LICENSE` | Legal permission | Public repos unless intentionally all-rights-reserved |
| `.gitignore` | Keeps generated/local files out | Always for code repos |
| `CHANGELOG.md` | Upgrade/change history | Versioned packages, tools, apps with releases |
| `ROADMAP.md` | Direction and planned work | Maintainer wants users/contributors to understand future priorities |
| `CONTRIBUTING.md` | Contribution process | Public OSS accepting contributions |
| `SECURITY.md` | Vulnerability reporting | Packages, infra, services, anything security-sensitive |
| `CODE_OF_CONDUCT.md` | Community expectations | Larger communities, public contribution programs |

## GitHub surfaces

| Surface | Purpose | Good default |
| --- | --- | --- |
| Description | Search/result card clarity | One sentence, 80–140 chars |
| Homepage | Link to docs/demo/package | Use live demo, docs site, or package page |
| Topics | Discovery | 5–12 accurate topics, no spam |
| Social preview | First impression in link shares | Use actual product screenshot/OG card |
| Issues | Bug/feature intake | Enable if maintained; disable if not monitored |
| Discussions | Community Q&A | Enable only if community exists or maintainer wants Q&A |
| Wiki | Docs | Usually disable; prefer versioned docs in repo |
| Releases | Version signal | Use for packages, CLIs, binaries, templates |
| Branch protection | Maintainer safety | Protect default branch once CI exists |

## Project-class patterns

### 1. Skill / agent package

Models: Hallmark for productized proof; good-pr for small operational workflow. For detailed packaging and layout rules, see `skill-repo-best-practices.md`.

Recommended structure:

```text
README.md
LICENSE
CHANGELOG.md or ROADMAP.md
package.json or .claude-plugin/marketplace.json
skills/<skill-name>/SKILL.md
skills/<skill-name>/references/*.md
skills/<skill-name>/scripts/*.sh        # optional, for cheap mechanical checks
docs/recipes.md or references/*example*.md
evals/evals.json                       # strongly recommended for skills
examples/ or site/_tests/              # when visual/executable proof matters
```

High-value signals:

- Install command for the target harnesses.
- Clear invocation verbs or workflow triggers.
- Frontmatter passes skill spec requirements and includes trigger-rich description.
- References are modular and loaded on demand.
- Worked examples show the skill's behavior on realistic prompts.
- Blank templates plus filled examples when the skill produces a repeatable artifact.
- Small scripts automate mechanical checks when useful.
- Evals capture non-obvious behaviors the skill must reliably catch.
- Safety rails and refusal/confirmation rules are explicit.
- Package or marketplace metadata points to the skill entry.

Avoid:

- A single enormous `SKILL.md` with no reference split.
- Generic prompting advice with no concrete workflow.
- No examples or evals proving the skill works.
- README that describes the philosophy but not installation or usage.

### 2. Library / package

Recommended structure:

```text
README.md
LICENSE
CHANGELOG.md
package manifest
src/
tests/
examples/
docs/ or generated API docs link
.github/workflows/ci.yml
```

High-value signals:

- Package name matches install command.
- Minimal runnable example includes imports and output.
- Supported runtime versions are explicit.
- API docs are linked or generated.
- CI runs tests on supported versions.
- Semver/release process is clear.

Avoid:

- Examples that reference APIs not exported.
- Full API dump in README.
- No tests while claiming production reliability.

### 3. CLI / TUI tool

Recommended structure:

```text
README.md
LICENSE
CHANGELOG.md
src/ or cmd/
examples/
docs/configuration.md
completions/ (if available)
.github/workflows/ci.yml
```

High-value signals:

- Screenshot/GIF/terminal capture in first screenful.
- Install methods: package manager, binary release, source.
- `tool [FLAGS] <args>` synopsis.
- 3–5 common commands with actual output.
- Shell completion and config docs when relevant.
- Release artifacts for supported platforms.

Avoid:

- Only showing `--help` output.
- No platform/version support statement.
- No expected output for examples.

### 4. Web app / SaaS / template

Recommended structure:

```text
README.md
LICENSE
.env.example
docs/deployment.md
app/ or src/
public/ or assets/
examples/ or screenshots/
.github/workflows/ci.yml
```

High-value signals:

- Live demo or screenshots.
- Local dev setup from clone to running server.
- `.env.example` and required services.
- Deployment instructions or link.
- Tech stack and architecture notes for contributors.
- Seed/demo data if the app needs data to be meaningful.

Avoid:

- Missing environment variable documentation.
- Screenshots that do not match current app.
- Assuming paid services without stating costs.

### 5. Docs / knowledge repo

Recommended structure:

```text
README.md
docs/
CONTRIBUTING.md
LICENSE
.github/workflows/link-check.yml
```

High-value signals:

- README explains scope and audience.
- Table of contents or route map.
- Contribution rules for edits/citations.
- Link checking.
- Source/citation policy.

Avoid:

- Uncurated link dumps.
- No maintenance date or owner.
- No criteria for inclusion.

### 6. Research / ML artifact

Recommended structure:

```text
README.md
LICENSE
CITATION.cff or citation block
requirements.txt / environment.yml / pyproject.toml
notebooks/
scripts/
models/ or links to model registry
data/README.md or dataset links
```

High-value signals:

- Paper/model link.
- Hardware/software requirements.
- Dataset acquisition instructions.
- Training and inference commands.
- Results table and reproduction caveats.
- Citation instructions.

Avoid:

- Claims without benchmark setup.
- Untracked notebooks that require hidden data.
- No model/data license clarity.

## Minimum launch-ready checklist

A public repo is launch-ready when a visitor can answer these without asking the maintainer:

- What does it do?
- Who is it for?
- How do I install or run it?
- What does success look like when it works?
- What are the prerequisites?
- What license applies?
- Where do I report bugs or contribute?
- What is current vs planned?
- Is there proof it works?

## Repo structure principles

1. **Root is for orientation.** Keep root files few and recognizable.
2. **Examples are product proof.** Add examples before adding more prose.
3. **Docs should route, not sprawl.** Long docs need an index.
4. **Generated assets need provenance.** Screenshots/GIFs should be reproducible or versioned.
5. **Automation should validate promises.** If README says `npm test`, CI should run it.
6. **Governance should match community size.** Do not add elaborate process to a tiny personal tool.
7. **Truth beats completeness.** Missing sections are better than stale or fake ones.
