---
name: benos-workflow-prompts
description: BEN//OS Prompt Templates & Workflow Patterns. Ready-to-use prompts for setup, cron jobs, business automation, content creation, development workflows, security checks, and systemprompts for KIRA and research agents. Copy-paste these directly when building new workflows.
version: 1.0.0
author: Hermes Agent (from BEN//OS Wissensbasis)
license: MIT
metadata:
  hermes:
    tags: [BEN//OS, Prompts, Workflows, Templates, Cron, Automation, Sub-Agent, Setup]
    related_skills: [benos-agent-patterns, benos-cost-routing, benos-kira-architecture]
    source: /mnt/c/Users/benlo/Desktop/Hermes-Inbox/Good to know/
---

# BEN//OS Workflow Prompts

## Trigger Conditions
- Building a new OpenClaw cron job or heartbeat
- Spawning a sub-agent for research or content tasks
- Setting up integrations (Gmail, Asana, GitHub)
- Creating a new agent and need systemprompt
- Generating a morning briefing or weekly review
- Content pipeline or competitor tracking setup
- Developing mobile coding workflows
- Accounting automation tasks
- Security configuration verification

## Setup & Integration Prompts

**Gmail Integration:**
```
"Help me set up Gmail integration. I want to connect my email account [email]"
→ OpenClaw will guide through OAuth
```

**Add API Token:**
```
"Add my [SERVICE] Personal Access Token to the .env file"
→ Prompts for token, writes to ~/.hermes/.env securely
```

**Install Skill:**
```
"Install the [skill-name] skill"
→ Queries ClawHub, installs if available
```

**Check/Install:**
```
"Check if I have the [skill] installed. If not, install it"
```

**TOOLS.md Management:**
```
"Add my Asana workspace details to TOOLS.md. 
Workspace: '[name]' with ID [id]. Projects: [Project1], [Project2]"

"Add my morning briefing preferences to TOOLS.md: 
location [city], trending topics in [topics]"

"Save this as my style guide to ~/clawd/reference/brand-voice.md: [content]"
```

**Status Monitoring:**
```
"Show me all my active background jobs"
"What's the status of [job-name]?"
"openclaw /status" → shows active sessions
```

## Cron Job Prompts

**Morning Briefing (basis automation ★):**
```
Create a cron job that runs every weekday at 7am.
It should check my email, pull my calendar events for today,
and send me a morning briefing via Telegram.
```

**Enhanced Morning Briefing:**
```
Create a skill called 'morning-briefing' that generates a daily summary with:
- weather for [city]
- my calendar events for today and tomorrow
- any urgent emails from the last 12 hours
- top 3 trending topics in AI and tech
```

**Weekly Review (cron):**
```
Every Friday at 5pm, create my weekly review. Pull from:
- my Notion pages tagged 'meeting notes'
- Slack threads I participated in
- and GitHub PRs I merged this week.
Summarize: key decisions made, action items for next week,
project status updates, blockers. Send via email.
```

**Competitor Tracking (YouTube):**
```
Every Monday, analyze my competitor channels and send me a summary:
how many videos they uploaded this week, what topics they covered,
and which videos performed best.
```

**Cost Monitoring:**
```
"Create a weekly cron job that checks my monthly token spend.
If over 50% budget used, send Telegram alert.
If over 80%, escalate to critical."
```

## Sub-Agent Spawning Prompts

**Generic Research:**
```
"Spawn a sub-agent to research our top 5 competitors 
and compile detailed findings into a report"
```

**Market Research:**
```
"Research the market for '[TOPIC]'. Find competitors, analyze their pricing 
models, identify market gaps, and compile everything into a markdown report. 
Save to ~/clawd/research/[name].md"
```

**Content Idea Pipeline:**
```
"Monitor our Slack channel #content-ideas. Whenever someone says 
'potential video idea', extract the topic, search X/Twitter for related 
discussions, collect the top 10 relevant tweets, and create an Asana card 
in my Video Pipeline project with a summary, the tweets, and a suggested outline"
```

**Auto-Fix Workflow:**
```
"Every hour, check the metrics at [url]. If the bounce rate is over 50%, 
create a GitHub issue labeled 'auto-fix'"

"Create a skill that watches for GitHub issues labeled 'auto-fix'. 
When you see one: analyze the issue, spawn a coding agent to implement 
a fix, create a PR, run tests, and if tests pass, merge and deploy. 
Then notify the team in Slack"
```

**Mobile Coding Workflow:**
```
[From Telegram on mobile:]
"Build a login form component with email and password validation. 
Use React and Tailwind CSS"

"Show me the code you wrote"
"Run the tests"
"If everything looks good, commit this to GitHub and deploy to production"
```

## Business & Automation Prompts

**Goal Tracking:**
```
"Add to TOOLS.md that my business goal is [GOAL] within [TIMEFRAME]. 
Break this down into quarterly milestones."

"Create a weekly review where you check progress on all my business goals, 
identify blockers, and suggest next steps"
```

**Notification Routing:**
```
"For notifications: critical issues send to Telegram immediately, 
important stuff goes in a daily summary, 
general info goes in a weekly digest"
```

**Task Completion Alerts:**
```
"Whenever a sub-agent completes a task, send me a notification via 
Telegram with a summary"
```

## Brand & Content Prompts

**Brand Voice Analysis:**
```
"Analyze these writing samples and extract my writing style. 
Create a style guide covering: tone, vocabulary, sentence structure, 
and common phrases"
```
→ Save to ~/clawd/reference/brand-voice.md

## Security Prompts

**Security Check (run monthly):**
```
"Check my config file. Make sure OpenClaw is only listening on 
localhost (127.0.0.1), not exposed to the internet"

"Check the permissions on my .env file. 
It should only be readable by me (600)"

"Enable authentication on the gateway. 
Generate a secure random token and add it to the config"
```

## Systemprompts (for Agent Creation)

**KIRA CEO Agent:**
```
Du bist KIRA, der zentrale orchestrierende Agent von BEN//OS.

DEINE AUFGABE:
- Koordination aller Sub-Agents
- Kostenoptimierung: Erste Frage bei jeder Aufgabe: Kann S1 das lösen?
- Tägliches Reporting an Ben via Telegram
- Eskalation kritischer Probleme sofort

MODELL-ROUTING:
- S1 (kostenlos): Status-Checks, HEARTBEAT_OK, triviale Antworten
- S2 (günstig): Einfache Zusammenfassungen, Datenextraktion
- S3 (mittel): Recherche, strukturierte Analyse
- S4 (Sonnet): Code, Reasoning, Entscheidungen
- S5 (Opus, NUR mit manueller Ben-Freigabe): Kritisches

KOMMUNIKATION:
- Output immer als JSON-Schema wenn an andere Agents
- Alle Ergebnisse via Telegram an Ben
- Fehler sofort eskalieren, nicht still ignorieren
```

**Research Agent:**
```
Du bist ein spezialisierter Research-Agent.

AUFGABE: [spezifisch]
INPUT-FORMAT: { "topic": "", "depth": "basic|deep", "sources": [] }
OUTPUT-FORMAT:
{
  "summary": "max 3 Sätze",
  "key_findings": ["finding1", "finding2"],
  "sources": ["url1", "url2"],
  "confidence": 0.0-1.0,
  "next_steps": ["action1"]
}

REGELN:
- Nur verifizierte Informationen
- Keine Halluzinationen — lieber "unbekannt" als falsch
- Token-effizient arbeiten
```

**Content Writer Agent:**
```
Du bist ein professioneller Content-Writer für [TOPIC/BRAND].

STIL: Extract brand voice from ~/clawd/reference/brand-voice.md

OUTPUT-FORMAT:
{
  "title": "...",
  "excerpt": "max 160 chars",
  "content": "markdown with headings",
  "tags": ["tag1", "tag2"],
  "word_count_estimate": 1200,
  "target_audience": "..."
}

REGELN:
- Follow brand tone guidelines (reference file)
- Include at least 3 actionable insights
- No fluff — value per word ratio > 1.0
- Use markdown structure: H2, H3, lists, emphasis
```

**Cost Monitor Agent:**
```
Du bist der CTO Cost Monitor für BEN//OS.

TÄGLICHE AUFGABEN:
1. Check token usage for all agents
2. Compare against monthly budgets
3. Identify agents with >80% of budget used
4. Generate Telegram alert if any agent exceeds 50% budget

WEEKLY SUMMARIZE:
- Total spend by agent (ranking)
- Abnormal usage patterns
- Recommendations: reduce expensive model calls, lower agent frequency
```

## Heartbeat Templates

**Minimalistic (Optimized):**
```
Run every 6 hours:
1. Check email from boss/important contacts only
2. Check calendar for events in next 2 hours
3. Verify active background jobs still running
4. If all clear → respond "HEARTBEAT_OK"
5. If urgent → Telegram alert with summary

Settings:
- model: S1 (free)
- isolatedSession: true
- lightContext: true
- prompt-size: <200 tokens
```

## Pitfalls
- Heartbeat every 30min with full context = $100s/month
- Tool output in main session context → context explosion
- Multi-task prompts → confuse agents, lower quality
- Missing output format → unusable results
- API keys in .env without 600 permissions → security risk
- Defaulting to S4/S5 → 5-25x cost inflation
- No fallback → failed tasks block pipeline

## Verification
Prompt checks before execution:
- [ ] Complexity assessed → correct model tier (S1-S5) chosen
- [ ] `/compact` will be called after task completion
- [ ] Sub-agent tasks are atomic and self-contained
- [ ] All external integrations have tokens in .env, permissions 600
- [ ] Output format explicitly defined
- [ ] Deadlines reasonable for task complexity
- [ ] Fallback strategy specified
- [ ] Notification routing configured (Telegram/daily/weekly)
