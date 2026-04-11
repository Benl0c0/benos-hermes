---
name: benos-kira-architecture
description: BEN//OS KIRA (Hierarchical Multi-Agent System) Architecture. Defines the complete agent hierarchy, roles, director chains, and tech stack (Paperclip + OpenClaw + Hermes + AnythingLLM). Use this skill when implementing the full KIRA system or adding new agents.
version: 1.0.0
author: Hermes Agent (from BEN//OS Wissensbasis)
license: MIT
metadata:
  hermes:
    tags: [BEN//OS, KIRA, Hierarchical, Director-Agent, Multi-Agent-System, Paperclip, OpenClaw]
    related_skills: [benos-agent-patterns, benos-multi-agent-protocol, benos-cost-routing]
    source: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/Good to know/
---

# BEN//OS KIRA Architecture

## Trigger Conditions
- Implementing the full KIRA agent system
- Adding new agents to the hierarchy
- Setting up Paperclip orchestration layer
- Configuring director-subordinate relationships
- Debugging coordination failures between agents
- Deploying new agent domains (Research, Content, Trading)

## Architecture Overview (Tech Stack)

```
Paperclip (Orchestration Layer)
    ↓
OpenClaw (Agent Runtime - Always-On)
    ↓
Hermes (Self-Learning + Skill Execution)
    ↓
AnythingLLM (RAG + Knowledge Base)
```

## Step 1: Agent Hierarchy Structure

```
KIRA (CEO Agent) - Central orchestrator
├── Intel Director
│   ├── Web News Agent (scrapes RSS, news sites)
│   ├── YouTube Intel Agent (analytics, trends)
│   ├── Reddit Scout (subreddit monitoring)
│   ├── GitHub Monitor (repo activity, issues)
│   └── X/Twitter Scanner (Grok-powered social intel)
├── Content Director
│   ├── Writer Agent (blog articles, docs)
│   ├── Video Script Agent (YouTube scripts)
│   └── Distribution Agent (publishing, scheduling)
├── Trading Director
│   ├── Market Analysis Agent (trends, signals)
│   ├── Backtest Agent (strategy validation)
│   └── Signal Agent - MANUAL RELEASE ONLY (trading triggers)
└── CTO Agent
    ├── Cost Monitor (token budgets, spending alerts)
    └── Model Router (S1-S5 routing enforcement)
```

## Step 2: Director Pattern Requirements

**Each Director must implement:**

1. Task decomposition: Break requests into atomic subtasks
2. Sub-agent assignment: Route subtasks to appropriate agents
3. Deadline enforcement: Track subtask timeouts
4. Result aggregation: Combine subtask results into final output
5. Escalation: Report failures to KIRA CEO

**Example Director workflow:**
```
Request: "Gather intel on competitor X"
↓ Decompose:
  - "Search web for Competitor X news (last 30 days)"
  - "Check GitHub repos for Competitor X activity"
  - "Scan Reddit for mentions of Competitor X"
  - "Check YouTube for Competitor X videos"
↓ Assign to agents with task_id tracking
↓ Wait (aggregate results)
↓ If any failure: retry once → if still fail: continue with partial
↓ Generate consolidated summary → return to CEO
```

## Step 3: Agent Owned Resources

**Never share resources without explicit ownership:**
- Filesystem: Each agent writes to its own subdirectory
- Database tables: Separate tables/rows per agent
- API quotas: Track per-agent usage through TOOLS.md
- Token budgets: Each agent has monthly cap enforced by CTO

**TOOLS.md entries required:**
```
[Agent Name] - purpose
Primary model tier: S3 (or as specified)
Budget: $X/month
Owned resources: ~/agents/intel/web-news-agent/ (path)
Caller permissions: Intel Director, KIRA CEO only
```

## Step 4: Self-Learning Loop (Hermes Integration)

Hermes integration phases:
1. Initial deployment: agents run with defined prompts+configs
2. Performance tracking: Log token usage, success rate, task completion time
3. Weekly review: CTO Cost Monitor identifies wasters
4. Prompt refinement: Low-performing agents get prompt-tuned automatically (Hermes feature)
5. Pattern emergence: Successful patterns shared across agent families

**KIRA must store:**
- Agent performance metrics per task type
- Prompt versions and their success rates
- Cost per agent and per task category
- Failure modes and resolution time

## Step 5: Fallback and Degradation

**Tiered fallback:**
```
Agent offline → Spawn new instance (if possible)
Agent timeout → Retry once with same task
Agent failure → Reassign to alternate agent with same capabilities
Model unavailable → Route to backup model in same tier
```

**Degraded operation mode:**
If too many agents failing, KIRA should:
- Skip non-critical intel (rely on cached data)
- Reduce freshness requirements (e.g., "last 7 days" instead of "last 24h")
- Notify Ben of degraded service

## Step 6: Dashboard Integration

KIRA must publish metrics for the BenOS Dashboard:
- Active agents count and status
- Token spending by agent (cumulative, current month)
- Task queue length per director
- Success/failure rate per agent (24h rolling)
- Warning thresholds (budget 80%, agent failures >3, queue backlog >10)

**Dashboard API format:**
```json
{
  "timestamp": "2026-03-29T12:34:56Z",
  "active_agents": 12,
  "monthly_spend_usd": 45.67,
  "agent_status": [
    { "name": "intel-director", "state": "healthy", "tasks_processed": 156 },
    ...
  ]
}
```

## Pitfalls
- Undefined ownership → agents stepping on each other's toes
- No cost caps → runaway spending hard to trace
- Missing director failure handling → dead tasks never retried
- KIRA single point of failure → no supervisor above it
- Deep task dependencies → cascade failures
- Agents making assumptions about shared state → unreliable results
- No performance logging → impossible to optimize

## Verification
- [ ] All agents have declared owner and resource path in TOOLS.md
- [ ] Each director implements retry + fallback on subtask failure
- [ ] All agents have model tier, budget, and caller permissions defined
- [ ] KIRA dashboard metrics accessible at status endpoint
- [ ] Agent performance logs being written (Hermes integration)
- [ ] Fallback paths exercised in simulated failures
- [ ] No circular dependencies in agent call graph
