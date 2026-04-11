---
name: sop-inbox-processing
title: SOP Inbox Processing & File Handling
description: Defines how to handle incoming files in the Hermes Inbox. Standard operating procedure for rating, extracting, and archiving.
---

# Standard Operating Procedure: Inbox Processing

## Role Definition
Hermes acts as the **Command Center / Manager**, not a worker bee. Orchestrate tasks via sub-agents and maintain availability for Ben.

## Workflow
When the watchdog detects new files in the Inbox folder:

1. **Analyze Everything Completely** – Do NOT skip or mark as "blocked".
   - **Images (jpg/png)**: Use Vision (SkillBoss) to extract UI/layout or system evidence.
   - **PDFs**: Use `pdftotext` or equivalent tool to read text content.
   - DOCX: Extract XML from ZIP and pull `<w:t>` text.
   - **HTML/Code**: Parse and understand; categorize by size and purpose.
   - **TXT with Links**: Check if links are live/valuable if they appear relevant. Follow instructions if Ben gives explicit "check the link" command.

2. **Rate 1-10** (10 = Gold for System, 1 = Trash).
   - 10: System docs (OpenAI Abo, Configs), Live Evidence (running system screenshots), Core Code Baupläne.
   - 7-9: Useful secondary content (YT collections, reference materials).
   - 4-6: Decorative or duplicate variants.
   - 1-3: Useless (selfies, dead links, generic images without technical content).

3. **Implement Actions**:
   - Extract key knowledge and add to **Hermes Memory** or **Dashboard v3** as needed.
   - Move important raw files to `processed/` archive.
   - Delete trash immediately (no "maybe" pile).
   - Log every decision in `processing_log.json` with `file`, `rating`, `action`, `timestamp`.

4. **Present Summary to Ben**:
   - Show counts and examples of what was kept/deleted.
   - Offer to reconsider items if drift is high.

## Notes
- Ben may send files from smartphone; they go to `bensmartphone-inbox` (within Hermes-Inbox).
- PDFs are NOT blocked; always attempt text extraction.
- If image shows a person (selfie) with no technical context → 0/10 → delete.
- Live evidence screenshots of running processes are 10/10 but the jpg itself can be deleted after logging the insights.