$ErrorActionPreference = "Stop"
$root = Split-Path $PSScriptRoot -Parent
$pubDir = Join-Path $root "publications"

$items = @(
  @{ slug="archer-paper"; title="Archer: Towards Agentic Review for Compiler Optimizations"; year="2026"; kind="paper"; group="Source control & review agents"; url="https://arxiv.org/html/2607.01808"; contrib=@("First agentic review tool specialized for compiler optimization patches","Obligation-guided analysis from historical bug fixes","Deterministic validation guard (Alive2/LLUBI/opt) before admitting findings","Evaluated on hundreds of recent LLVM GitHub PRs"); summary="Presents Archer, an LLM agent that reviews LLVM optimization PRs with compiler-specific knowledge and executable evidence, reporting high rates of semantic bugs in open and closed PRs and arguing that generic code-review agents are insufficient for compilers."; takeaways=@("SCM (GitHub PRs) is a first-class surface for AI-compiler agents","Evidence-gated comments are the right pattern for HITL","Directly supports survey gaps 4.2, 4.5, 4.8") },
  @{ slug="archer-github"; title="cuhk-s3/Archer (GitHub)"; year="2026"; kind="code"; group="Source control & review agents"; url="https://github.com/cuhk-s3/Archer"; contrib=@("Runnable agent taking --pr LLVM PR ids","Pass knowledge loading + structured PoC reviews","Tooling for verify/difftest/trans against local LLVM tree"); summary="Open-source implementation of Archer for evidence-backed LLVM PR review focused on middle-end optimizations."; takeaways=@("Primary SCM-integrated compiler review reference","Pair with Discourse experience report and the paper") },
  @{ slug="gerrit-ai-code-review"; title="Gerrit plugin: ai-code-review (googlesource)"; year="2024+"; kind="code"; group="Source control & review agents"; url="https://gerrit.googlesource.com/plugins/ai-code-review/"; contrib=@("In-Gerrit AI comments after patch sets","/review and /review_last commands","Optional votes; ChatGPT/Ollama/Azure backends"); summary="Official-style Gerrit plugin that posts LLM review comments on Changes—generic AI review inside Gerrit workflows used by large orgs."; takeaways=@("Shows agents inside Gerrit (not only GitHub)","Not compiler-oracle-aware—contrast with Archer","Delivery channel for future Alive2-backed review") },
  @{ slug="reviewai-gerrit-plugin"; title="amarula/reviewai-gerrit-plugin"; year="2025+"; kind="code"; group="Source control & review agents"; url="https://github.com/amarula/reviewai-gerrit-plugin"; contrib=@("Review Agent sidebar on Gerrit change page","Multi-provider LangChain routes","Scoped patch-set / commit-message reviews"); summary="Gerrit plugin exposing a chatbot-style Review Agent in the change UI for interactive AI review."; takeaways=@("HITL UX pattern for Gerrit","Still general-purpose unless paired with compiler tools") },
  @{ slug="gerritforge-ai-review-provider"; title="GerritForge/ai-review-agent-provider"; year="2025+"; kind="code"; group="Source control & review agents"; url="https://github.com/GerritForge/ai-review-agent-provider"; contrib=@("Provider backend for Gerrit v3.14+ native AI chat","Multi-LLM adapter (Gemini/OpenAI/Anthropic/Ollama)"); summary="Implements Gerrit's AI Code Review Agent API so in-UI chat can call external LLMs."; takeaways=@("Interface layer matching gap 4.5 for SCM hosts","Compiler specialization still an open integration") },
  @{ slug="openevolve"; title="OpenEvolve (AlphaEvolve-style OSS)"; year="2025"; kind="code"; group="Source control & review agents"; url="https://github.com/algorithmicsuperintelligence/openevolve"; contrib=@("Open-source evolutionary coding agent","MAP-Elites style evolution with LLM proposals","Reproducibility/seeding features advertised"); summary="OSS implementation of DeepMind AlphaEvolve-style evolutionary optimization; Magellan talks cite OpenEvolve as a path for open-sourcing heuristic discovery."; takeaways=@("Bridge from closed Magellan/AlphaEvolve to public experiments","Relevant to offline heuristic synthesis control plane") },
  @{ slug="heurigym"; title="HeuriGym (cornell-zhang/heurigym)"; year="2025"; kind="code"; group="Source control & review agents"; url="https://github.com/cornell-zhang/heurigym"; contrib=@("Agentic benchmark for LLM-crafted heuristics","Includes compiler tasks (e-graph extraction, intra-op parallelism)","Quality-Yield Index metric"); summary="ICLR'26-oriented benchmark where LLMs propose and refine heuristics via code execution feedback across EDA/compiler/logistics/biology tasks; cited in Magellan-related literature."; takeaways=@("Fills unified-benchmark gap for heuristic synthesis","Compiler problems included—not only logistics toys") },
  @{ slug="kernelagent"; title="meta-pytorch/KernelAgent"; year="2025"; kind="code"; group="Source control & review agents"; url="https://github.com/meta-pytorch/KernelAgent"; contrib=@("Multi-agent PyTorch→Triton generation","Strict runtime verification workers","Hardware-guided optimization pipeline; KernelBench-oriented"); summary="Meta PyTorch org agent framework that synthesizes and verifies Triton kernels with sandboxed workers and iterative profiling feedback."; takeaways=@("GitHub-hosted kernel-agent reference beside KernelBench","Matches Trend D and hybrid admit gates") },
  @{ slug="compileiq-github"; title="NVIDIA/CompileIQ (GitHub)"; year="2026"; kind="code"; group="Source control & review agents"; url="https://github.com/NVIDIA/CompileIQ"; contrib=@("OSS optimizer for NVIDIA compiler Advanced Controls","Search-space catalogs released via GitHub Releases","Produces distributable ACF artifacts"); summary="Public repository for CompileIQ: evolutionary HPO over NVCC/PTXAS controls for CUDA/Triton/Helion kernels after source tuning plateaus."; takeaways=@("Vendor control-plane tuning as a GitHub-deliverable artifact","ACF caching pattern for gap 4.3") },
  @{ slug="claudes-c-compiler-github"; title="anthropics/claudes-c-compiler"; year="2026"; kind="code"; group="Source control & review agents"; url="https://github.com/anthropics/claudes-c-compiler"; contrib=@("Full SCM history of agent-written C compiler","Multi-arch Linux-capable claims with heavy test suites","Human-authored caution not to use in production"); summary="GitHub artifact of Anthropic's agent-team C compiler experiment—agents as compiler engineers with tests as the product."; takeaways=@("Source control as provenance for agent-authored TCB","Supports gaps 4.8/4.9 on ownership and security") },
  @{ slug="ml-compiler-opt-github"; title="google/ml-compiler-opt"; year="2021+"; kind="code"; group="Source control & review agents"; url="https://github.com/google/ml-compiler-opt"; contrib=@("Training infra for LLVM MLGO advisors","Inlining and regalloc policy training","Corpus/demo pipelines"); summary="Companion GitHub repo to in-tree LLVM MLGO: trains neural policies that replace heuristics inside the production compiler hosted on llvm-project."; takeaways=@("Classic traditional ML-in-compiler training host","Contrast with Magellan synthesizing C++ instead of nets") },
  @{ slug="hintpilot-github"; title="ZJU-PL/hintpilot"; year="2026"; kind="code"; group="Source control & review agents"; url="https://github.com/ZJU-PL/hintpilot"; contrib=@("Open implementation of HintPilot hint synthesis","RAG + profile-guided refine loop"); summary="Code release for HintPilot's semantics-preserving compiler-hint agent."; takeaways=@("Reproducible hybrid Selector path") },
  @{ slug="llvm-project-github"; title="llvm/llvm-project (host repository)"; year="ongoing"; kind="code"; group="Source control & review agents"; url="https://github.com/llvm/llvm-project"; contrib=@("Primary public host for LLVM/Clang/MLIR monorepo","GitHub PR review surface used by Archer and Discourse agent studies","Contains MLGO advisor hooks in-tree"); summary="The production compiler codebase and SCM surface on which many AI-compiler agents operate (pass landing, PR review, MLGO inference)."; takeaways=@("Anchor host repo for GitHub-centric compiler agents","Pair with Gerrit plugins for non-LLVM large-org workflows") }
)

