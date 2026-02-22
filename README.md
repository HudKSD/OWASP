# OWASP AI Attack Surface Framework (AI ASF)

Status: Draft (community bootstrapping)

This project provides a vendor neutral, architecture first method to identify, classify, and document the attack surface of AI systems, including:
- LLM applications
- Retrieval augmented generation (RAG)
- Agentic systems with tool use and action execution
- Classical ML pipelines
- Fine tuning and training pipelines
- Multi tenant inference platforms

The core deliverables are:
- A detailed attack surface taxonomy for AI systems
- Surface Cards (standardized “units” for security review)
- Reference architecture patterns with detailed Mermaid diagrams
- A repeatable “Attack Surface Review” methodology
- Crosswalk mappings to existing OWASP AI resources and external frameworks

Why this exists:
Teams struggle to apply AI security guidance because the architecture decomposition step is missing or inconsistent. This framework standardizes that step so that threat modeling, control selection, testing, and telemetry planning become repeatable and comparable across systems.

## What this project is not
- It is not a new Top 10 list
- It is not a replacement for verification standards (AISVS, LLMSVS, MLSVS)
- It is not a vendor product comparison
- It does not publish weaponized exploit code or step by step offensive instructions
- It does not attempt to solve AI safety as a whole, it focuses on security relevant attack surfaces and controls

## How to use this framework (practitioner workflow)
1. Identify your architecture pattern (or create one from the pattern template)
2. Create an AI Attack Surface Map (ASM) using the template
3. Enumerate surfaces and trust boundaries using the taxonomy and surface cards
4. Map the surfaces to:
   - OWASP Top 10 for LLM Apps 2025
   - OWASP ML Security Top 10
   - AISVS categories
   - OWASP AI Testing Guide layers
   - MITRE ATLAS techniques (optional)
5. Produce a scoped test plan and telemetry plan
6. Re run after major changes (model swap, new tool, new connector, new prompt policies, new memory mode)

Outputs you should produce for every real system:
- Trust boundary diagram
- Data flow diagram
- Privilege flow summary (who can call what, where tokens cross boundaries)
- Surface inventory (list of all interfaces and channels)
- Control mapping and testing plan
- Logging and detection plan
- AI incident response notes (what constitutes an AI security incident for this system)

## Detailed reference diagram (Agentic RAG + tools + training lifecycle)

Paste this diagram into any Mermaid renderer or GitHub Markdown.

