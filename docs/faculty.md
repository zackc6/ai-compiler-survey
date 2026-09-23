# Faculty and industry people behind the survey

Last checked: **2026-09-23**.

This page lists people whose university or company pages, and whose author lines on sources in [`../reference/`](../reference/), connect them to the survey’s agentic-compiler work. Digests do not record academic rank. A name appears here only when a university page states a professor title, or when a paper, talk, or product page names the person and the affiliation is a company.

The list is not every coauthor. Students, research fellows, and uncredited industry teammates stay out.

Companion: [`SURVEY.md`](SURVEY.md) §0 and §5.6.2 · [`../reference/publications/INDEX.md`](../reference/publications/INDEX.md) · [`../reference/products.md`](../reference/products.md)

## How to read the bands

Regions come first. Inside each region the order is: strongly related, then future potential, then others.

**Strongly related.** The person is an author of a system that does one of the four jobs below, and that system is a primary source for the survey.

**Future potential.** The person is an author of a substrate the survey keeps in scope: a compiled agent workflow, a foundation-model “compiler,” a heuristic benchmark that includes compiler tasks, or a megakernel forge. Their home research area is adjacent to compiler construction.

**Others.** The person is a faculty coauthor whose published expertise sits outside compiler construction, or the region has a cited affiliation and no confirmed professor on the author list.

## The four jobs, in words

The survey predicts four agent jobs. Later sections name the job in a sentence instead of a letter.

1. **Online specialization.** An agent searches schedules, flags, or kernels for a live workload. A classical compiler and a test or profile admit the result. Examples: CompileIQ, GEAK, Cake, Argus, MaxKernel.
2. **Offline heuristic and pass synthesis.** An agent writes reviewable pass logic or heuristics offline. The shipped artifact runs inside the classical compiler. Example: Magellan.
3. **Compiler engineering and review.** An agent reviews patches, fixes compiler bugs, or trains against a formal checker. Examples: Archer, llvm-harness, LLM-VeriOpt.
4. **Accelerator bring-up and codesign feedback.** An agent generates a correct backend for a new or future accelerator, using simulation and silicon, and the traces can inform the next ISA or IR. Examples: TritorX, Zomboss. Peak kernel search on an existing GPU or TPU is a different objective.

## Singapore

No professor is an author on the Singapore-affiliated digest.

**AwareCompiler** studies online specialization of compiler pass sequences. Its Nanyang Technological University coauthor, Haoran Luo, is a research fellow. The corresponding authors are at the Institute of Software, Chinese Academy of Sciences, and the University of Chinese Academy of Sciences.

## Hong Kong

### Strongly related

**Shaohua Li**, Assistant Professor, Department of Computer Science and Engineering, Chinese University of Hong Kong.

His faculty page lists compilers, programming languages, software engineering, security, and systems, with emphasis on reliability and performance of classical and AI software stacks. He is an author of [Archer](../reference/publications/archer-paper.md), which reviews LLVM optimization patches with obligations and an executable validation guard, and of [llvm-harness](../reference/publications/llvm-harness.md), which gives agents LLVM middle-end tools, a bug benchmark, and a repair agent. Both are compiler engineering and review.

**Binhang Yuan**, Assistant Professor, Department of Computer Science and Engineering, Hong Kong University of Science and Technology.

His faculty page lists data management and distributed systems for machine learning. He is an author of [Argus](../reference/publications/argus.md). That paper is online specialization: an agent writes GPU kernels in a tile DSL, and compile-time data-flow invariants plus an SMT solver admit or reject the kernel before it runs.

### Others

**Junhui Hou**, Professor, Department of Computer Science, City University of Hong Kong.

His faculty page lists visual computing, geometry, and compression. He is a faculty coauthor of [AgentCompile](../reference/publications/agentcompile.md), an LLM-guided compiler that emits CUDA for inference. The corresponding author on that paper is Zhiyu Zhu at City University of Hong Kong (Dongguan).

## United States

### Strongly related

**Saman Amarasinghe**, Professor, MIT CSAIL.

He is the speaker of the 2026 Ken Kennedy plenary [Compiler 2.0](../reference/publications/compiler-2.0-cgo2026.md). The line of work, including MOCHA, uses machine learning to retarget compilers and to raise abstractions for heterogeneous hardware. The survey treats this as the vision for offline heuristic and pass synthesis that still lands in a classical compiler, with verified rewrite rather than an unconstrained model acting as the optimizer.

