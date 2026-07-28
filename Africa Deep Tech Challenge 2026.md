Africa Deep Tech Challenge 2026
The Laptop LLM Challenge: Build On-Device AI for the Hardware Africa Actually Has

About the challenge
Africa is not excluded from the language model revolution. The bottleneck is no longer research or raw model availability - it is access economics. Cloud-hosted LLMs require API fees, stable fiber, and sustained electricity. For a university student in Lagos, an extension officer in Arusha, or a small-business owner in Dakar, these are not minor frictions - they are blockers.

Africa Deep Tech Challenge 2026 (inspired by the Africa AI XPrize) is an engineering-first competition to make useful language-model applications run well on the computers Africans already own: mid- and low-end commodity laptops. We are not building for exotic edge silicon. We are building for the 8 GB laptop with integrated graphics - the machine sitting on millions of desks, in classrooms, clinics, and corner shops across the continent.

You could be the one to democratize access to low cost inference for the continent.

This is an applied systems engineering contest. Hitting genuinely useful performance on commodity hardware requires optimization across the full stack: model selection and fine-tuning, quantization and compilation, memory and cache management, retrieval-augmented generation over local corpora, and application UX that makes such a model feel responsive.

Get started
Register on DevPost for the Africa Deep Tech Challenge 2026

Form or join a team of 1 to 3 people and pick your problem domain
Clone the submission template
Test your model locally by cloning the model profiler. Ensure your model and submission formats are perfectly compatible with the ADTC evaluation pipeline. The local profiler allows you to run latency, throughput, memory, and CPU checks directly on your target hardware.
Apply for up to 5 hours of GPU credits courtesy of Udutech to train your model.
Check out the rules and submission requirements, then start building!
Requirements
What to Build
Participants build a working, end-to-end, on-device Language Model that runs without cloud dependencies on the ADTC Standard Laptop (defined below). The model must address one of the published problem domains

Each team selects one primary domain. These are the ADTC standardized benchmarking domains; validation sets are provided for each.

Math \& Scientific Reasoning - problem solving, proof assistance, scientific question-answering, and quantitative reasoning tasks.

Healthcare \& Medical - clinical information, medical Q\&A, triage support, and patient education.

Agriculture - crop, livestock, weather, and market advisory for farmers and extension officers.

Creative Writing - story generation, editing assistance, poetry, and narrative support across languages.

Coding Assistants - code generation, debugging help, and programming tutoring across common languages.

Corporate / Enterprise - knowledge-work productivity: summarization, drafting, and analysis for small and medium enterprises.

Autonomous AI Agents - local orchestration, task automation, and privacy-focused workflow management using decentralized tools and messaging interfaces.



All submissions are evaluated against a single, published reference hardware profile. This eliminates fragmentation and gives every participant a target they can design for. Participants may develop on any hardware, but final benchmarks and audits are reported against the Standard Laptop profile.



Component

ADTC Standard Laptop

CPU

Intel Core i5 10th–12th gen OR AMD Ryzen 5 3000–5000 (x86-64)

RAM

8 GB DDR4

Graphics

Integrated only (Intel UHD / Iris Xe or AMD Radeon integrated). No discrete GPU.

Storage

256 GB SSD

OS (reference)

Ubuntu 22.04 LTS

Representative Price

$400–$500 new / $150–$250 refurbished



What to Submit
Open Source Github repo that leverages the approved ADTC 2026 Report Template
A comprehensive project report including:
Problem definition and context
Identified constraints (e.g. power, data, compute, connectivity)
Documentation of design alternatives and final decisions
Tools used and why they were chosen
Performance tests and benchmarks
Screenshots or short videos showing your build in action
A short video (max 2 minutes) explaining your solution and development journey
Updated repo, documentation and video (if part of semi-final or final round)


Leaderboard Scoring
Stotal = 0.50⋅Sacc+0.30⋅Sperf+0.20⋅Seff−Pthermal

Component

Weight

Formula

Notes

Sacc

50%

Weighted average of model response scored between 0 and 100 by a Judge.

Weighted combination of automated benchmark scores and qualitative assessment of model prompt responses by the judge panel.

Sperf

30%

100 × (TPSact ÷ TPSmax)



TPS\_REFERENCE = 15.0 provisional

Seff

20%

Seff = 100 × ((7 GB − Peak RAM) ÷ 7 GB)



Rewards lower RAM usage. The less memory consumed relative to the 7 GB budget, the higher the score.

Peak RAM = 7 GB

Pthermal

\-10 points
-10 if throttled or temp > 85°C

Else 0



Prizes
$16,500+ in prizes+ other prizes
Grand Prize
$8,000 in cash
1 winner
Second Place
$4,000 in cash
1 winner
3rd Place
$3,000 in cash
1 winner
Best African Use Case
$1,500 in cash
1 winner
Finalist Stipends
10 winners
$250 (In GPU Credits) for up to 10 finalists

Semifinalist Stipends
20 winners
$50 (In GPU Credits) for up to 20 semi finalists

Judging Criteria

Model Accuracy \& Quality

A combination of multiple-choice benchmarks and qualitative evaluations that includes accuracy of prompts, quality of documentation

Model Throughput Performance

Evaluated relative to the maximum observed tokens per second

Model Efficiency

Rewards lower RAM utilization profiles relative to the maximum memory budget

African Use Case Bonus

Up to 10 extra points awarded for how applicable the model is to a real African use case

Hardware \& Thermal Penalties

10 points deducted if core/package temperature exceeds 85∘C or if thermal throttling is flagged. OOM or sandbox execution crash results in disqualification

