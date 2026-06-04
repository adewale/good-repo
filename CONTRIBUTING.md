# Contributing

Contributions are welcome, especially improvements to the rubric, examples, and repository-class guidance.

## Local setup

```sh
git clone https://github.com/adewale/good-repo.git
cd good-repo
```

There is no build step for the current skill package. Validate changes by checking:

```sh
python3 -m json.tool package.json >/dev/null
```

Then spot-check internal Markdown links and skill frontmatter.

## What to contribute

Good contributions include:

- New repo-class guidance in `skills/good-repo/references/repo-anatomy.md`.
- Sharper scoring criteria in `quality-checklist.md`.
- Concrete GitHub settings/workflow examples.
- Real audit examples in `docs/recipes.md`.
- Corrections that make the skill safer or less boilerplate-prone.

For large changes to the rubric or philosophy, open an issue first so the direction can be discussed.

## Pull requests

Please include:

- A short summary of the change.
- The repo class or workflow it improves.
- Any validation performed.

Keep guidance evidence-backed and avoid adding files or process that small repos cannot realistically maintain.
