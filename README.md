# NetMind Provider for Hermes Agent

This plugin adds NetMind's OpenAI-compatible inference API to Hermes Agent.

## Install

This independent plugin has no additional runtime dependencies beyond Hermes.
It requires a host supporting `providers.base.ProviderProfile` and discovery of
`kind: model-provider` plugins. Install this local Git checkout with:

```bash
hermes plugins install file:///absolute/path/netmind-hermes-provider
```

After publishing the repository, use its URL and full commit SHA:

```sh
hermes plugins install https://github.com/NetMind-AI/netmind-hermes-provider --ref FULL_COMMIT_SHA
```

Replace `FULL_COMMIT_SHA` with the full reviewed commit hash from the repository.
Direct repository installation and admission to Hermes' curated catalog are
separate steps. Review the installer's scan and consent prompts.

## Configure

Set the NetMind API key in the active Hermes profile's environment:

```bash
export NETMIND_API_KEY="your-api-key"
```

Select the provider and bundled model:

```bash
hermes model --provider netmind
```

You can also run a one-shot request:

```bash
hermes -z "Reply with exactly: ok" \
  --provider netmind \
  -m Qwen/Qwen3.8-Flash
```

## Built-in Models

The plugin bundles the 31-model NetMind catalog and uses
`Qwen/Qwen3.8-Flash` as its default auxiliary model.

The plugin deliberately uses a static catalog and disables model-list discovery
and the corresponding health check. Authenticated `/models` support has not
been verified; this does not imply NetMind has no such endpoint.

## Test

Run the contract tests with a Hermes Agent checkout:

```bash
HERMES_AGENT_ROOT=/path/to/hermes-agent \
PYTHONPATH=/path/to/hermes-agent \
python -m pytest -q tests/
```

The live smoke test also requires `NETMIND_API_KEY` and `NETMIND_LIVE_TEST=1`.

Live tests make billable requests. Inference sends prompts, supplied context,
and tool definitions to `api.netmind.ai`. Keys remain in the Hermes profile
environment and must never be committed.

## Catalog submission and maintenance

Hermes' curated catalog requires a public plugin repository, a full 40-character
commit pin, accurate capability declarations, plugin validation including the
install security scan, and a maintainer-reviewed PR. Each subsequent catalog
pin update is a new reviewed PR. This plugin does not update its own code.

Before submission, use `hermes plugins validate --help` to run the installed
host's validation command. See the authoritative catalog requirements:
https://github.com/NousResearch/hermes-agent/tree/main/plugin-catalog

The source of model metadata is `netmind-agent-provider-integrations`. In that
repository, run `make generate` and
`python3 scripts/sync_upstreams.py --runtime hermes`, then run this plugin's
tests, update its version and publish the reviewed commit.
