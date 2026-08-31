## What You Author And What Invoke Generates

Invoke Define turns bounded intent plus exact repository evidence into one
candidate definition bundle. You author one `invoke.define-source.v2` JSON
document. The compiler validates it and generates the bundle.

```text
intent + exact repository evidence
                |
                v
       DEFINE-SOURCE-v2.json      <- author this
                |
                v
     Invoke Define v2 compiler
                |
                +--> DEFINITIONS.json            <- machine artifact
                +--> DEFINITIONS.md / GLOSSARY.md <- derived views
                +--> SPEC.md + evidence files
                `--> stage receipt                <- production evidence
```

Do not author `DEFINITIONS.json` or the stage receipt. The generated
`DEFINITIONS.json` is the machine definition artifact. The Markdown files are
deterministic views. The receipt proves only that this producer completed the
declared transformation. Every new registry and definition remains
`candidate`, with `authority_effect: none`; compilation grants no acceptance,
promotion, mutation, publication, deployment, or production authority.
