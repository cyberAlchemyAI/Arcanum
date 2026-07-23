# Runtime Overlays

Runtime overlays let a consuming repository add declared, digest-bound material
to an Arcanum-generated runtime package without turning the generated package
into an authority.

The canonical package is always generated first. A repository overlay may then:

- insert a declared fragment after one exact canonical anchor;
- copy a declared file to a contained package destination;
- add only metadata named in the manifest.

It may not replace canonical text, remove a gate or status ceiling, infer a
preset from an existing generated package, or use a generated package as an
overlay source.

Validate a manifest before generation:

```bash
python3 runtime/overlays/scripts/validate_runtime_overlay.py \
  --manifest <repo>/.arcanum/runtime/overlays/<target>/manifest.json \
  --target <target> \
  --repo-root <repo>
```

After generation and overlay application, add `--check-generated` to validate
the resulting runtime packages and copied payloads.
