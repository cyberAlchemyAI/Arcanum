# Workbench Up

Workbench Up is an Arcana sigil for bringing the local ide-extension HTML workbench online and making it usable for manual bridge testing.

It is intentionally small: it starts or checks the local server, returns the workbench URL, and can prepare an approval-gated open-poll request that a session may later claim. It can also run a synthetic smoke loop to prove the bridge contract still works.

## When To Use

Use this sigil when:

- the user wants the workbench running now,
- a call or demo needs the HTML canvas available at `/demo/l0`,
- an operator wants to prepare a task for manual polling,
- a developer wants a quick bridge smoke before testing real agent behavior.

Do not use it to claim that a real skill executed. The smoke mode proves only the local bridge loop: prepare, approve, ready, claim, and admitted result.

## Default Boundary

The default workbench is:

```text
http://127.0.0.1:8765/demo/l0
```

The default project root is:

```text
projects/ide-extension
```

Workbench Up does not create a remote tunnel, background worker, queue lease, browser-extension controller, or provider integration. Those are separate lifecycle routes.

## Common Invocations

Start or verify the workbench:

```text
[$workbench-up] --start
```

Start the workbench and prepare an available request:

```text
[$workbench-up] --available --task "Create a short augmentor presentation" --skill whisper
```

Run the bounded local bridge smoke:

```text
[$workbench-up] --smoke --task "Workbench bridge smoke" --skill decision-gate --agent-ref openrouter.local-session
```

## Proof Claims

Workbench Up can honestly prove:

- the server responds on the loopback workbench URL,
- the workbench route renders,
- a request can be prepared, approved, and marked ready,
- a polling session can claim a ready request,
- the local kernel admits a claimant-bound result.

Workbench Up cannot prove:

- Codex executed the requested skill,
- OpenRouter produced model output,
- a browser was controlled through VS Code or VSCodium,
- a remote agent will continue polling automatically,
- a trusted-local HTML artifact is safe against hostile content.

## Lifecycle Status

Status: initial local operating sigil.

Promotion readiness is not claimed. The next lifecycle step is repeated use against real workbench demos and manual bridge tasks, followed by experiment-harness evidence if the invocation contract stays stable.
