# Survey status

Last updated: **2026-09-23**

## Current state

| Area | Status and practical meaning |
|---|---|
| Survey and design guidance | Revised in the existing narrative, retaining sections 0 through 9 and the alternatives section. |
| Objectives | Runtime performance first; developer productivity and portability next; search cost measured from the start. |
| Architecture | Passes, lowering, representations, and agent boundaries remain choices to evaluate. |
| Forecast | One, three, five, and ten years from September 2026, plus beyond; confidence and needed progress stated. |
| Design checklist | All 23 product topics and ten technical priorities retained in readable comparisons. |
| Evidence | 155 source digests; related papers, blogs, and repositories distinguished from independent corroboration. |
| Updated sources | Ave version 2, CAKE result scope, and Helion’s model-guided tuning; structured search and distribution coverage expanded. |
| Survey PDF | Rebuilt with the current narrative and reference appendices; source links open primary references. |
| Presentation | Existing slides and bilingual transcripts are an earlier snapshot; not aligned with this revision. |
| Repository skill | Updated with plain-language guidance, evidence standards, architecture flexibility, and publication authorization rules. |
| Publication | Local changes only for this batch. The user’s instruction not to push remains in effect. |

## Coverage still to strengthen

- Independent application-level comparisons under shared workloads, constraints, and search budgets.
- Transfer of performance and workload coverage to genuinely new hardware and additional vendors.
- Ablations separating model capability, representation, diagnostic feedback, and search resources.
- Broader evaluation of generated compiler components, communication choices, and long-term maintenance.
- Full-text refinement of older, thin digests; historical shorthand remains in parts of the source catalog.

## Change log

