---
name: telegram-voice-tts
description: Add voice message reception and TTS voice reply capability to Telegram bot using espeak-ng and ffmpeg.
trigger: User asks to add voice/audio handling to Telegram bot, or TTS voice replies needed.
category: devops
---

# Telegram Voice + TTS Integration

Add voice message reception and TTS voice reply to the Telegram bot.

## Steps

1. Add imports: `subprocess, tempfile`
2. Add `send_voice()` method (send OGG via Telegram API)
3. Add `_generate_tts_ogg()` method (espeak-ng wav -> ffmpeg ogg opus)
4. Add `handle_voice_message()` method (generate TTS and send reply)
5. Detect `voice` in `process_message` and save to inbox
6. Trigger `handle_voice_message()` after inbox save, then `return`

## Key details
- espeak-ng: `-v de -s 130 --stdout` for German
- ffmpeg: `-c:a libopus -b:a 32k -ar 24000` for Telegram-compatible OGG
- Clean up temp wav/ogg files after sending
- Bot must be restarted after code changes

## Pitfalls
- TELEGRAM_ALLOWED_USERS must be in .env
- --user flag does not work for systemctl here (no user services)
- Kill old bot process before starting new one
