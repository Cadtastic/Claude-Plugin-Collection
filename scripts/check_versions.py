"""Check that every GitHub-hosted entry matches its plugin's own manifest at the pinned ref.

For each entry in .claude-plugin/marketplace.json whose source is a GitHub repository, either
{"source": "url", "url": "https://github.com/<owner>/<repo>.git"} (preferred: HTTPS works without
an SSH key) or {"source": "github", "repo": "<owner>/<repo>"}:
- the entry must pin a "ref" (a release tag), and must carry a "version";
- .claude-plugin/plugin.json must exist in that repository at that ref;
- its "name" and "version" must equal the entry's.

Stdlib only. Set GITHUB_TOKEN to raise the API rate limit (CI passes the workflow token).
Exit code 0 when every entry agrees, 1 otherwise.
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CATALOG = Path(__file__).resolve().parent.parent / ".claude-plugin" / "marketplace.json"
GITHUB_URL = re.compile(r"^https://github\.com/([^/]+/[^/]+?)(?:\.git)?/?$")


def github_repo(source: object) -> str | None:
    """owner/repo for a GitHub-hosted source, else None."""
    if not isinstance(source, dict):
        return None
    if source.get("source") == "github":
        return source.get("repo")
    if source.get("source") == "url" and (match := GITHUB_URL.match(source.get("url", ""))):
        return match.group(1)
    return None


def plugin_manifest(repo: str, ref: str) -> dict:
    url = (
        f"https://api.github.com/repos/{repo}/contents/.claude-plugin/plugin.json"
        f"?ref={urllib.parse.quote(ref, safe='')}"
    )
    headers = {"Accept": "application/vnd.github.raw+json", "User-Agent": "check-versions"}
    if token := os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {token}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as resp:
        return json.load(resp)


def main() -> int:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    problems: list[str] = []
    for entry in catalog.get("plugins", []):
        name, source = entry.get("name"), entry.get("source")
        repo = github_repo(source)
        if repo is None:
            continue
        ref, version = source.get("ref"), entry.get("version")
        if not ref:
            problems.append(f"{name}: source has no ref; pin it to a release tag")
            continue
        if not version:
            problems.append(f"{name}: entry has no version; installed users would never update")
            continue
        try:
            manifest = plugin_manifest(repo, ref)
        except urllib.error.HTTPError as err:
            problems.append(f"{name}: cannot read .claude-plugin/plugin.json at {repo}@{ref} ({err})")
            continue
        if manifest.get("name") != name:
            problems.append(f"{name}: plugin.json at {ref} is named {manifest.get('name')!r}")
        if manifest.get("version") != version:
            problems.append(
                f"{name}: entry version {version} != plugin.json version "
                f"{manifest.get('version')} at {repo}@{ref}"
            )
        else:
            print(f"ok  {name} {version} ({repo}@{ref})")
    for problem in problems:
        print(f"ERROR  {problem}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
