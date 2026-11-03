# agentsec v1.0.0 Release Checklist

This checklist is for creating the first release of the single `agentsec` repository
and getting a DOI for it from Zenodo. These steps need a person logged in to the real
GitHub and Zenodo accounts. They cannot be done through a file edit.

Repository: `https://github.com/samyshyaka/agentsec`

The earlier checklist, `agentsec-bench/docs/release-checklist.md`, covers the old
AgentSec-Bench v0.1.0 release and its DOI (10.5281/zenodo.23107266). That record stays
tied to the old `agentsec-bench` repository. This release gets its own, new DOI.

## 0. Decisions to confirm before starting

- [ ] **Version number.** This checklist uses `v1.0.0`. Confirm it, or change it everywhere below.
- [ ] **Authors.** `CITATION.cff` lists Kelvin Oteyo and Samuel Dushimimana Shyaka. The DOI record
      will show whatever is in that file at release time. Confirm whether anyone else should be added.
- [ ] **Who owns the Zenodo account** that will archive the release (see section 3).

## 1. Fix these before releasing

- [ ] **Licence placeholders.** On `main`, the `LICENSE` files in `agentsec-scorecard` and `agenttrace`
      still say `[COPYRIGHT HOLDER - Samy to fill in before publishing]`. The fix ("Update LICENSE
      copyright holder to Samuel Dushimimana Shyaka") exists only on these unmerged branches:
      `agentsec-scorecard/month-2-agentsec-scorecard` and `agenttrace/month-2-agenttrace`.
      Merge or copy that change into `main` first. A release freezes whatever is on `main`.
- [ ] **Unmerged branches.** Five remote branches have commits that are not in `main`
      (`agentsec-bench/experiments-groq-oct2026`, `agentsec-bench/groq-free-tier-pilot`,
      `agentsec-scorecard/month-2-agentsec-scorecard`, `agentsec-scorecard/staging`,
      `agenttrace/month-2-agenttrace`). Decide whether to merge or keep each one. Do not
      delete a branch that holds work that is not saved elsewhere.
- [ ] **Checks are green on `main`.** Open the Actions tab and confirm the latest run on `main` passed.
- [ ] **No keys or credentials in the repository.** Search for `.env` files, API keys and local file paths.
- [ ] **Root files are present on `main`:** `README.md`, `LICENSE`, `CITATION.cff`, `CONTRIBUTING.md`,
      `.gitignore`, `docs/`, `examples/`, `research/`.
- [ ] **Update `CITATION.cff` for the release.** Add `version: 1.0.0` and set `date-released` to the
      release date (format `YYYY-MM-DD`). Do not add the `doi:` line yet; the DOI does not exist until after
      the release (section 4).
- [ ] **Sub-project versions.** `agentsec-bench/pyproject.toml` says `version = "0.1.0"`. Decide whether the
      individual projects keep their own version numbers. The repository release number does not have to match them.

## 2. Create the GitHub Release

Do the Zenodo setup in section 3 first if you want Zenodo to archive this release automatically. Zenodo only
archives releases published after the repository is switched on there.

1. Go to `https://github.com/samyshyaka/agentsec/releases/new`
2. Click **Choose a tag**, type `v1.0.0`, and choose **Create new tag on publish**. Target: `main`.
3. Title: `agentsec v1.0.0`
4. Description (draft, edit freely):

   > First versioned release of the agentsec repository. It brings six projects
   > together in one place, each in its own folder with its own README: agentsec-bench,
   > agentguard, agenttrace, agentsec-scorecard, criticalagent-blueprints and agentsec-crosswalk.
   >
   > - Month 2 experiment results are in `research/month2-results/`, with the raw run files,
   >   result tables and the script that rebuilds them.
   > - See `CONTRIBUTING.md` for how to contribute and `LICENSE` for the MIT licence.
   > - Cite this work using `CITATION.cff`.

5. Leave **Set as the latest release** ticked. Leave **pre-release** unticked.
6. Click **Publish release**.

## 3. Turn on Zenodo for the repository

1. Go to `https://zenodo.org` and log in with the account that should own the archive.
2. Open the GitHub settings page: `https://zenodo.org/account/settings/github/`
3. Connect your GitHub account if asked, then find `samyshyaka/agentsec` in the list and switch it **on**.
   - The repository must be public.
   - You need admin access to the repository. If it is not listed, click **Sync now**, or check
     Zenodo's current documentation. The GitHub connection steps have changed over time.
4. Once it is on, publishing a GitHub Release (section 2) makes Zenodo archive that release automatically
   and mint a DOI. If the release was already published before this switch was turned on, Zenodo will
   not pick it up. In that case, publish a new release, for example `v1.0.1`.

## 4. After the release

- [ ] **Find the DOI.** On the Zenodo page for the new record, copy the DOI. Zenodo gives two:
      a **version DOI** for exactly this release, and a **concept DOI** that always points to the latest version.
      Use the concept DOI for general citation and the version DOI when you need to point to this exact release.
- [ ] **Check the Zenodo record.** Confirm the title, authors and licence shown are correct. You can edit the
      metadata on Zenodo if something is wrong.
- [ ] **Add the DOI to `CITATION.cff`** (a `doi:` line) and to the root `README.md`, using a normal pull request.
- [ ] **Check `date-released`** in `CITATION.cff` matches the actual release date.
- [ ] **Do not re-tag.** If something is wrong after publishing, fix it in a new commit and make a new release
      (for example `v1.0.1`). Do not move or delete the `v1.0.0` tag.
- [ ] **Old repositories.** The six old repositories keep a pointer README that links to this repository.
      Confirm those pull requests are merged so the old pages send people to the new DOI.