| Date | Change |
|---|---|
| 2026-09-23 | Reframed the single narrative as a performance-first design guide; retained the section structure, 23 product topics, and 10 technical priorities. Added five forecast horizons, flexible compiler boundaries, explicit evidence scope, and readable design experiments. Added Mirage, Prism, Helion tuning, Triton-distributed, and Shardy; updated Ave and CAKE interpretations. Index: 155. Updated repository skill and PDF pipeline; preserved historical heading links. Presentation remains an earlier snapshot. |
| 2026-09-23 | September evidence wave: MaxKernel ★, JAXBench ★, Pallas, AMDKernelVault ★, KernelGenBench ★, Hyperloom ★, AsmEvo ★, ForgeMegakernel ★. INDEX **150**. Hybrid holds; **C9** still open (peak ≠ TritorX coverage). Survey PDF + Beamer/EN/zh-TW. |
| 2026-08-31 | Beamer + EN/zh-TW: skill-scope fold on 4/22/24–27/29/33/36–41 (T10 exists, C7, ★ SIGIL, INDEX **142**). Sharing PDF rebuilt. |
| 2026-08-31 | Skill-scope lesson + re-search (hard rule 15): digest Agent Skills spec, SKILL.state, SIGIL ★, SkCC, SkVM, SkillSmith (2605.15215). Three senses of “skill”; T10/P2/§4.6/§9 grow; **no** C6/C2 move, **no** L-band. INDEX **142**. Survey PDF rebuilt (Beamer unchanged). |
| 2026-08-27 | §0.1 **top of the picture**: agentic compiler loop (control plane → typed kernel → classical lower → freeze-serve). Survey is evidence, not a second goal. Canonical loop + §5.1 pointer. Survey PDF rebuilt (Beamer unchanged). |
| 2026-08-26 | Re-search after TIRx miss: digest vendor L4 kernel IRs (TileLang, Gluon, TLX, FlyDSL, CuTe DSL, Event Tensor, ThunderKittens 2.0). Lesson: not only arXiv “LLM+IR”; walk docs/FFI/LSP/stale stacks. INDEX **136**. C4 more contested; Event Tensor = L6 not L-llm. Hybrid holds. Survey + sharing PDFs; Beamer 10/28/31–32/36–38/40–41 + EN/zh-TW |
| 2026-08-26 | Cover **TIRx** in LLM-oriented IR: TVM Tensor IR next as L4 typed agent face (FFI + tile primitives; search rungs ≠ survey L-bands). Tier B. INDEX **129**. Thin T1/T2/C3/C4; survey + sharing PDFs; Beamer 10/28/32/37/41 + EN/zh-TW |
| 2026-08-25 | Fold **LLM-oriented IR**: vocabulary §0.2 (fluency / summary / intent / typed-agent / translation glue); ★ LLM4IR; IntOpt, IRIS-14B, ComPile, IRCoder; thin T1/T7/C3/A5; **not** a new L-band. INDEX **128**. Survey + sharing PDFs; Beamer 4/10/18/28–32/37/40–41 + EN/zh-TW |
| 2026-08-24 | Beamer + EN/zh-TW: DeepSeek Harness on C7 (24/33) and T10 (29); slide 37 count 123; slide 39 not-A footer; survey + sharing PDFs rebuilt |
| 2026-08-24 | Add **DeepSeek Harness** (`dsh`, 2026-08-13): Tier B control-plane runtime; **not** a compiler harness (**C7**); T10 color only; INDEX **123**; survey PDF + slide 40/41 counts |
| 2026-08-24 | Beamer + EN/zh-TW transcripts: fold August wave (Cake, Argus, GEAK v4, Zomboss, T-LLM, llvm-harness) into slides 4/7/12/14/17–18/28–31/38–41; Argus under CausalFlow not AMD; index **122**; sharing PDF rebuilt |
| 2026-08-24 | Add missed **Argus** ★ (arXiv:2604.18616): data-flow invariants + SMT; INDEX **122**; thin T1/T2/C3/C4; survey PDF rebuilt |
| 2026-08-24 | August evidence wave: Cake ★, Zomboss ★, GEAK v4 ★, T-LLM, GEAK MLA, llvm-harness; INDEX **121**; thin SURVEY §0.1/§1/§4–§8 + T1/T2/T5/T6/T8; goal-align holds hybrid; survey PDF rebuilt |
| 2026-08-06 | Beamer slide 11: fix bottom size-callout overlap (fit+below gutter); bet line = priors+e2e controller; EN+zh-TW |
| 2026-08-06 | All 41 transcripts → slide-04 detail + abbrev glosses (EN+zh-TW); README/skill bar |
| 2026-08-06 | Beamer slide 4: shrink org tags to tiny foot line; restore claim primacy; transcripts |
| 2026-08-06 | Beamer slide 4: org tags on six-trend examples; detailed EN+zh-TW transcripts |
| 2026-08-05 | Goal-align after §5.1.1–5.1.4; §5.1.4 M1/M2/M3 + slide 13; S8; deck 41; thin consistency; PDFs |
| 2026-08-05 | SURVEY §5.1.3 e2e-optimal-seeking architecture (A7/S7); slide 12; stance #8; deck 40; survey+sharing PDFs |
| 2026-08-05 | Sharing: slides 10–11 (bands + cost model/plugins); stance #7; deck 39 slides; EN+zh-TW transcripts; survey PDF |
| 2026-08-05 | SURVEY §5.1.1: one universal cost model — feasibility + size (prior LLM vs local advisors); PDF rebuilt |
| 2026-08-05 | SURVEY §5.1.2: predict ~6–7 abstraction bands (roles + cluster/power); plugins if not consolidated; PDF rebuilt |
| 2026-08-05 | SURVEY §5.1.1: how many data-plane abstractions vs one agent cost model; claims A6/S6; survey PDF rebuilt |
| 2026-08-05 | Restore slides 4/9/11/12/23 pre-readability layouts (fix overlaps); 12 settlement clear below |
| 2026-08-05 | Transcripts bilingual: `en/` + `zh-TW/` (37 slides); `translate_transcripts.py`; skill requires both langs |
| 2026-08-05 | Beamer readability pass: larger shared styles; band relayouts 12/18/23/27/34–37; inspect for overflow |
| 2026-08-05 | Rename Beamer out PDF → `publish/out/next-gen-ai-compiler-sharing.pdf` (was expert-briefing) |
| 2026-08-05 | Skill: on every SURVEY.md update — goal-align (goal vs sub-context) + rebuild survey PDF before Beamer |
| 2026-08-05 | Beamer 14/26 band layout (like 24–25); bump Exists/Missing + body fonts on 14/24–26; refresh transcripts |
| 2026-08-05 | Beamer slides 24–25: 3-line bands (title/exists/missing + unlocks); keep Exists on-slide; refresh transcripts |
| 2026-08-05 | Fix Beamer slides 6/11/23 box-on-text overlaps; skill: no box-on-text + pdftoppm inspect |
| 2026-08-05 | Skill: Beamer layout — no overlap boxes/arrows; fit one slide; refine via PDF inspect |
| 2026-08-05 | Skill: Beamer edits must update `publish/beamer/transcripts/` in the same batch |
| 2026-08-05 | Beamer Technical Prediction slides aligned to settled §5.8 (T1–T10 exists/missing/unlocks + FlashInfer/KernelBook evidence); appendix Tier A refreshed |
| 2026-08-05 | Post-§5.8 alignment review: goal/prediction still hybrid; thin fixes (§4 four jobs, FlashInfer in §4.10, §5.5↔§5.8, C2 pressure note, §9 T* loop) |
| 2026-08-05 | Skill harden: **push `main` only** section overrides cloud `cursor/*`+PR defaults; SETUP_GITHUB notes match |
| 2026-08-05 | §5.8 evidence search: +7 digests (FlashInfer-Bench★, KernelBook★, TritonRL, DRTriton, mlir-opt-repl RFC, VibeServe); thin-update T1–T3/T6–T10 exists cells; INDEX **115** |
| 2026-08-05 | SURVEY **§5.8 Technical prediction**: techniques within/outside compiler, critical missing parts, checkpoint→technique map (T1–T10); slides deferred until settled |
| 2026-08-05 | Beamer **Technical Prediction** section: in/out-of-compiler techniques, missing parts, checkpoint unlock map (37 slides) |
| 2026-08-05 | Beamer appendix from `reference/`: evidence map, Tier A products/repos, ★ digests, publication groups (32 slides) |
| 2026-08-05 | Beamer reorder: trends (§1) before verdict; drop claim/systems slides; light Discussion; 26 slides |
| 2026-08-05 | Beamer slide 8 → roadmap spine (Today/Horizon A/B + §5.5 checkpoints); slide 5 target-stack arrow relayout |
| 2026-08-05 | Beamer deck polish (title case, light title, agenda spoken-only weight/contract, TikZ overlap fixes) + per-slide transcripts in `publish/beamer/transcripts/` |
| 2026-08-04 | Add LaTeX Beamer expert briefing (~28 slides, diagram-first; §5→§4→§1) → `publish/out/next-gen-ai-compiler-expert-briefing.pdf` |
| 2026-08-04 | Remove visual posters, PPTX decks, and `build_visual.py` / `build_pptx.py` — PDF-only publish |
| 2026-08-04 | Refresh §5.1 + architecture-evolution visuals; add 2-slide share deck `architecture-51-and-evolution.pptx` |
| 2026-08-04 | Rescan: EmitC-MLGO June 2026 PoR checkpoint (C1 not settled); +CuTeGen ★, CompileIQ agent-skills ★, Hexagon-MLIR; INDEX **108** |
| 2026-08-04 | Distill docs-consolidation + prediction lessons into `.cursor/skills/survey` (SKILL.md architecture rules + survey.md experience log) |
| 2026-08-04 | Consolidate docs into one reading path: fold TAXONOMY/SYSTEMS/CLAIMS/CONFLICTS/WORKFLOW (+ COMPARISON stub) into `docs/SURVEY.md` §0 / §1b / §6–§9; `docs/` = SURVEY + SETUP_GITHUB only |
| 2026-08-04 | Fold STACK into SURVEY §5.6; drop circular SURVEY↔STACK pointers |
| 2026-08-04 | Collect evidence under `reference/` (guide → publications / products / repos) |
| 2026-08-04 | Fold ROADMAP into SURVEY §5.5; drop circular SURVEY↔ROADMAP pointers; remove self-repo name from PDF cover / setup notes |
| 2026-08-04 | Redraw §5.1 architecture + §5.5 architecture-evolution diagrams; add visual posters (architecture stack, Today→A→B evolution) |
| 2026-08-04 | Add agent control-plane substrate digests (Auto, FlowCompile, AgentFlow, Hetero); wire §0.1, Trend B, §4.6, §5.1, §5.7 P3/P22/P23; INDEX **104** |
| 2026-07-31 | Initial scaffold through prediction refocus (C1–C8, §5, tiers) |
| 2026-07-31 | Roadmap + stack reshape + HW codesign (job d); C9–C10; +10 digests; CLAIMS/WORKFLOW/validate |
| 2026-07-31 | Add `publish/` PDF pipeline; export `next-gen-ai-compiler-survey.pdf` |
| 2026-07-31 | Distill methodology into `.cursor/skills/survey` skill |
| 2026-08-03 | PDF publish builds en + zh-CN + zh-TW |
| 2026-08-03 | Keep only English PDF in out/; add graph-heavy PPTX builder |
| 2026-08-03 | Redesign PPTX as editorial idea deck; add PPT_TOOLS.md suggestions |
| 2026-08-03 | Add Compiler 2.0 Ken Kennedy plenary + lineage + MOCHA; SURVEY §1.5 vision map |
| 2026-08-03 | Fix KernelEvolve INDEX title (full paper name); add Meta Engineering blog digest |
| 2026-08-03 | Add Org + Publisher to all digests and INDEX; validate requires fields |
| 2026-08-03 | Visual survey pack: 10 diagram posters + visual PPTX in publish/out |
| 2026-08-03 | SURVEY §5.7: commercialization critical problems (contract, memory, sub-agents, …) |
| 2026-08-03 | Expand §5.7 → P1–P22 (eval, economics, tenancy, IP, versioning, DR, A/B, compliance, …) |
| 2026-08-03 | §5.7 P23: tokens / inference / model capability survey + conclusion |
| 2026-08-03 | Rebuild PDF + visuals (+ commercial/P23 posters) + editorial PPTX |
| 2026-08-03 | Update `.cursor/skills/survey` with §5.7/P23, visuals, Org, hybrid lessons |

## Next actions

1. Test agentic optimization against strong structured-search and conventional baselines.
2. Seek evidence that changes a design choice, especially application gains, new-target transfer, or component replacement.
3. Update the presentation and both transcript languages when that work is requested.
4. Publish this prepared batch only after the maintainer authorizes a push.
