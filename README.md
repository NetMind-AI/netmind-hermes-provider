# NetMind Provider for Hermes Agent

This plugin adds NetMind's OpenAI-compatible inference API to Hermes Agent.

## Install for Local Testing

Copy this repository into the active Hermes profile:

```bash
mkdir -p "$HERMES_HOME/plugins/netmind-provider"
cp -R . "$HERMES_HOME/plugins/netmind-provider/"
```

After the plugin is published, install it through Hermes' plugin installer and catalog instead of copying it manually.

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

NetMind does not currently expose a compatible `/models` catalog endpoint, so this plugin uses a static fallback catalog.

## Test

Run the contract tests with a Hermes Agent checkout:

```bash
HERMES_AGENT_ROOT=/path/to/hermes-agent \
PYTHONPATH=/path/to/hermes-agent \
python -m pytest -q tests/
```

The live smoke test also requires `NETMIND_API_KEY` and `NETMIND_LIVE_TEST=1`.
