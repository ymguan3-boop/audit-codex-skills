---
name: separate2allmakevideos
description: Use when the user wants to turn multiple segmented video clips into one complete narrated video, with per-scene narration, optional center-screen text overlays, generated SRT subtitles, optional background music and volume balancing, review iterations, and YouTube-ready description and tags.
---

# separate2allmakevideos

## Overview

Use this skill to produce a complete publish-ready video from multiple scene clips. The workflow covers collecting scene metadata, generating lively narration, timing subtitles to speech, adding center-screen text, mixing background music below narration, exporting the final MP4, and drafting YouTube metadata.

## Required Workflow

1. Inventory the user's inputs:
   - Segmented video clips, in intended order.
   - Per-scene narration text.
   - Per-scene center-screen text, if any. Center-screen text is not narration unless the user explicitly says so.
   - Background music choice: no music, generated/simple music, or user-uploaded audio file.
   - Desired output filename, resolution, language, and voice style if specified.

2. Clarify only missing essentials:
   - Ask for missing clip order, missing narration, or whether center-screen text should be spoken only when it cannot be reasonably inferred.
   - Default to preserving each source clip once. Do not loop or duplicate clips unless the user asks.

3. Generate narration:
   - Prefer a natural neural voice if available, such as `edge-tts` with a matching locale voice.
   - Use the OS voice only as a fallback.
   - Fit narration to each scene by adjusting speech rate or FFmpeg `atempo`; do not extend or repeat the scene just to fit narration.
   - Keep center-screen text out of narration unless explicitly included in the narration field.

4. Create timed subtitles:
   - Use TTS word or sentence boundary timestamps when available.
   - Split subtitle cues into short readable phrases, generally 10-22 CJK characters per cue.
   - Apply the same time compression factor used for the audio.
   - Burn subtitles into the video for compatibility and also export a `.srt` file.
   - Keep subtitle margins inside the safe area; use readable font size and wrapping so text does not exceed screen bounds.

5. Add center-screen overlays:
   - Treat them as visual titles, not subtitles.
   - Use separate text layers when different lines need different sizes, for example title on top and producer credit smaller below.
   - Avoid escaping mistakes in ASS subtitles: a literal ASS line break is `\N`; do not render `/` or `\` visibly.

6. Combine scenes:
   - Normalize each scene to a consistent resolution and frame rate.
   - Use tasteful transitions such as fade, smooth wipe, circle open, or fade black.
   - Crossfade audio across transitions.
   - Final duration should roughly equal sum of source scene durations minus transition overlaps.

7. Mix audio:
   - Narration must be clearly louder than background music.
   - When using FFmpeg `amix`, set `normalize=0` if manual volume balancing is intended.
   - A good starting mix is voice `volume=2.5-3.5`, music `volume=0.25-0.55`, then `alimiter`.
   - If the user says narration is too quiet or music is inaudible, redo only the final mix when possible.

8. Validate:
   - Check final duration, stream info, subtitle stream, and output file size.
   - Extract preview frames from opening title, subtitle-heavy scenes, and ending title.
   - Verify clips are not duplicated, subtitles stay in bounds, center text appears correctly, and music/voice balance matches the user's request.

9. Deliver:
   - Provide direct links to the final MP4 and SRT.
   - Mention duration, resolution, audio/subtitle streams, and any limitations.
   - If asked, create YouTube description and tags.

## Script Starting Point

Use `scripts/make_video_from_scenes.py` as a starting point for repeatable local projects. Copy or adapt it into the working folder, then customize the `SCENES` list, output names, voice, and music path.

The script expects:
- FFmpeg available directly or through `imageio-ffmpeg`.
- Optional `edge-tts` for neural narration.
- One narration entry per scene.
- Optional `center_title` and `center_credit` fields per scene.

Install dependencies if needed:

```powershell
python -m pip install --user imageio-ffmpeg edge-tts
```

## YouTube Metadata

When the user asks for a YouTube description:

- Start with the video's core public value in 1-2 sentences.
- Summarize the story or process in short paragraphs.
- Include creator/organization credits if appropriate.
- Avoid exaggerated claims not shown in the video.
- Keep it easy to paste into YouTube.

When the user asks for tags:

- Provide comma-separated tags.
- Include topic, location, organization, method/technology, problem domain, outcome, and creator name when relevant.
- Use natural search phrases, not only hashtags.

## Common Pitfalls

- Do not include "center-screen text" in narration unless explicitly requested.
- Do not loop source clips by default.
- Do not make one long subtitle per scene.
- Do not let background music overpower narration.
- Do not rely on command-line inline Chinese paths if the shell mangles encoding; find files by globbing or write UTF-8 scripts.
