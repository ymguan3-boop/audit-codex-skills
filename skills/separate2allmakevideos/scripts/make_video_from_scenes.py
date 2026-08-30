from __future__ import annotations

import asyncio
import json
import os
import pathlib
import re
import subprocess
from dataclasses import dataclass

try:
    import edge_tts
except ImportError:
    edge_tts = None

try:
    import imageio_ffmpeg
    FFMPEG = pathlib.Path(imageio_ffmpeg.get_ffmpeg_exe())
except ImportError:
    FFMPEG = pathlib.Path("ffmpeg")


ROOT = pathlib.Path.cwd()
BUILD = ROOT / "build_video"
VOICE_DIR = BUILD / "voice"
SCENE_DIR = BUILD / "scenes"
SUBTITLE_DIR = BUILD / "subtitles"
OUTPUT = ROOT / "complete_video.mp4"
SRT_OUTPUT = ROOT / "complete_video.srt"


@dataclass
class Cue:
    start: float
    end: float
    text: str


@dataclass
class Scene:
    index: int
    video: pathlib.Path
    narration: str
    center_title: str | None = None
    center_credit: str | None = None
    center_at_end: bool = False


# Customize this list for the user's project.
SCENES = [
    Scene(1, ROOT / "scene1.mp4", "Narration for scene 1.", "Center title", "Credit"),
    Scene(2, ROOT / "scene2.mp4", "Narration for scene 2."),
]

# Set to a user-uploaded music file, or None.
MUSIC_PATH: pathlib.Path | None = None


