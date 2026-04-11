---
name: inbox-triage-3-systems
description: Ben's 3-tier inbox triage protocol for Telegram/Windows Smartphone inputs. Differentiates between ALARM (immediate fix), RESEARCH_PRE (pre-sorted, analyze), and RESEARCH_RAW (marked by prefix, store for later).
category: devops
---

# Ben's 3 Inbox Systems Triaging Protocol

Ben sends materials/notifications from his smartphone via Windows Smartphone link or Telegram. All inputs arrive in the inbox (e.g., `~/Desktop/Hermes-Inbox` or Telegram). These inputs must be classified into three systems immediately upon receipt.

## Classification Logic

Check the **Filename/Title** or **First Word/Number Marker** to classify:

### 1. System: ALARM / FEHLER (PRIORITY 1)
- **Indicators:** Title contains 'Fehler', 'Alarm', 'Report', 'Urgent', or similar critical terms.
- **Action:**
  - **IMMEDIATE:** Analyze and fix the reported issue.
  - **LOG:** Write a log entry of the issue and resolution.
  - **NOTIFY:** Send a Telegram confirmation to Ben.
  - **CLEANUP:** Delete the original message/file to keep inbox clean.

### 2. System: RESEARCH PREPARED (READY TO SORT)
- **Indicators:** Material is already titled, sorted, or clearly described by Ben before sending.
- **Action:**
  - **FULL ANALYSIS:** Extract all content (text, links followed to the end, voice transcribed, images analyzed).
  - **SORTING:** Place into the correct structured folder (e.g., `research/karpathy/`).
  - **WAIT:** Prepare a summary and wait for Ben in the chat. Ben will review the analysis and decide on integration when he is at his laptop.

### 3. System: RESEARCH RAW (UNSORTED)
- **Indicators:** File/message only has a simple prefix marker (e.g., `karpathy_sehr_wichtig`, `1_something`, etc.) but no clear description.
- **Action:**
  - **STORE:** Move immediately to `research_raw/` or a designated holding folder.
  - **LIGHT ANALYSIS:** Perform a quick gist extraction (what is this?) just so Ben knows what it is later.
  - **LOG:** Add to the "Later Review" list.
  - **WAIT:** Do not deeply analyze or integrate until Ben is home and ready to review jointly.

## Supported Data Types & Handling
- **Images/Screenshots:** Use vision tools to analyze content even if code/metadata is empty or corrupted.
- **Documents (PDF/DOCX):** Parse full text and follow all embedded/mentioned links to their end to extract info.
- **Voice Messages:** Open, transcribe (STT), and process content.
- **Links:** Follow redirect chains to the final destination and extract the core information.

## Workflow
1. Input received → Classify (Alarm/Prep/Raw).
2. Execute specific actions.
3. Confirm receipt via Telegram.
4. Prepare for Ben's review in chat (if Prep/Raw) or resolve (if Alarm).