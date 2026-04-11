---
name: benos-multi-agent-protocol
description: BEN//OS Multi-Agent Communication Protocol. Defines the schema-based communication between agents, failure modes, and the 80% spec-problem fix. Use this skill when agents need to exchange tasks, results, or coordinate.
version: 1.0.0
author: Hermes Agent (from BEN//OS Wissensbasis)
license: MIT
metadata:
  hermes:
    tags: [BEN//OS, Multi-Agent, Protocol, JSON-Schema, Task-Delegation, Communication]
    related_skills: [benos-agent-patterns, benos-kira-architecture, benos-cost-routing]
    source: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/Good to know/
---

# BEN//OS Multi-Agent Protocol

## Trigger Conditions
- Dispatching a task to another agent (research, write, analyze, etc.)
- Setting up agent-to-agent communication for the first time
- Debugging failed multi-agent workflows (silent failures, wrong outputs)
- Adding a new agent to the KIRA architecture
- Creating or modifying delegation workflows

## Core Principle: 79% of Multi-Agent Failures Are SPEC Problems

Only 16% of failures are infrastructure. Everything else is caused by:
- Ambiguous task descriptions
- Missing output format specifications
- No timeout/deadline defined
- Unclear roles/responsibilities
- Shared resources without explicit ownership

**Solution:** Strict JSON schemas for ALL agent communications.

## Step 1: Task Submission Schema

When delegating a task, format the message as:
```json
{
  "task_id": "REPLACE_WITH_UUID",
  "from_agent": "YOUR_AGENT_NAME",
  "to_agent": "TARGET_AGENT_NAME",
  "task_type": "research|write|analyze|code|monitor|report",
  "priority": "S1|S2|S3|S4|S5",
  "context": "minimal_only_what_subagent_needs",
  "task_description": "Single clear sentence. No ambiguity.",
  "input_data": { "relevant": "key-value pairs only" },
  "output_format": "json|markdown|structured_text",
  "output_schema": {
    "summary": "max 3 sentences",
    "key_findings": ["array of strings"],
    "sources": ["url1", "url2"],
    "confidence": "0.0 to 1.0",
    "next_steps": ["array of strings"]
  },
  "deadline_seconds": 300,
  "fallback": "Return PARTIAL if deadline reached; do not hallucinate"
}
```

## Step 2: Expected Response Schema

Agent responses must follow the output_schema defined in the task:
```json
{
  "task_id": "SAME_AS_INPUT",
  "status": "complete|partial|failed",
  "result": {
    "summary": "...",
    "key_findings": ["..."],
    "sources": ["..."],
    "confidence": 0.85,
    "next_steps": ["..."]
  },
  "error": null,
  "elapsed_seconds": 142,
  "token_cost_estimate": { "input_tokens": 1200, "output_tokens": 800 }
}
```

## Step 3: Agent Role Assignment

Each agent needs clear boundaries:
```
Research Director → Intel Agents (Web, YouTube, Reddit, GitHub, X)
Content Director  → Writer, Script, Distribution Agents
Trading Director  → Market Analysis, Backtest, Signal Agents
CTO Agent         → Cost Monitor, Model Router
```

**Rules:**
- No shared resources without explicit ownership
- Each sub-agent writes to its own output directory
- Agents NEVER bypass their director to talk to other directors
- Results always escalate back through hierarchy

## Step 4: Communication Flow

```
1. Director receives high-level request
2. Director breaks into atomic tasks
3. Director assigns each task via Task Submission Schema
4. Director waits for response (with timeout)
5. On timeout → retry once → if still failed → report partial
6. Director merges results → creates summary
7. Director reports results up the chain (or to user)
```

## Step 5: Failure Handling

```
| Failure Type          | Detection                    | Action                                |
|-----------------------|------------------------------|---------------------------------------|
| Timeout               | deadline_seconds exceeded    | Retry once, then return partial       |
| Wrong output format   | Schema validation fails      | Request clarification, max 2 retries  |
| Silent failure        | No response received         | Escalate immediately to director      |
| Hallucinated data     | No sources provided          | Flag as unverified, mark confidence=0 |
| Resource conflict     | File/lock already exists     | Wait with timeout, then fail cleanly  |
```

## Step 6: Multi-Agent Best Practices

- Keep context minimal: only what the receiving agent actually needs
- Atomic tasks: one task per message, never batch unrelated tasks
- Explicit schemas: both request AND response must follow defined format
- Reasonable deadlines: 5min for simple research, 30min for complex analysis
- Token budget: set per-agent token limits to prevent runaway costs
- MCP protocol: use Model Context Protocol for external tool integration
- No implicit state: agents must NOT assume previous task knowledge

## Pitfalls
- Vague task descriptions → wrong results, wasted money
- Missing output format → unusable results requiring rework
- No timeouts → agents hang indefinitely, blocking other tasks
- Shared file paths without locking → race conditions and data corruption
- Combining multiple tasks in one message → confused sub-agents
- Passing full context to sub-agents → costs multiply per sub-agent
- No fallback strategy → task dead-ends silently

## Verification
- [ ] Every task submission includes valid JSON schema
- [ ] Output format explicitly defined for every request
- [ ] Deadline set and documented for each task
- [ ] Fallback strategy defined for each delegation
- [ ] No shared resources without explicit ownership
- [ ] Response parsed and validated against expected schema
- [ ] Failed tasks retry at most twice before escalation
