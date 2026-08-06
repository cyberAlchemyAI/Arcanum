# Closeout Contract

Each selected SWU must return a lifecycle-owner receipt containing:

- work-pack, task, SWU, layer, and attempt identities;
- exact pre-mutation target inventory and baselines;
- files changed within the selected SWU's write scope;
- acceptance-critical validation commands and results;
- owner-boundary and public-boundary results;
- unresolved residue and whether it can falsify acceptance;
- generated-package parity status when applicable;
- the unique successor from `SWU-MANIFEST.json`, returned but never auto-selected.

Closeout may update only this package's implementation result/evidence and the owner lifecycle records explicitly admitted by the selected route. It cannot promote, publish, release, deploy, select a successor, or rewrite unrelated pending work.
