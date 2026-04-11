---
name: benos-agent-patterns
description: BEN//OS Agent Patterns. Implements 9 proven patterns: lane-based FIFO, heartbeat, context management, model routing, multi-agent protocols, cron isolation, sub-agent spawning, always-on, and anti-pattern avoidance. Use this skill when designing or modifying any agent workflow.
version: 1.0.0
author: Hermes Agent (from BEN//OS Wissensbasis)
license: MIT
metadata:
  hermes:
    tags: [BEN//OS, OpenClaw, Agent-Architecture, Patterns, FIFO, Lanes, Heartbeat]
    related_skills: [benos-cost-routing, benos-multi-agent-protocol, benos-kira-architecture]
    source: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/Good to know/
---

# BEN//OS Agent Patterns

## Trigger Conditions
- Designing a new agent or sub-agent
- Reconfiguring existing agent behavior
- Encountering blocking/queueing/concurrency issues
- Setting up cron jobs, heartbeats, or scheduled tasks
- Multi-agent coordination problems
- Agent crashes or failure to restart

## Pattern 1: Lane-Based FIFO Queuing

**Problem:** OpenClaw global lane limits sometimes fail (Bug #16055), causing agents to block each other.

**Solution:** Assign dedicated lanes per agent type.

```
Agent Type → Lane Name    | laneConcurrency
--------------------------------------------
Primary agents → agent-pri | 2
Research agents → res-*   | 4
Content agents → cnt-*    | 4
Automation → cron-jobs    | 2
Monitoring → heartbeat-*  | 2
```

**Implementation in OpenClaw config:**
```yaml
lanes:
  agent-pri:
    description: "Primary agent runs"
    concurrency: 2
  res-web:
    description: "Research agents"
    concurrency: 4
  cron:
    description: "Isolated cron jobs"
    concurrency: 2
```

**Action:** Audit agent configs → ensure each uses its own lane based on workload.

## Pattern 2: Heartbeat Optimization

**Do NOT use:** Heartbeats every 30 minutes with full context = $$$$$.

**Do use:**
```
Frequency: 6-hour minimum
Context: lightContext=true
Session: isolatedSession=true
Output: HEARTBEAT_OK only if nothing urgent
Alert: Telegram ONLY for critical items
```

**HEARTBEAT.md checklist:**
```
1. Check email from boss/important contacts only
2. Check calendar for events in next 2 hours
3. Verify active background jobs are still running
4. If all clear → respond "HEARTBEAT_OK"
5. If urgent → Telegram alert with summary
```

## Pattern 3: Context Management

**6 Cost Drivers:**
1. Context accumulation (40-50%)
2. Tool outputs (20-30%)
3. Systemprompt (10-15%)
4. Reasoning chains (10-15%)
5. Model selection (5-10%)
6. Heartbeat frequency (variable)

**Actions:**
- Run `/compact` immediately after task completion
- Use session-reset for completed workflows
- Move status-check jobs (with huge tool outputs) to isolated sessions
- Mask observations you don't need (observationMasking)
- Keep sessions under 50% window usage

## Pattern 4: Cron Job Isolation

**Problem:** Cron jobs running in main session = expensive extra rounds with full context.

**Solution:** Each cron job gets:
- `isolatedSession: true`
- `lightContext: true`
- Dedicated lane (cron-jobs)
- Cheapest viable model (S1/S2)

**Example:**
```yaml
cron:
  schedule: "0 7 * * 1-5"  # Weekdays 7am
  lane: cron-jobs
  model: S2
  isolatedSession: true
  lightContext: true
```

## Pattern 5: Sub-Agent Spawning

**When to spawn:** For tasks that are truly atomic and independent.

**Pattern:**
```
"Spawn a sub-agent to [specific task] 
and compile findings into [report type]"

Requirements:
- Sub-agent must have its own lane budget
- Parent must wait for completion result
- Parent sends Telegram notification on completion
- Sub-agent result structured as JSON
```

## Pattern 6: Always-On + Notification Routing

**Process monitoring:**
```
- Use systemd or pm2 for auto-restart
- On restart: send notification if downtime >5 minutes
- Service health check endpoint (if available)
```

**Notification priority:**
```
Critical  → Immediate Telegram
Important → Daily digest email
General   → Weekly digest email
```

## Pattern 7: Multi-Agent Protocol (schema-based)

**Every agent-to-agent message must include:**
```json
{
  "task_id": "uuid",
  "from_agent": "agent_name",
  "to_agent": "target_agent",
  "task_type": "research|write|analyze",
  "priority": "S1|S2|S3|S4|S5",
  "context": "minimal|full",
  "output_format": "structured_json",
  "deadline_seconds": 300
}
```

**Result format:** Agent MUST respond with designated output_format; no free text.

## Anti-Patterns (actions required)

| Anti-Pattern | Detection | Fix |
|-------------|-----------|-----|
| Expensive models for trivial tasks | Model tier > task level | Apply routing matrix, downgrade |
| Heartbeats with full context every 30min | `heartbeat interv < 3600` OR `!isolatedSession` | Set interv >=21600, enable isolatedSession |
| All tool outputs stored in context | Session size >50% window | Create separate debug session |
| No lane separation | All agents using default/main lane | Assign specific lane per agent type |
| Missing JSON schemas | Multi-agent interface not structured | Define input/output schemas |
| Cron jobs in main context | Cron config missing `isolatedSession` | Add isolatedSession: true |

## Pitfalls
- Forgetting lane separation → sub-agents queue up and block each other
- Running heartbeats too frequent → hundreds of $/month for nothing
- Using full context for cron → duplicate expense with no benefit
- Ambiguous agent messages → 79% of multi-agent failures
- No timeouts on sub-agent calls → permanent hangs
- Session never compacted → cost explosion over months

## Verification
- [ ] Each agent has dedicated lane (check OpenClaw config)
- [ ] All heartbeats: interv >=6h, isolatedSession, lightContext
- [ ] Sessions >50% window trigger /compact
- [ ] Cron jobs have isolatedSession=true
- [ ] All multi-agent messages follow JSON schema
- [ ] Systemprompts are minimal (under 500 tokens)
- [ ] Sub-agent tasks are atomic and have deadlines
