# Hallmark as an Exemplary GitHub Repo

Reference: [`nutlope/hallmark`](https://github.com/nutlope/hallmark). Use this file when the user asks what makes Hallmark excellent or wants to model a skill/package repo after it.

## The short answer

Hallmark is exemplary because the repository behaves like a finished product, not a code dump. A visitor can understand the promise, see proof, install it, inspect examples, understand the operating model, and trust that the author has a quality bar — all in a few minutes.

## What Hallmark does especially well

### 1. The opening is a complete product pitch

Hallmark's README opens with:

- A clear project name.
- A sharp one-line positioning statement: a design skill that refuses to look AI-generated.
- A live demo link.
- A compact feature promise: 22 themes, four verbs, press `T` to cycle.
- A hero image showing the output.

This satisfies the `good-readme` first-screen test: what it is, why it matters, and why the reader should keep going.

### 2. It shows proof before explanation

Hallmark does not merely claim it produces varied UI. It shows:

- A live demo site.
- Screenshot grid in the README.
- Multiple generated pages under `site/_tests/`.
- Docs that explain each generated test.
- Example recipes with prompts, inferred context, picks, and excerpts.

For a visual/design skill, screenshots are not decoration; they are the product proof.

### 3. The public interface is named

The README and skill define four verbs:

- default build
- `audit`
- `redesign`
- `study`

This turns the repo from "a pile of prompting instructions" into a tool with a memorable API. Users know what to ask the agent to do.

### 4. The install path is explicit

Hallmark gives a single install command:

```sh
npx skills add nutlope/hallmark
```

It also documents copy/install paths for Claude Code, Cursor, and Codex. This removes adoption uncertainty across harnesses.

### 5. Packaging metadata matches the product

`package.json` includes:

- `name`, `version`, `description`, `keywords`, `license`.
- `files: ["skills"]`, so package contents are intentional.
- A `skill` block pointing to `skills/hallmark/SKILL.md`, references, and supported harnesses.

The repo tells package managers and humans the same story.

### 6. The README is concise; references carry the depth

Hallmark avoids a giant README. Deep behavior lives in:

- `skills/hallmark/SKILL.md` — operating protocol.
- `skills/hallmark/references/` — modular design rules.
- `docs/recipes.md` — worked prompts.
- `docs/study-examples.md` — worked `study` flows.
- `ROADMAP.md` — future direction.

This is progressive disclosure: skim first, inspect when needed.

### 7. The skill itself has real judgment

The skill is not a generic checklist. It contains:

- Safety rails for existing projects.
- Pre-flight scan instructions.
- Component-vs-page routing.
- Macrostructure selection.
- Theme diversification.
- Mobile gates.
- Slop-test gates.
- Pre-emit self-critique.
- Project memory.

That specificity makes it reusable. A great skill repo must encode judgment, not vibes.

### 8. It has examples across contrasting cases

The README and docs demonstrate different briefs: SaaS, travel, coffee, portfolio, fashion, ceramics, developer infrastructure, podcasts, bakeries, manifestos, and more.

This matters because the core claim is variety. The examples test the claim across domains rather than showing one cherry-picked demo.

### 9. It records quality work as artifacts

`site/_tests/README.md` explains what the generation tests are for, what worked, what failed, and what changed in later versions. This is stronger than a vague "tests" folder: it documents learning and regression criteria.

### 10. Roadmap is concrete

`ROADMAP.md` lists specific next moves: tighten themes, image-heavy brief hook, brand-first flow, motion tokens, variants, charts reference, multi-page coherence.

A good roadmap is not a wishlist of nouns. It shows the maintainer sees the product's current edge and next leverage points.

### 11. It has restraint

Hallmark avoids many repo anti-patterns:

- No badge soup.
- No giant README manual.
- No empty boilerplate sections.
- No vague "coming soon" placeholders in the front door.
- No hidden install path.
- No mismatch between README promise and repo contents.

## What is not perfect

Even exemplary repos have gaps. Hallmark could improve:

- GitHub topics appear empty from the public API; topics would improve discovery.
- A `CONTRIBUTING.md` would help outside contributors.
- A simple CI/link check could validate skill metadata and docs references.
- Issue templates could shape high-quality bug/design reports.
- `CHANGELOG.md` or GitHub Releases could make version changes easier to scan.

Do not copy Hallmark blindly. Copy the pattern and adjust for project class.

## Transferable Hallmark pattern

For a skill/package repo, aim for this shape:

```text
README.md                         # concise product front door
LICENSE                           # clear legal permission
CHANGELOG.md or ROADMAP.md         # maintenance/change signal
package.json                       # package + skill metadata
skills/<name>/SKILL.md             # agent-facing operating protocol
skills/<name>/references/*.md      # modular deep rules
/docs/recipes.md                   # copy-paste prompts / workflows
/docs/examples.md                  # worked examples / case studies
/site or /examples                 # runnable proof / gallery
.github/                           # contribution + automation when ready
```

## Hallmark-derived repo principles

1. **Proof beats promises.** If the repo claims visual output, show screenshots. If it claims a CLI, show terminal output. If it claims a library, show runnable code.
2. **Name the verbs.** Users remember actions better than abstractions.
3. **Keep the README as the front door.** Move depth to docs/references.
4. **Make installation boring.** One obvious command, plus alternatives only when needed.
5. **Encode judgment.** Rules, gates, refusals, and examples matter more than slogans.
6. **Show variation.** One demo proves possibility; many contrasting demos prove robustness.
7. **Leave a maintenance trail.** Roadmap, changelog, generated tests, and known gaps build trust.
8. **Avoid generic polish.** Every section should prove something specific about this repo.
