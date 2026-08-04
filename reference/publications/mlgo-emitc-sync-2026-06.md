# LLVM MLGO sync minutes: EmitC path PoR (June 8, 2026)

| Field | Value |
|---|---|
| **Year** | 2026 |
| **Org** | Google / LLVM community |
| **Publisher** | LLVM Discourse |
| **Type** | forum |
| **Group** | Forums & workshops |
| **Link** | [https://discourse.llvm.org/t/mlgo-meeting-june-5-moved-to-june-8-2026/90976](https://discourse.llvm.org/t/mlgo-meeting-june-5-moved-to-june-8-2026/90976) |
| **Evidence tier** | **A** — settlement-watch checkpoint for C1 (EmitC-MLGO deploy path), not a settlement |

## Key contributions

- Published minutes for the June 8, 2026 MLGO sync focused on EmitC embedding of ML models
- States a **plan of record**: land Google-internal EmitC for the **inliner** first (regalloc if ready), using frequent trunk updates as large-scale integration testing while models stay fixed
- Explicit next customers: after that path, **Android and Fuchsia can start using EmitC**; **Chrome** needs multi-model support for the same policy as a follow-on

## Summary

This is a process checkpoint on the neural-advisor side of conflict **C1**, not a Magellan settlement and not “EmitC is default on Android/Chrome.” Engineering work remains (memref patterns, class wrapping, globals, docs). The minutes make the deploy sequence concrete: internal inliner EmitC → Android/Fuchsia → Chrome multi-model.

## Key takeaways

- EmitC-MLGO is still an active production bet in mid-2026
- Settlement watch for C1 should track **customer uptake** (Android/Fuchsia/Chrome), not only RFC existence
- Magellan’s shippable-C++ story and MLGO’s in-tree NN advisors remain **parallel**, not resolved

## Why it matters for this survey

Updates SURVEY §6 **C1** settlement watch and §5.4 / §5.5.1 job (b) evidence. Companion to [`mlgo-emitc-rfc.md`](mlgo-emitc-rfc.md). Prefer this primary Discourse thread when citing the June 2026 PoR.

## Limits / caveats

- Minutes, not an LLVM commit or Android/Chrome release note
- “Can start using” ≠ already default; Chrome multi-model is explicitly deferred
- No public evidence here that Magellan heuristics displaced MLGO on the same apps
