# Repository Anti-Patterns

Use this catalog to name repo problems clearly and propose the smallest fix.

## 1. README-Only Excellence

**Looks like:** The README is polished, but the repo has no license, no examples, no CI, broken install path, or no actual proof.

**Why it hurts:** Visitors get persuaded and then blocked. Trust collapses faster because the first impression over-promised.

**Fix:** Keep the README, but add proof and adoption scaffolding: license, quick-start validation, examples, CI smoke test, package metadata.

## 2. The Ghost Repo

**Looks like:** No README or a one-line README, no description/topics, no license.

**Why it hurts:** Nobody can evaluate the project without reading source.

**Fix:** Add minimal README, description, license decision, and a run/install command.

## 3. Proof Gap

**Looks like:** Claims of "beautiful UI," "fast CLI," "easy integration," or "AI skill" with no screenshot, output, example, benchmark, or worked prompt.

**Why it hurts:** Claims without proof feel like marketing copy.

**Fix:** Add the proof native to the project class: screenshots, live demo, terminal output, copy-paste code, notebook, examples, recipes.

## 4. Install Cliff

**Looks like:** `npm install` or `pip install` appears, but prerequisites, environment variables, platform support, or first-run command are missing.

**Why it hurts:** Adoption fails at the highest-friction point.

**Fix:** Add prerequisites, install command, first success command, expected output, and troubleshooting note for the most common failure.

## 5. Package Metadata Drift

**Looks like:** README says one package name, manifest says another; license differs; version is stale; package entry point is unclear.

**Why it hurts:** Users install the wrong thing or cannot import/run it.

**Fix:** Align README, manifest, package registry, release tags, and license.

## 6. Badge Soup

**Looks like:** 10+ badges before the description, many decorative or redundant.

**Why it hurts:** Badges push value below the fold and look like performative maintenance.

**Fix:** Keep only useful badges: CI, package version, license, docs. Remove decorative badges.

## 7. Template Zombie

**Looks like:** Generated files still contain placeholders, empty sections, default issue templates, or irrelevant contributing process.

**Why it hurts:** It signals the maintainer did not finish the repo setup.

**Fix:** Delete irrelevant sections. Replace placeholders with real project-specific content.

## 8. Demo Museum

**Looks like:** Screenshots/GIFs exist but show an old UI or command output that no longer matches.

**Why it hurts:** Users cannot tell whether the project or docs are stale.

**Fix:** Regenerate assets, version filenames, or remove stale visuals. Add a release checklist item.

## 9. Hidden Support Contract

**Looks like:** Issues enabled but no templates or maintainer expectations; discussions enabled but unmonitored; no support channel.

**Why it hurts:** Users do not know where to ask, and maintainers get low-quality reports.

**Fix:** Configure features intentionally. Add issue templates and response expectations, or disable surfaces you will not monitor.

## 10. Governance Theater

**Looks like:** Tiny project has heavy CODEOWNERS, CLA language, complex labels, stale project boards, and five templates but no usage docs.

**Why it hurts:** Process appears before value. Contributors face friction with no payoff.

**Fix:** Scale governance to community size. Start with README, license, PR checklist, and test command.

## 11. CI Theater

**Looks like:** CI badge exists but workflow does not validate the core promise, or badge is failing/red.

**Why it hurts:** Automation becomes negative trust.

**Fix:** Make CI run the install/build/test/docs commands that matter. Remove badges until green.

## 12. Docs Sprawl

**Looks like:** Many docs files with no index; README links are inconsistent; API reference duplicated in README and docs.

**Why it hurts:** Users cannot find the right page, and duplicated docs drift.

**Fix:** Add docs index/routing table. Keep README as orientation. Move depth to docs and link once.

## 13. No Maintenance Signal

**Looks like:** No changelog, roadmap, release notes, status, or recent validation. Users cannot tell whether the project is alive.

**Why it hurts:** Adoption feels risky.

**Fix:** Add one truthful signal: changelog for releases, roadmap for direction, status note for alpha/beta/maintenance, or archived notice if inactive.

## 14. Overclaiming

**Looks like:** README claims production-ready, secure, fast, used by teams, or compatible with platforms without evidence.

**Why it hurts:** Unverified claims create liability and user disappointment.

**Fix:** Replace claims with evidence or caveats. Say "tested on," "used internally," "experimental," or "not verified" when accurate.

## 15. Discovery Blind Spot

**Looks like:** Great repo, but GitHub description, homepage, topics, and social preview are blank.

**Why it hurts:** Search, link previews, and first impressions underperform.

**Fix:** Add concise description, homepage, 5–12 topics, and a social preview image.

## 16. Hidden Homepage URL

**Looks like:** README says `Live`, `Demo`, `Docs`, `Play now`, or package metadata has `homepage`, but GitHub's sidebar homepage URL is blank or points somewhere else.

**Why it hurts:** The best next click is hidden inside the README. Search results, link previews, and casual visitors lose the fastest route to the product.

**Fix:** Set GitHub `homepageUrl` to the canonical demo/docs/package URL. Keep README, manifest, and GitHub metadata aligned.

## 17. Unclear Project Class

**Looks like:** Visitor cannot tell if repo is a library, app, template, skill, tutorial, research artifact, or personal experiment.

**Why it hurts:** Expectations mismatch. A template README for a library, or a library README for an app, confuses users.

**Fix:** Name the class in the opening sentence and structure sections accordingly.

## 18. Missing Legal Boundary

**Looks like:** Public repo with no license, or README says MIT but no LICENSE file.

**Why it hurts:** Many users and companies cannot use the code.

**Fix:** Ask the owner to choose a license. Add LICENSE and align README/package metadata.

## 19. Examples Without Ownership

**Looks like:** `examples/` exists but no README explains which example to run first or what each demonstrates.

**Why it hurts:** Examples become a junk drawer.

**Fix:** Add `examples/README.md` with scenario table, commands, expected output, and maintenance status.

## 20. Skill Without Skill Behavior

**Looks like:** Agent skill repo has a `SKILL.md` but it is just a broad essay; no triggers, verbs, workflow, safety rails, or references.

**Why it hurts:** The agent cannot reliably invoke or execute the skill.

**Fix:** Add frontmatter description, invocation modes, explicit workflow, output format, and modular references.

## 21. Skill With No Evals

**Looks like:** Skill repo has instructions and examples, but no eval cases showing the behaviors it must reliably trigger or catch.

**Why it hurts:** Nobody can tell whether future edits preserve the skill's judgment. Subtle behaviors regress silently.

**Fix:** Add `evals/evals.json` or equivalent test prompts with expected outputs/assertions. Model this after `good-pr`: include cases that catch non-obvious failures, not just happy paths.

## 22. Hallmark Cargo Cult

**Looks like:** Repo copies Hallmark's screenshots/docs/roadmap style without matching its own project class or proof needs.

**Why it hurts:** Form without evidence reads as imitation.

**Fix:** Copy exemplar principles, not artifacts: Hallmark's front-door clarity/proof/modular depth, and good-pr's pain-to-checklist/templates/scripts/evals discipline.
