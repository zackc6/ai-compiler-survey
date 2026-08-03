#!/usr/bin/env python3
"""Protect domain terms during machine translation of the survey."""

from __future__ import annotations

# Longer phrases first. Values are Simplified Chinese; OpenCC derives Traditional.
GLOSSARY_EN_TO_ZH_CN: list[tuple[str, str]] = [
    ("Agents own", "智能体负责"),
    ("agents own", "智能体负责"),
    ("Compilers own", "编译器负责"),
    ("compilers own", "编译器负责"),
    ("agentic compiler", "智能体编译器"),
    ("Agentic compiler", "智能体编译器"),
    ("Agentic Compiler", "智能体编译器"),
    ("Next-Generation AI Compiler Survey", "下一代 AI 编译器综述"),
    ("control plane", "控制面"),
    ("data plane", "数据面"),
    ("bring-up", "使能/拉起"),
    ("codesign", "软硬件协同设计"),
    ("co-design", "软硬件协同设计"),
    ("HW–SW codesign", "软硬件协同设计"),
    ("HW-SW codesign", "软硬件协同设计"),
    ("living survey", "持续更新型综述"),
    ("evidence tier", "证据层级"),
    ("Evidence tier", "证据层级"),
    ("Tier A", "A 级证据"),
    ("Tier B", "B 级证据"),
    ("Tier C", "C 级证据"),
    ("pass list", "优化遍序列"),
    ("pass sequences", "优化遍序列"),
    ("heuristic synthesis", "启发式综合"),
    ("offline heuristic", "离线启发式"),
    ("online specialization", "在线特化"),
    ("admit gate", "接纳门控"),
    ("fallback", "回退路径"),
    ("oracles", "判定预言机"),
    ("oracle", "判定预言机"),
    ("digests", "文献摘要"),
    ("digest", "文献摘要"),
    ("falsifiable", "可证伪的"),
    ("North star", "北极星目标"),
    ("north star", "北极星目标"),
    ("Agents", "智能体"),
    ("agents", "智能体"),
    ("Agent", "智能体"),
    ("agent", "智能体"),
]

# Keep proper nouns / IR names untouched via placeholders.
PROTECT_TERMS: list[str] = [
    "ACCLAIM",
    "Magellan",
    "AlphaEvolve",
    "OpenEvolve",
    "CompileIQ",
    "KernelEvolve",
    "TritorX",
    "KernelBench",
    "KernelBench-X",
    "KernelLLM",
    "KernelAgent",
    "KernelBlaster",
    "AutoKernel",
    "KForge",
    "Kernel Forge",
    "HintPilot",
    "AgentCompile",
    "AutoPass",
    "Compiler-R1",
    "LLM-VeriOpt",
    "mlirAgent",
    "MLGO",
    "CompilerGym",
    "Alive2",
    "StableHLO",
    "OpenXLA",
    "TensorRT-LLM",
    "TorchInductor",
    "torch.compile",
    "PyTorch",
    "Triton",
    "Helion",
    "CUDA Tile",
    "Tile IR",
    "CuTe",
    "MLIR",
    "LLVM",
    "IREE",
    "XLA",
    "Inductor",
    "GEAK",
    "MTIA",
    "NPU",
    "GPU",
    "ASIC",
    "ACF",
    "MCP",
    "OpInfo",
    "PTX",
    "NVCC",
    "PTXAS",
    "HIP",
    "SYCL",
    "FlashAttention",
    "CUTLASS",
    "Archer",
    "Souper",
    "IR2Vec",
    "EmitC",
]


def apply_glossary(text: str) -> str:
    for en, zh in GLOSSARY_EN_TO_ZH_CN:
        text = text.replace(en, zh)
    return text


def protect(text: str) -> tuple[str, dict[str, str]]:
    mapping: dict[str, str] = {}
    out = text
    for i, term in enumerate(sorted(PROTECT_TERMS, key=len, reverse=True)):
        token = f"XPROTECT{i}X"
        if term in out:
            mapping[token] = term
            out = out.replace(term, token)
    return out, mapping


def unprotect(text: str, mapping: dict[str, str]) -> str:
    for token, term in mapping.items():
        text = text.replace(token, term)
    return text
