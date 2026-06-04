# good-repo Recipes

Copy-paste prompts for common repository improvement workflows.

## 01 · Read-only audit

```text
good-repo audit this repository. Score it out of 100, classify the repo type, cite evidence by file path, and give the top 5 fixes by impact.
```

Use when you want judgment before edits.

## 02 · Hallmark-style exemplar analysis

```text
Explain why https://github.com/nutlope/hallmark is an exemplary GitHub repo, then identify which patterns we should copy into this repo and which patterns do not apply.
```

Expected output:

- Hallmark strengths.
- Gaps Hallmark still has.
- Transferable pattern list.
- File/settings plan for the current repo.

## 03 · good-pr-style operational skill analysis

```text
Explain why https://github.com/adewale/good-pr is an exemplary small skill repo. Then identify where this repo should copy its pain-to-checklist, template, script, and eval patterns.
```

Expected output:

- The real user/maintainer pain the repo serves.
- Checklist/template/example/script/eval opportunities.
- Gaps that should not be copied blindly.
- Small-scope file plan.

## 04 · Launch-ready skill repo

```text
Configure this as a launch-ready agent skill repository. Use good-readme for the README. Apply Hallmark for front-door/proof/modular-reference discipline and good-pr for pain-to-checklist/templates/scripts/evals discipline. Ask before legal or remote GitHub setting changes.
```

Good first file plan:

- `README.md`
- `package.json`
- `LICENSE` after approval
- `CHANGELOG.md`
- `skills/<name>/SKILL.md`
- `skills/<name>/references/*.md`
- `skills/<name>/scripts/*` if cheap mechanical checks exist
- `evals/evals.json` for skill behavior
- `docs/recipes.md`

## 05 · GitHub metadata pass

```text
Inspect this repo's GitHub metadata with gh if available. Recommend description, homepage, topics, feature toggles, social preview, and any missing .github files. Do not change remote settings without approval.
```

Expected output:

```markdown
**Description:** ...
**Homepage:** ...
**Topics:** ...
**Issues:** enable/disable because ...
**Discussions:** enable/disable because ...
**Manual settings:** social preview upload ...
```

## 06 · Proof gap repair

```text
Find proof gaps in this repository. If the repo claims UI, CLI behavior, package usage, skill behavior, or performance, identify the screenshot/demo/example/test that should prove it. Propose the smallest proof artifact we can add now.
```

Examples:

- UI app → screenshot + live demo link.
- CLI → terminal transcript with expected output.
- Library → runnable example + test.
- Skill → worked prompt + output excerpt.
- ML repo → inference notebook + results table.

## 07 · Maintenance hygiene

```text
good-repo maintain: check for stale README commands, missing changelog/release notes, broken internal links, stale screenshots, outdated package metadata, and unowned issues/templates. Return a prioritized maintenance punch list.
```

Use before a release or public announcement.

## 08 · Minimal OSS governance

```text
Add only the OSS governance files this repo can realistically maintain. Start with CONTRIBUTING and a PR template. Do not add code of conduct, security policy, issue forms, branch protection, or dependency bots unless you can justify them for this repo class and maturity.
```

Good output separates:

- Add now.
- Ask owner first.
- Defer.

## 09 · README + repo stack

```text
First run a README quality pass using good-readme principles. Then run a repo effectiveness pass using good-repo. Do not let README polish hide missing proof, license, metadata, examples, or automation.
```

Use when the repo has no launch surface yet.

## 10 · Owner-wide audit

```text
Assess every public repo under github.com/<owner>. Classify each repo, score it, detect homepage URL drift, and summarize profile-wide cleanup themes.
```

Useful command:

```sh
python3 skills/good-repo/scripts/audit-github-owner.py <owner> --output docs/<owner>-repos-assessment.md
```
