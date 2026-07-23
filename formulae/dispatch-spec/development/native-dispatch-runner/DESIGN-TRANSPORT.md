# Design Transport

- Next consumer: Invoke Plan
- Selected architecture: deterministic coordinator plus host-native Orchestrate driver
- Canonical runtime source target: `runtime/orchestrate/`
- First proof host: native Codex subagent runtime
- Required proof: failure withholding first, then successful dependent progression, both from `orchestrate execute <dispatch.json>`
- Prohibited shortcut: bespoke parent spawning followed by synthesized receipts
