# Claude Plugin Collection: contributor rules

This repository is the `cadtastic` plugin marketplace. It holds only the catalog
(`.claude-plugin/marketplace.json`), its README and CI. Plugins live in their own repositories.

## Rules for every catalog change

- **`main` publishes.** Users who added this marketplace receive whatever is on `main` on their next
  refresh. Work on a branch and merge through a pull request once CI passes.
- **Pin every entry to a release tag, over HTTPS.** Use a `url` source,
  `{"source": "url", "url": "https://github.com/<owner>/<repo>.git", "ref": "v<version>"}`, never a
  branch. The tag must already exist in the plugin's repository. Do not use the `github` source
  form: Claude Code clones it over SSH, which fails for anyone without a GitHub SSH key.
- **Versions must agree.** An entry's `version` must equal the `version` in the plugin's own
  `.claude-plugin/plugin.json` at the pinned tag. Without a version change, installed users are
  never offered the update.
- **Keep descriptions in sync.** Copy the entry's `description` and `keywords` from the plugin's
  `plugin.json`, and add or update the plugin's row in the README table.
- **No `metadata.pluginRoot`.** Entries use explicit sources; do not set a top-level `version`
  either (plugins release independently).
- **Only `marketplace.json` goes in `.claude-plugin/`.**

## Updating a plugin to a new release

1. Tag and release the plugin in its own repository.
2. Here, set the entry's `ref` to the new tag and `version` to the new version, and update the
   README row.
3. Run the checks below, open a pull request, and merge when CI is green.

## Checks (CI runs the same)

```bash
claude plugin validate . --strict
python scripts/check_versions.py
```

`check_versions.py` reads each GitHub-hosted entry's `plugin.json` at its pinned `ref` and fails when
the tag is missing or the versions differ.
