# GitHub's Official Repo-Quality Baseline

Use this reference when grounding a `good-repo` audit in GitHub's own documentation. GitHub does not publish one universal "good repo" score, but its docs define a practical baseline through community profiles, repository metadata, README guidance, contribution files, security policy, Actions CI, and repository size limits.

## 1. README: the first orientation surface

GitHub says a repository README tells people why the project is useful, what they can do with it, and how they can use it.

A README typically includes:

- what the project does,
- why the project is useful,
- how users can get started,
- where users can get help,
- who maintains and contributes to the project.

Source: [About the repository README file](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)

`good-repo` implication: treat README quality as the front door, but do not let a polished README hide repo-level gaps like no license, no CI, no examples, or missing metadata.

## 2. Community Profile: GitHub's closest official health checklist

For public repositories, GitHub's Community Profile helps maintainers see whether a project meets recommended community standards. The checklist looks for recommended community health files such as:

- `README`,
- `CODE_OF_CONDUCT`,
- `LICENSE`,
- `CONTRIBUTING`.

GitHub's Community Profile docs also route maintainers toward issue/PR templates and other contribution guidance.

Source: [About community profiles for public repositories](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories)

The Community Profile is also exposed through GitHub's REST API, including `health_percentage` and detected community files.

Source: [Get community profile metrics](https://docs.github.com/en/rest/metrics/community?apiVersion=2022-11-28#get-community-profile-metrics)

`good-repo` implication: for public OSS projects that seek contributors, check Community Profile files explicitly and report the official health percentage when available. For tiny experiments, archived repos, private/internal repos, or projects not accepting contributors, apply these proportionately instead of recommending governance theater. Use [`community-profile-repolinter.md`](community-profile-repolinter.md) for API usage and Repolinter comparison.

## 3. Description, homepage, and topics: official discoverability surfaces

GitHub exposes repository description and homepage fields in repository settings/API. The homepage field is the URL with more information about the repository.

Source: [REST API: Update a repository](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#update-a-repository)

GitHub says topics help other people find and contribute to a project. Topics classify repositories by intended purpose, subject area, affinity groups, technologies, or other important qualities.

Source: [Classifying your repository with topics](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics)

`good-repo` implication:

- A missing description is a discoverability/front-door gap.
- Missing topics are a discoverability gap for public repos.
- Homepage drift is real: if README/package/docs expose a project homepage, live demo, docs site, package page, or marketplace listing, GitHub's `homepageUrl` should usually point to that canonical URL.
- Do not set homepage to third-party dependency docs, sponsor links, tweets, YouTube videos, citations, or generic framework docs.

## 4. License: required for open-source reuse

GitHub says public repositories are often used to share open source software, and for a repository to truly be open source, it needs a license so others are free to use, change, and distribute the software. Without a license, default copyright laws apply.

Source: [Licensing a repository](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

`good-repo` implication: for a public repo intended for reuse, no root `LICENSE` is a launch/trust blocker. README/package license claims are weaker than GitHub-detected license evidence; recommend adding a root license file that matches README and manifest claims.

## 5. Contribution guidelines and templates

GitHub says contributor guidelines communicate how people should contribute. GitHub surfaces contribution guidelines in repository UI and when users create issues or pull requests.

Source: [Setting guidelines for repository contributors](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/setting-guidelines-for-repository-contributors)

GitHub says issue and pull request templates customize and standardize the information contributors include when opening issues and pull requests.

Source: [About issue and pull request templates](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/about-issue-and-pull-request-templates)

`good-repo` implication: recommend `CONTRIBUTING.md`, issue templates, and PR templates when the repo invites external contribution or issue traffic. For small solo projects, start with a lightweight PR checklist and test command before heavy process.

## 6. Security policy

GitHub says a security policy gives instructions for reporting a vulnerability. The generated `SECURITY.md` should include supported versions and how to report a vulnerability.

Source: [Adding a security policy to your repository](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/adding-a-security-policy-to-your-repository)

`good-repo` implication: recommend `SECURITY.md` for packages, infrastructure, services, public apps, or anything security-sensitive. Ask for a real contact and supported-version policy before creating one.

## 7. CI and workflows

GitHub says continuous integration automatically builds and tests code in the repository. CI helps detect errors sooner; GitHub Actions workflows can run on pushes, pull requests, schedules, or external events, and expose test results in pull requests.

Source: [Continuous integration](https://docs.github.com/en/actions/get-started/continuous-integration)

`good-repo` implication: CI is not part of the Community Profile checklist, but it is an official GitHub quality mechanism. Recommend the smallest workflow that validates the repo's core promise: install/build/test for code, link checks for docs, eval validation for skill repos, smoke checks for apps.

## 8. Repository size and large files

GitHub documents large-file limits and performance concerns for regular Git repositories. Large binary assets should use Git LFS or another artifact strategy.

Source: [About large files on GitHub](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github)

`good-repo` implication: include repo-size and large-file risk in audits for repos with media, datasets, generated assets, models, build artifacts, or vendor bundles. Large files are a repo-health issue, not just a Git implementation detail.

## 9. Social preview: documented polish, not a core health file

GitHub supports customizing a repository's social media preview image for shared links.

Source: [Customizing your repository's social media preview](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/customizing-your-repositorys-social-media-preview)

`good-repo` implication: treat social preview as discoverability polish for public projects, visual/productized repos, and launch campaigns. Do not rank it above README, license, metadata, quick start, or proof.

## Official baseline vs good-repo additions

GitHub's docs support these as official baselines:

- README orientation,
- Community Profile health files,
- description/homepage/topics metadata,
- license clarity,
- contributor guidelines and templates,
- security policy where relevant,
- CI/workflows as automation,
- large-file/repo-size hygiene.

`good-repo` deliberately goes beyond GitHub docs with adoption/product heuristics:

- proof native to the project class,
- examples and quick-start verification,
- changelog/releases/roadmap/status signals,
- package metadata consistency,
- skill evals and trigger behavior,
- homepage drift detection across README/package/GitHub,
- owner/profile portfolio cleanup.

When auditing, label GitHub-official findings separately from `good-repo` judgment calls when that distinction matters.
