# Define live intent evidence

Result: **PASS**

Two consecutive source-isolated native Codex artifacts at each selected complexity level cover the repository-owned minimum semantic oracle when replayed by the final validator.

## Results

| Target | Attempt | Obligations | Coverage digest | Receipt digest |
|---|---:|---:|---|---|
| target:mixed-define-v3 | 1 | 3 | `5fecde27bd520fa5313abd15276c92a08c5534e224d0dde568e6fffe2e750c69` | `1ff33edd5ffe92c229adce53b20f316ef6fb664cb3a687623058929bb87d06ad` |
| target:mixed-define-v3 | 2 | 3 | `5fecde27bd520fa5313abd15276c92a08c5534e224d0dde568e6fffe2e750c69` | `1ff33edd5ffe92c229adce53b20f316ef6fb664cb3a687623058929bb87d06ad` |
| target:complexity-example-ladder | 1 | 14 | `46573629d78c6b417447f0fa78829d3cd747a9d98dfee7b5308381e659aae383` | `763063203d057d3e8b3ee45d88b12c49589089869ab0677e855a34ea1c2d317a` |
| target:complexity-example-ladder | 2 | 14 | `d63b56a79750989533181d8dd34b1f649e4e8098470c5a4f5025761eaf745073` | `cb150df2bab4e6ea335249215bd596b8962582ad80a418e9fd7692a00f8d3280` |
| target:invoke-plan-successor | 1 | 33 | `85f3b8c64a335abd2b9dc6e74901bc913afeedbebda4d8d3144977ca8700c61f` | `3744a01f76d0d771eb08d2d8a64169f9226271ad66d40930a379396c1bc3aa08` |
| target:invoke-plan-successor | 2 | 33 | `1cf379d52c0bea39e7435a16510036d3350ca593f5b50a51d999dc7dfa2443f0` | `4757c2dd4d7d91b57a1ce8412e4672a41e79eb8922735eab68176711a1cf814a` |

All six artifacts were authored in source-only, read-only, ephemeral native Codex sessions without the hidden oracle. Each target has two consecutive passing artifacts under the final validator. Raw non-counted misses remain under `../live-intent-evidence-misses/`.

## Claim ceiling

This is bounded experimental evidence for the selected prompts and oracle. It is not proof of all possible human intent, end-to-end Arcanum readiness, lifecycle admission, execution authority, publication, or deployment.
