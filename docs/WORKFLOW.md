# How to update this survey

Prediction-first loop aimed at the **future agentic compiler** (SW stack + HW codesign feedback). Digests are evidence.

## Decision tree

```text
New source
  ├─ Reshapes agentic compile / heuristics / kernels / oracles / ASIC bring-up?
  │     YES → Tier A (or B if substrate only: Helion, StableHLO, llvm-project)
  │     NO  → skip or Tier C one-liner
  ├─ Pure EDA/RTL LLM with no kernel/IR/oracle loop?
  │     YES → out of scope (unless it feeds compiler codesign claims H*)
  ├─ Conflicts with CLAIMS / CONFLICTS?
  │     YES → update CONFLICTS first (never average)
  └─ Moves SURVEY §5?
        YES → CLAIMS + narrative; else digest+INDEX+STATUS only
```

## Add-source order

1. Tier A/B/C  
2. Digest from `reference/publications/_TEMPLATE.md` (create if missing; fill **Org** + **Publisher**)  
3. INDEX row with Org/Publisher columns (★ only for prediction-critical)  
4. CONFLICTS if disagreeing  
5. CLAIMS if prediction moves  
6. Thin touch to SURVEY §5  
7. `reference/repos.md` / `reference/products.md` / SYSTEMS if mechanism new  
8. STATUS changelog  
9. `python3 scripts/validate_survey.py`

## Depth

Stub → digest → deep (PDF) before changing SURVEY §5.5 horizons.
