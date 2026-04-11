---
name: telegram-vision-voice-bot
description: Complete Telegram bot implementation with Vision AI (SkillBoss), Voice TTS (espeak-ng+ffmpeg), and async background thread processing. Single-file bot for ~/.hermes/scripts/
version: 1.0.0
category: telegram
trigger: User wants Telegram bot with image recognition, voice replies, and robust async processing
---

# Telegram Bot: Vision + Voice + Async

Full implementation combining image analysis, voice message handling, and non-blocking async processing.

## What It Does
- Receives photos -> analyzes with SkillBoss Vision API (GPT-4o) -> sends German description via Telegram
- Receives voice notes -> replies with TTS voice generated via espeak-ng + ffmpeg
- All heavy work runs in background threads so polling never blocks
- Self-recovering: try/except wraps all API calls, timeouts set appropriately

## Complete Bot File (telegram_bot.py)

Save to ~/.hermes/scripts/telegram_bot.py

### Import Block
- subprocess, base64, urllib.request, threading
- requests, sqlite3, json, tempfile
- Path, datetime

### Constructor
Reads TELEGRAM_BOT_TOKEN and TELEGRAM_ALLOWED_USERS from ~/.hermes/.env
Initializes SQLite inbox table with columns: update_id, chat_id, message_id, text, has_media, media_path, received_at, processed

### Core Methods

1. get_updates(offset) -> list
   - GET /getUpdates with timeout=30, request timeout=35
   - Returns result array or empty on error

2. send_message(chat_id, text, parse_mode='Markdown')
   - POST /sendMessage with timeout=10
   - Returns True/False on success

3. download_media(file_id, file_type) -> path or None
   - Gets file path via /getFile, downloads to ~/.hermes/telegram_media/
   - Handles photo, voice, document types

4. send_voice(chat_id, audio_path, caption=None)
   - POST /sendVoice with OGG file upload
   - timeout=30

5. _generate_tts_ogg(text, lang='de') -> path
   - espeak-ng -v de -s 130 --stdout to WAV
   - ffmpeg -i wav -c:a libopus -b:a 32k -ar 24000 to OGG
   - Cleans up WAV, returns OGG path

6. _get_skillboss_key() -> string
   - Reads SKILLBOSS_API_KEY from .env
   - IMPORTANT: .env may have DUPLICATE entries with one empty. Filter carefully - skip empty/whitespace-only values

7. _analyze_image_with_vision(image_path, prompt) -> text
   - Base64 encode image
   - POST to https://api.heybossai.com/v1/chat/completions
   - Model: openai/gpt-4o, max_tokens=2000
   - 90s timeout (vision can be slow)
   - Returns description text or None

8. _process_photo_with_vision(chat_id, media_path)
   - Sends "🔍 Analysiere Bild..." immediately
   - Calls _analyze_image_with_vision()
   - Sends result (truncates >4000 chars) or error message

9. _process_message_async(chat_id, has_media, media_path, text)
   - Background thread target - NEVER call Vision/TTS in main loop
   - Routes to correct handler based on media type
   - Wraps everything in try/except

10. handle_voice_message(chat_id, voice_path, original_text)
    - Generates TTS response "Deine Sprachnachricht wurde empfangen. Hermes meldet sich."
    - Sends as voice note, cleans up temp files

## Async Processing Pattern (Critical)

```python
# NEVER block the poll loop with Vision/TTS calls
# ALWAYS use this pattern:
t = threading.Thread(target=self._process_message_async, 
                     args=(chat_id, has_media, media_path, text), 
                     daemon=True)
t.start()
```

## Critical Pitfalls

- **Duplicate .env entries**: SKILLBOSS_API_KEY may appear twice, once empty. Must filter: `if val and val not in ('""', "''", '')`
- **Main loop blocking**: Vision API takes 5-15s. NEVER call it from poll loop. Use threads.
- **Vision API endpoint**: Use /v1/chat/completions with image_url content type, NOT /v1/vision
- **Image format**: Support both PNG and JPEG. Telegram photos are JPEG, screenshots may be PNG
- **Memory management**: Thread objects accumulate. Prune finished threads periodically

## Startup Procedure

1. Syntax check: python3 -m py_compile ~/.hermes/scripts/telegram_bot.py
2. Kill old processes: pkill -f telegram_bot.py
3. Start: nohup python3 ~/.hermes/scripts/telegram_bot.py > /tmp/telegram_bot.log 2>&1 &
4. Verify: pgrep -f telegram_bot.py (should show PID)
5. Monitor logs: tail -f /tmp/telegram_bot.log

## Deployment Notes (April 2026)

Current Hermes setup runs the bot **manually**, not as a systemd user service. This means:
- No automatic restart on crash
- Bot must be started manually after reboot
- Health is monitored via `~/.hermes/.telegram_heartbeat` (written every 60s)
- `crash_watchdog` only monitors `hermes-gateway`, not this bot

**Recommended improvement**: Create a systemd user service for auto-restart:
```ini
# ~/.config/systemd/user/telegram-bot.service
[Unit]
Description=Hermes Telegram Bot
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/benlo/.hermes/scripts/telegram_bot.py
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```
Then: `systemctl --user enable --now telegram-bot`

Alternatively, extend `crash_watchdog` to also monitor the bot process.

## Recovery

If bot crashes or hangs:
1. Kill all bot processes and subprocess children
2. Check log for errors (tail /tmp/telegram_bot.log)
3. Fix issue, syntax check, restart
4. Send test message to verify getUpdates is working

## Test Sequence

Send these in order via Telegram:
1. Simple text -> should acknowledge
2. Photo -> should send "🔍 Analysiere Bild..." then description
3. Voice note -> should respond with voice TTS
4. /status -> system health
5. /help -> command list