```mermaid
flowchart TB

%% Legend:
%% - Red nodes: Primary external entry points
%% - Orange nodes: High risk surfaces (often abused)
%% - Blue nodes: Core system components
%% - Green nodes: Control and governance components
%% - Gray nodes: Observability components

classDef entry fill:#ffdddd,stroke:#cc0000,stroke-width:2px,color:#111;
classDef highrisk fill:#ffe7cc,stroke:#cc6600,stroke-width:2px,color:#111;
classDef core fill:#ddeeff,stroke:#2255aa,stroke-width:1.5px,color:#111;
classDef control fill:#ddffdd,stroke:#228822,stroke-width:1.5px,color:#111;
classDef obs fill:#eeeeee,stroke:#666666,stroke-width:1px,color:#111;

subgraph Z0["Zone 0: Users and Clients"]
  U1["End User"]:::entry
  U2["Internal Analyst"]:::entry
  UI["Web or Mobile UI"]:::core
  SDK["Client SDK"]:::core
end

subgraph Z1["Zone 1: Application Orchestration"]
  WAF["API Gateway / WAF"]:::control
  AUTH["AuthN / AuthZ (OIDC, SSO, API Keys)"]:::control
  APP["App Backend"]:::core
  ORCH["Prompt Orchestrator"]:::core
  PROMPT["Prompt Template Store"]:::highrisk
  POLICY["Policy Engine (guardrails, allow lists, deny lists)"]:::control
  MEM["Conversation Memory / Session Store"]:::highrisk
  OUT["Output Renderer (UI, API, downstream systems)"]:::highrisk
end

subgraph Z2["Zone 2: Model Runtime"]
  LLMGW["LLM Gateway (routing, caching, quotas)"]:::highrisk
  LLM1["LLM Inference (provider or self hosted)"]:::core
  EMB["Embedding Model Endpoint"]:::core
  SAFETY["Safety Filters (toxicity, policy checks)"]:::control
end

subgraph Z3["Zone 3: Retrieval and Knowledge"]
  RETQ["Retrieval Query Builder"]:::highrisk
  VDB["Vector DB (indexes, embeddings)"]:::highrisk
  DOCS["Document Store (raw corpora)"]:::highrisk
  CONN["Connectors (SaaS, file shares, web, tickets)"]:::highrisk
  INGEST["Ingestion Pipeline (chunk, parse, embed)"]:::highrisk
end

subgraph Z4["Zone 4: Tools and Actions"]
  TOOLRT["Tool Router / Function Calling Interface"]:::highrisk
  TOOLGW["Tool Gateway (policy enforcement, signing)"]:::control
  SANDBOX["Tool Execution Sandbox (container, VM)"]:::control
  MCP["MCP Server(s) / Plugin Hosts"]:::highrisk
  INTAPI["Internal Services APIs (CRM, HR, Finance)"]:::highrisk
  EXTAPI["External APIs (email, search, payments)"]:::highrisk
end

subgraph Z5["Zone 5: Data, Training, and Supply Chain"]
  DSRC["Data Sources (prod logs, vendor data, labeled sets)"]:::highrisk
  LABEL["Labeling and Curation"]:::highrisk
  TRAIN["Training or Fine Tune Pipeline"]:::highrisk
  EVAL["Evaluation Harness (red team sets, benchmarks)"]:::highrisk
  REG["Model Registry / Artifact Store"]:::highrisk
  CICD["CI/CD for models, prompts, policies"]:::highrisk
  SBOM["AIBOM / SBOM Generator and Attestations"]:::control
end

subgraph Z6["Zone 6: Observability and Response"]
  LOG["Central Logging"]:::obs
  MET["Metrics and Tracing"]:::obs
  AUD["Audit Store (who asked what, who approved what)"]:::obs
  SIEM["SIEM / Detection Engineering"]:::obs
  IR["Incident Response Runbooks"]:::control
end

U1 --> UI --> WAF --> AUTH --> APP
U2 --> SDK --> WAF --> AUTH --> APP
APP --> ORCH
ORCH <--> PROMPT
ORCH <--> POLICY
ORCH <--> MEM
ORCH --> LLMGW
LLMGW --> SAFETY --> LLM1
ORCH --> RETQ --> VDB
CONN --> INGEST --> EMB --> VDB
INGEST --> DOCS
VDB --> ORCH
ORCH --> LLMGW
ORCH --> TOOLRT --> TOOLGW --> SANDBOX
SANDBOX --> MCP
SANDBOX --> INTAPI
SANDBOX --> EXTAPI
MCP --> SANDBOX
LLM1 --> ORCH --> OUT --> UI
DSRC --> LABEL --> TRAIN --> REG
REG --> CICD --> LLMGW
EVAL --> CICD
TRAIN --> EVAL
SBOM --> REG
APP --> LOG
ORCH --> LOG
LLMGW --> LOG
TOOLGW --> LOG
SANDBOX --> LOG
VDB --> LOG
AUTH --> AUD
POLICY --> AUD
LOG --> SIEM
MET --> SIEM
SIEM --> IR

class U1,U2 entry;
class PROMPT,MEM,OUT,LLMGW,RETQ,VDB,DOCS,CONN,INGEST,TOOLRT,MCP,INTAPI,EXTAPI,DSRC,LABEL,TRAIN,EVAL,REG,CICD highrisk;
class APP,ORCH,LLM1,EMB,UI,SDK core;
class WAF,AUTH,POLICY,SAFETY,TOOLGW,SANDBOX,SBOM,IR control;
class LOG,MET,AUD,SIEM obs;
```

## Repo tour

* docs/01-taxonomy: the attack surface taxonomy, trust boundaries, surface cards
* docs/02-methodology: the repeatable process and artifacts
* docs/03-patterns: detailed architecture patterns with per pattern surface inventories
* docs/04-mappings: crosswalks to OWASP and external frameworks
* docs/05-appendices: telemetry guidance, assurance levels, examples, references
* templates: copy and paste templates for contributors and practitioners
* schemas: a machine readable JSON schema for an AI Attack Surface Map
* tools: optional scripts to validate maps and lint mappings