def run(cmd: list[str | os.PathLike[str]], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(
        [str(c) for c in cmd],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if cp.stdout:
        print(cp.stdout)
    if check and cp.returncode != 0:
        raise RuntimeError("command failed: " + " ".join(str(c) for c in cmd))
    return cp


def media_duration(path: pathlib.Path) -> float:
    cp = run([FFMPEG, "-hide_banner", "-i", path], check=False)
    match = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", cp.stdout)
    if not match:
        raise RuntimeError(f"cannot read duration for {path}")
    h, m, s = match.groups()
    return int(h) * 3600 + int(m) * 60 + float(s)


def ass_time(seconds: float) -> str:
    seconds = max(0, seconds)
    h = int(seconds // 3600)
    seconds -= h * 3600
    m = int(seconds // 60)
    seconds -= m * 60
    s = int(seconds)
    cs = int(round((seconds - s) * 100))
    if cs == 100:
        s += 1
        cs = 0
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def srt_time(seconds: float) -> str:
    total = int(round(max(0, seconds) * 1000))
    h, rem = divmod(total, 3_600_000)
    m, rem = divmod(rem, 60_000)
    s, ms = divmod(rem, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def ff_path(path: pathlib.Path) -> str:
    return path.resolve().as_posix().replace(":", r"\:")


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", r"\{").replace("}", r"\}")


def line_wrap(text: str, limit: int = 18) -> str:
    lines: list[str] = []
    current = ""
    for ch in text:
        current += ch
        if ch in "，、；。" or len(current) >= limit:
            lines.append(current)
            current = ""
    if current:
        lines.append(current)
    return r"\N".join(lines[:2])


def split_fallback(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"(?<=[，、；。.!?])", text) if p.strip()] or [text]


def make_fallback_audio(scene: Scene, duration: float) -> tuple[pathlib.Path, list[Cue], float]:
    """Silent placeholder when no TTS is available. Replace with OS TTS if desired."""
    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    out = VOICE_DIR / f"scene_{scene.index}_silent.wav"
    run([FFMPEG, "-y", "-f", "lavfi", "-i", f"anullsrc=r=48000:cl=mono", "-t", f"{duration:.3f}", out])
    parts = split_fallback(scene.narration)
    cues = [Cue(i * duration / len(parts), (i + 1) * duration / len(parts) - 0.1, p) for i, p in enumerate(parts)]
    return out, cues, 1.0


async def synthesize_scene(scene: Scene, duration: float, voice: str = "zh-TW-HsiaoChenNeural") -> tuple[pathlib.Path, list[Cue], float]:
    if edge_tts is None:
        return make_fallback_audio(scene, duration)

    VOICE_DIR.mkdir(parents=True, exist_ok=True)
    raw = VOICE_DIR / f"scene_{scene.index}_raw.mp3"
    fitted = VOICE_DIR / f"scene_{scene.index}_fit.wav"
    boundaries: list[dict] = []
    communicate = edge_tts.Communicate(scene.narration, voice, rate="+18%", pitch="+6Hz", boundary="WordBoundary")
    with raw.open("wb") as f:
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                f.write(chunk["data"])
            elif chunk["type"] == "WordBoundary":
                boundaries.append({"offset": chunk["offset"], "duration": chunk["duration"], "text": chunk["text"]})

    raw_duration = media_duration(raw)
    available = max(1.0, duration - 0.25)
    speed = max(1.0, raw_duration / available)
    run([FFMPEG, "-y", "-i", raw, "-af", f"atempo={min(speed, 2.0):.6f},apad,atrim=0:{duration:.3f},aresample=48000", "-ac", "1", fitted])

    if not boundaries:
        parts = split_fallback(scene.narration)
        cues = [Cue(i * available / len(parts), (i + 1) * available / len(parts), p) for i, p in enumerate(parts)]
    else:
        cues = []
        text = ""
        start = boundaries[0]["offset"] / 10_000_000
        end = start
        for msg in boundaries:
            piece = msg["text"].strip()
            msg_start = msg["offset"] / 10_000_000
            msg_end = (msg["offset"] + msg["duration"]) / 10_000_000
            if text and (len(text) + len(piece) > 18 or text.endswith(("，", "。", "；", "、"))):
                cues.append(Cue(start / speed + 0.1, min(duration - 0.1, end / speed + 0.1), text))
                start = msg_start
                text = piece
            else:
                text += piece
            end = msg_end
        if text:
            cues.append(Cue(start / speed + 0.1, min(duration - 0.1, end / speed + 0.1), text))
    return fitted, cues, speed


def write_ass(scene: Scene, cues: list[Cue], duration: float, path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    events = [
        f"Dialogue: 0,{ass_time(c.start)},{ass_time(c.end)},Subtitle,,0,0,0,,{ass_escape(line_wrap(c.text))}"
        for c in cues
    ]
    if scene.center_title:
        start = max(0.5, duration - 4.0) if scene.center_at_end else 1.0
        end = duration - 0.4 if scene.center_at_end else min(duration - 0.4, 5.0)
        events.append(f"Dialogue: 1,{ass_time(start)},{ass_time(end)},Title,,0,0,0,,{ass_escape(scene.center_title)}")
        if scene.center_credit:
            events.append(f"Dialogue: 1,{ass_time(start)},{ass_time(end)},Credit,,0,0,0,,{ass_escape(scene.center_credit)}")

    content = """[Script Info]
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
PlayResX: 1920
PlayResY: 1080

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Subtitle,Microsoft JhengHei,46,&H00FFFFFF,&H000000FF,&HB0000000,&H90000000,0,0,0,0,100,100,0,0,1,4,1,2,170,170,58,1
Style: Title,Microsoft JhengHei,72,&H00FFFFFF,&H000000FF,&HBA000000,&HA0000000,-1,0,0,0,100,100,0,0,1,4,1,5,160,160,42,1
Style: Credit,Microsoft JhengHei,50,&H00FFFFFF,&H000000FF,&HBA000000,&HA0000000,-1,0,0,0,100,100,0,0,1,4,1,5,160,160,155,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    path.write_text(content + "\n".join(events) + "\n", encoding="utf-8-sig")


def render_scene(scene: Scene, audio: pathlib.Path, cues: list[Cue], duration: float) -> pathlib.Path:
    out = SCENE_DIR / f"scene_{scene.index}.mp4"
    ass = SUBTITLE_DIR / f"scene_{scene.index}.ass"
    SCENE_DIR.mkdir(parents=True, exist_ok=True)
    write_ass(scene, cues, duration, ass)
    vf = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=30," + f"subtitles='{ff_path(ass)}'"
    run([FFMPEG, "-y", "-i", scene.video, "-i", audio, "-filter_complex", f"[0:v]{vf}[v];[1:a]aresample=48000[a]", "-map", "[v]", "-map", "[a]", "-t", f"{duration:.3f}", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", out])
    return out


def write_srt(all_cues: list[list[Cue]], durations: list[float], transition: float = 0.55) -> None:
    cursor = 0.0
    idx = 1
    rows = []
    for cues, duration in zip(all_cues, durations):
        for cue in cues:
            rows.append(f"{idx}\n{srt_time(cursor + cue.start)} --> {srt_time(cursor + cue.end)}\n{cue.text}\n")
            idx += 1
        cursor += duration - transition
    SRT_OUTPUT.write_text("\n".join(rows), encoding="utf-8-sig")


def concat_and_mix(paths: list[pathlib.Path], durations: list[float], transition: float = 0.55) -> None:
    inputs: list[str | os.PathLike[str]] = []
    for p in paths:
        inputs.extend(["-i", p])
    effects = ["fade", "smoothleft", "wipeleft", "circleopen", "fadeblack", "smoothright"]
    parts = []
    cv, ca = "[0:v]", "[0:a]"
    offset = durations[0] - transition
    for i in range(1, len(paths)):
        nv, na = f"[v{i}]", f"[a{i}]"
        parts.append(f"{cv}[{i}:v]xfade=transition={effects[(i-1)%len(effects)]}:duration={transition}:offset={offset:.3f}{nv}")
        parts.append(f"{ca}[{i}:a]acrossfade=d={transition}{na}")
        cv, ca = nv, na
        offset += durations[i] - transition
    merged = BUILD / "merged.mp4"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(parts), "-map", cv, "-map", ca, "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", merged])

    if MUSIC_PATH and MUSIC_PATH.exists():
        mixed = BUILD / "mixed.mp4"
        total = media_duration(merged)
        run([FFMPEG, "-y", "-i", merged, "-stream_loop", "-1", "-i", MUSIC_PATH, "-filter_complex", f"[0:a]volume=3.0,alimiter=limit=0.92[voice];[1:a]volume=0.4,afade=t=in:st=0:d=1,afade=t=out:st={max(0,total-2):.3f}:d=2[music];[voice][music]amix=inputs=2:duration=first:normalize=0,alimiter=limit=0.98[a]", "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", mixed])
    else:
        mixed = merged
    run([FFMPEG, "-y", "-i", mixed, "-i", SRT_OUTPUT, "-map", "0:v", "-map", "0:a", "-map", "1:0", "-c:v", "copy", "-c:a", "copy", "-c:s", "mov_text", "-metadata:s:s:0", "language=chi", OUTPUT])


async def main() -> None:
    BUILD.mkdir(exist_ok=True)
    paths, durations, all_cues = [], [], []
    for scene in SCENES:
        duration = media_duration(scene.video)
        audio, cues, _ = await synthesize_scene(scene, duration)
        paths.append(render_scene(scene, audio, cues, duration))
        durations.append(duration)
        all_cues.append(cues)
    write_srt(all_cues, durations)
    concat_and_mix(paths, durations)
    print(f"Output: {OUTPUT}")
    print(f"SRT: {SRT_OUTPUT}")


if __name__ == "__main__":
    asyncio.run(main())