function Write-Digest($it) {
  $path = Join-Path $pubDir ($it.slug + ".md")
  $contrib = ($it.contrib | ForEach-Object { "- $_" }) -join "`n"
  $takes = ($it.takeaways | ForEach-Object { "- $_" }) -join "`n"
  $body = @"
# $($it.title)

| Field | Value |
|---|---|
| **Year** | $($it.year) |
| **Type** | $($it.kind) |
| **Group** | $($it.group) |
| **Link** | [$($it.url)]($($it.url)) |

## Key contributions

$contrib

## Summary

$($it.summary)

## Key takeaways

$takes

## Why it matters for this survey

Mapped in ``reference/repos.md`` to SCM/review context and to gaps in ``docs/SURVEY.md`` §4. Prefer the primary link above when citing.
"@
  Set-Content -Path $path -Value $body -Encoding UTF8
}

foreach ($it in $items) { Write-Digest $it }

# Append to INDEX
$indexPath = Join-Path $pubDir "INDEX.md"
$existing = Get-Content $indexPath -Raw
$rows = $items | ForEach-Object {
  "| $($_.year) | $($_.kind) | $($_.group) | [$($_.title)]($($_.slug).md) | [source]($($_.url)) |"
}
# bump total line if present
$newBlock = ($rows -join "`n") + "`n"
if ($existing -notmatch "archer-paper") {
  $updated = $existing -replace "(\*\*Total:\*\* )(\d+)( digests)", {
      param($m)
      # simpler: append before Total
      $m.Value
    }
  # Append rows before Total line
  if ($existing -match '(?s)(.*\n)(\*\*Total:\*\* )(\d+)( digests.*)') {
    $count = [int]$Matches[3] + $items.Count
    $updated = $Matches[1] + $newBlock + $Matches[2] + $count + $Matches[4]
    # Fix: Matches from -match on $existing
  }
  $m = [regex]::Match($existing, '(?s)(?<head>.*\n)(?<tot>\*\*Total:\*\* )(?<n>\d+)(?<tail> digests.*)')
  if ($m.Success) {
    $count = [int]$m.Groups['n'].Value + $items.Count
    $updated = $m.Groups['head'].Value + $newBlock + $m.Groups['tot'].Value + $count + $m.Groups['tail'].Value
    Set-Content -Path $indexPath -Value $updated -Encoding UTF8
  } else {
    Add-Content -Path $indexPath -Value "`n$newBlock"
  }
}

Write-Output "Wrote $($items.Count) SCM digests"