**Christopher Ré**, Professor, Stanford University.

He advises the Hazy Research line that produced [KernelBench](../reference/publications/kernelbench.md) and the ThunderKittens kernel library. KernelBench is the public ladder for online specialization: a generated GPU kernel must be correct and faster than a baseline.

**Azalia Mirhoseini**, Professor, Stanford University.

She co-advises KernelBench from the Scaling Intelligence lab. Her survey-facing work is machine-learning systems and automated kernel generation, which is online specialization.

**Christos Kozyrakis**, Professor of Electrical Engineering and Computer Science, Stanford University.

His long-standing work is computer architecture and cloud systems. He is an author of Argus. On that paper the agent searches GPU kernels inside a layout algebra, and an SMT solver supplies the admit check. That is online specialization with a compile-time oracle.

**Tianqi Chen**, Assistant Professor, Carnegie Mellon University.

He is an author of [TVM](../reference/publications/tvm-osdi18.md), [Cake](../reference/publications/cake.md), and [FlashInfer-Bench](../reference/publications/flashinfer-bench.md). The work is machine-learning compilers, typed kernel schedules, and a serving-trace ladder that substitutes kernels into SGLang and vLLM. Cake and FlashInfer-Bench are online specialization. The same papers also list an NVIDIA affiliation.

**Luis Ceze**, Professor, University of Washington.

He is an author of TVM, FlashInfer-Bench, and Cake. The survey-facing expertise is machine-learning systems and production kernel substitution, which is online specialization. He is also Vice President of AI Systems Software at NVIDIA.

**Vijay Janapa Reddi**, Gordon McKay Professor of Electrical Engineering, Harvard University.

He is an author of [JAXBench](../reference/publications/jaxbench.md). The benchmark is online specialization on TPUs: agents hill-climb Pallas kernels against XLA, with hand-tuned Pallas kernels as the reference on a subset of tasks.

**Nathan Bleier**, Assistant Professor, Computer Science and Engineering, University of Michigan.

His faculty page lists architectures for domains that conventional silicon does not serve, including flexible electronics, earable and olfactory computing, and in-space computing. His group’s survey paper is [Zomboss](../reference/publications/zomboss.md). That paper compiles a machine description once, then lets an agent search kernel mappings for an emerging accelerator. That is accelerator bring-up and codesign feedback, on an academic stack rather than a production ASIC.

**Zhiru Zhang**, Professor, School of Electrical and Computer Engineering, Cornell University.

His group works on high-level synthesis, hardware specialization, and design automation for heterogeneous systems. He is an author of [HeuriGym](../reference/publications/heurigym.md), an agent benchmark in which models write and refine heuristics. The task set includes compiler problems, among them e-graph extraction and intra-op parallelization. That is the benchmark face of offline heuristic and pass synthesis.

### Future potential

**Chuang Gan**, Assistant Professor, Manning College of Information and Computer Sciences, University of Massachusetts Amherst, and a research lead at the MIT-IBM Watson AI Lab.

His published expertise is computer vision and embodied agents. He is an author of [FlowCompile](../reference/publications/flowcompile.md), which compiles a structured language-model workflow offline. The survey uses that result as control-plane substrate. It is a workflow compiler, and it is separate from a kernel compiler or an LLVM pass.

### Others

HeuriGym also lists Cornell professors **Carla P. Gomes** and **Samitha Samaranayake**. Their fields are artificial intelligence and optimization. Compiler tasks are one slice of that benchmark.

## China (mainland)

### Strongly related

**Yuqun Zhang**, Associate Professor, Southern University of Science and Technology.

His faculty page lists software engineering, fuzzing, and decompilation. He is a corresponding author of llvm-harness. That system is compiler engineering and review: agents use LLVM-specific tools to understand and fix middle-end bugs, and the authors report an expert review of the remaining failures.

### Future potential

**Zhiyuan Liu**, Associate Professor, Department of Computer Science and Technology, Tsinghua University.

His faculty page lists natural language processing and pretrained models. He is the corresponding author of [ForgeMegakernel](../reference/publications/forgemegakernel.md), in which agents forge decode megakernels and a mid-state test oracle admits them. The survey reads that as a kernel-agent result from an NLP group.

