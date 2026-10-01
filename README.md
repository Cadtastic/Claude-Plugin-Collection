# Claude Plugin Collection

Custom-built plugins for [Claude Code](https://code.claude.com/) and Claude Cowork by Cadtastic,
published as one plugin marketplace named `cadtastic`.

## Add the marketplace

```
/plugin marketplace add Cadtastic/Claude-Plugin-Collection
```

Then install any plugin below with `/plugin install <name>@cadtastic`. Refresh the catalog later
with `/plugin marketplace update cadtastic`.

## Plugins

| Plugin | Version | What it does | Install |
|---|---|---|---|
| [RealOEM Searcher](https://github.com/Cadtastic/RealOEM-Searcher) | 0.1.0 | BMW, MINI, Rolls-Royce and BMW Motorrad parts on RealOEM.com: part numbers and supersession chains, VIN decoding, parts diagrams, fitment checks, vehicle comparison and a local vehicle finder. Needs [uv](https://docs.astral.sh/uv/). | `/plugin install realoem-searcher@cadtastic` |

Each plugin lives in its own repository and is pinned here to a release tag, so installing from this
marketplace gives you exactly the released version. See each plugin's README for requirements and
usage.

## Contributing

Changes go through pull requests; `main` is what installed users receive on their next refresh.
See [CLAUDE.md](CLAUDE.md) for the rules every catalog change follows.