### Note on a non-professor lead

[TileLang](../reference/publications/tilelang.md), the Peking University tiled kernel language the survey treats as an agent target, lists **Zhi Yang** as last author. The School of Computer Science page gives his title as associate researcher, and his interests as AI computing systems and distributed systems. He is omitted from the professor lists for that reason.

## Switzerland

### Strongly related

**Zhendong Su**, Professor, ETH Zurich.

His line of work is compiler testing and language reliability. He is an author of llvm-harness, which is compiler engineering and review, and he was the doctoral advisor of Shaohua Li.

## United Kingdom

### Strongly related

**Lev Mukhanov**, Lecturer at Queen Mary University of London. That title is the assistant-professor rank in the UK.

He is an author of [LLM-VeriOpt](../reference/publications/llm-veriopt.md) (CGO 2026). The paper trains a small model with reinforcement learning to propose LLVM peephole optimizations, and Alive2 is the correctness gate. That combines online specialization of peephole opts with a formal oracle from compiler engineering and review.

## Canada

### Future potential

**Ahmed E. Hassan**, Professor, School of Computing, Queen’s University.

He is an author of [Compiler.next](../reference/publications/compiler-next.md). The paper argues that a future compiler searches prompts, agent configurations, and free parameters of foundation-model software, with quality gates and traces. The survey keeps this as a vision for compiling agent workflows. It is separate from a GPU kernel compiler or an LLVM data plane.

---

## Appendix: Industry

These people are named on company papers, talks, or product pages that the survey cites. They are not listed as current university faculty above. Where a person also holds a university post, that post is already in the regional sections (Tianqi Chen and Luis Ceze).

The same three bands apply. Strongly related means the person’s named work is one of the four jobs. Future potential means a foundation model, a kernel language, or a compiler infrastructure the agents sit on. The last subsection lists team products that do not have one publicly famous individual lead.

### Meta

**Strongly related**

**Chris Cummins** and **Hugh Leather**, Meta AI.

They are the lead authors of the [Meta Large Language Model Compiler](../reference/publications/meta-llm-compiler.md), with Volker Seeker, Dejan Grubisic, Baptiste Rozière, Jonas Gehring, and Gabriel Synnaeve. The models are pretrained on compiler traces and fine-tuned for code-size and disassembly tasks. Cummins also wrote the [public explainer](../reference/publications/cummins-linkedin-llm-compiler.md). The survey uses this line as the foundation-model prior for compiler optimization. It feeds later agents. It is the model, and the pass that ships is still classical. Leather’s earlier compiler-ML work with Cummins is the academic-to-industry line behind that paper. On the LLM Compiler paper his affiliation is Meta AI.

**Gabriel Synnaeve**, Meta FAIR.

He is an author of the Meta Large Language Model Compiler and of [TritorX](../reference/publications/tritorx.md) (*Agentic Operator Generation for ML ASICs*). TritorX is accelerator bring-up and codesign feedback: a constrained agent loop writes Triton kernels for Meta’s MTIA, and the compiler, JIT, and OpInfo tests admit them, on silicon and on a simulator of future devices. Correspondence on that paper is Alec M. Hammond and Jacob Kahn.

**Carole-Jean Wu** and **Gang Liao**, Meta.

They are the corresponding authors of [KernelEvolve](../reference/publications/kernelevolve.md), with Gaoxiang Liu. KernelEvolve is online specialization at fleet scale: agents search kernels for ads-ranking models across NVIDIA GPUs, AMD GPUs, and MTIA, using Triton and lower-level languages, hardware manuals, and cross-stack profilers. Wu’s public reputation is machine-learning systems and accelerators. Liao is the engineering lead named on the paper and the Meta engineering write-up.

**Jason Ansel**, Meta.

He is the author of record for [Helion](../reference/publications/helion-github.md), the PyTorch tile language that lowers to Triton and autotunes many Triton implementations from one kernel. The survey treats Helion as the higher-level surface an online-specialization agent can target. Ansel is also known for the PyTorch compiler stack.

### Google and DeepMind

**Strongly related**

**Mircea Trofin**, Google.

He is an author of [MLGO](../reference/publications/mlgo-paper.md) with Yundi Qian, Eugene Brevdo, Zinan Lin, Krzysztof Choromanski, and Xinliang David Li, and he is a named speaker on the [Magellan LLVM Developers’ Meeting slides](../reference/publications/magellan-llvm-slides.md) with Chen, Novikov, Vũ, and Yazdanbakhsh. MLGO replaces hand-written LLVM inlining policy with a learned advisor inside the production compiler. Magellan is the later, different bet: an agent evolves readable C++ heuristics offline, and those heuristics land in the same classical compiler. The survey keeps those two bets side by side. The digest lists those speakers as Chen, Novikov, Vũ, Trofin, and Yazdanbakhsh. This catalog does not identify that Chen with Tianqi Chen at Carnegie Mellon.

**Xinliang David Li**, Google.

He is an author of MLGO and a long-time LLVM developer. His survey-facing work is the production path for a learned policy inside LLVM’s inlining pass.

**Amir Yazdanbakhsh**, Google.

He is a named author of the Magellan LLVM Developers’ Meeting slides. That talk is offline heuristic and pass synthesis, including production inlining numbers and early XLA graph-rewrite experiments. A JAXBench citation inside the MaxKernel paper also lists him among the benchmark authors.

**Alexander Novikov**, **Ngân Vũ**, and **Matej Balog**, Google DeepMind.

They are equal-contribution leads of [AlphaEvolve](../reference/publications/alphaevolve-paper.md), the evolutionary coding agent Magellan uses to discover compiler heuristics. Novikov and Vũ are also on the Magellan slides. AlphaEvolve itself is a general coding agent. The compiler-specific result is Magellan’s offline heuristic and pass synthesis. **Pushmeet Kohli** supervised the AlphaEvolve research program at DeepMind. The paper’s author list also includes university coauthors. This appendix keeps the company staff.

### OpenAI

**Future potential**

**Philippe Tillet**, OpenAI.

He created Triton, the Python kernel language and compiler that GEAK, KernelEvolve, TritorX, and Helion target. Triton is the data-plane language those agents write. Tillet’s own surveyed role is the language and its compiler, which grew out of his Harvard dissertation on compilers for blocked GPU algorithms.

### Modular

**Future potential**

**Chris Lattner**, Modular.

He created LLVM and led MLIR. The survey’s agent papers review, fuzz, and evolve LLVM, and they lower kernels through MLIR-family stacks. He is also the author of Modular’s [note on the Claude C Compiler](../reference/publications/modular-claude-c-compiler.md), which treats a generated C compiler as real progress that still depends on tests and engineering practice. His surveyed role is the classical compiler substrate and that public reading of generated compilers.

### AMD

**Strongly related**

**Emad Barsoum**, AMD, last author of [GEAK](../reference/publications/geak.md).

The paper’s primary authors are Jianghui Wang and Vinay Joshi, with Saptarshi Majumder, Xu Chao, Bin Ding, Ziqiong Liu, Pratik Prabhanjan Brahma, Dong Li, and Zicheng Liu. GEAK is online specialization for AMD GPUs: a language-model agent writes Triton kernels and iterates with compiler and performance feedback. Later GEAK versions add a serving path. Barsoum is the last author on the original paper.

### Team results without one famous individual lead

These shipping systems are primary survey evidence. Their public write-ups name a team, or a product, and no one person on the byline is a widely known compiler figure. They stay in this appendix so the company map is complete.

| System | Company | What the work is |
|---|---|---|
| [MaxKernel](../reference/publications/maxkernel.md) | Google | Online specialization for TPUs. The agent proposes Pallas kernels. XLA and a numerical harness admit them, and hardware traces guide the search. The author list is Shangkun Wang, Gerson Kroiz, George Vanica, Deepak Patil, Andi Gavrilescu, Hassan Sipra, and Sethu Sankaran. |
| [CompileIQ](../reference/publications/compileiq-deep-dive.md) | NVIDIA | Online specialization of CUDA compiler controls. Search produces versioned compiler-control files, and a statistical check decides whether the specialized build wins. The survey cites the product docs and the developer blog, which do not identify a single public technical lead. |
| [Hyperloom](../reference/publications/hyperloom.md) | AMD | An end-to-end Instinct serving harness. Kernel work is delegated to GEAK or another kernel agent, and a state file plus a critic decide what to keep. The survey cites the system paper as a team result. |
