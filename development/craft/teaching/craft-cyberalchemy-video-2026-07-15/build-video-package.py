#!/usr/bin/env python3

import json
import re
from pathlib import Path

import yaml


PACKAGE = Path(__file__).resolve().parent
SHOT_LIST = PACKAGE / "SHOT-LIST.yml"
SOURCE_TRACE = PACKAGE / "SOURCE-TRACE.md"
TEMPLATE = PACKAGE / "review.template.html"


def words(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def timecode(seconds: int) -> str:
    return f"{seconds // 60:02d}:{seconds % 60:02d}"


def write(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n")


def validate(data: dict) -> tuple[int, int]:
    package = data["package"]
    segments = data["segments"]
    required = {
        "segment_id",
        "act_id",
        "title",
        "duration_seconds",
        "generation_clip_seconds",
        "story_job",
        "concepts",
        "prior_model",
        "voice_copy",
        "written_copy",
        "visual_mode",
        "visual_prompt",
        "negative_prompt",
        "continuity_assets",
        "camera_and_motion",
        "sound_direction",
        "transition_in",
        "transition_out",
        "source_refs",
        "claim_posture",
        "editor_notes",
    }
    expected_ids = [f"VID-CAM-{index:03d}" for index in range(1, 23)]
    actual_ids = [segment["segment_id"] for segment in segments]
    if actual_ids != expected_ids:
        raise RuntimeError(f"Unexpected segment sequence: {actual_ids}")

    known_assets = set(data["assets"])
    trace_text = SOURCE_TRACE.read_text()
    known_refs = set(re.findall(r"^\| ((?:SRC|CLM)-[A-Z0-9-]+) \|", trace_text, re.MULTILINE))

    for segment in segments:
        missing = required - set(segment)
        if missing:
            raise RuntimeError(f"{segment['segment_id']} missing {sorted(missing)}")
        unknown_assets = set(segment["continuity_assets"]) - known_assets
        if unknown_assets:
            raise RuntimeError(f"{segment['segment_id']} unknown assets {sorted(unknown_assets)}")
        unknown_refs = set(segment["source_refs"]) - known_refs
        if unknown_refs:
            raise RuntimeError(f"{segment['segment_id']} unknown sources {sorted(unknown_refs)}")
        if not segment["written_copy"]:
            raise RuntimeError(f"{segment['segment_id']} has no written copy")
        if "previous scene" in segment["visual_prompt"].lower():
            raise RuntimeError(f"{segment['segment_id']} has a context-dependent prompt")
        segment_wpm = words(segment["voice_copy"]) * 60 / segment["duration_seconds"]
        if segment_wpm > 150:
            raise RuntimeError(f"{segment['segment_id']} pacing is too fast at {segment_wpm:.1f} wpm")

    runtime = sum(segment["duration_seconds"] for segment in segments)
    voice_words = sum(words(segment["voice_copy"]) for segment in segments)
    if runtime != package["runtime_target_seconds"]:
        raise RuntimeError(f"Runtime {runtime} does not match target")
    target = package["voice_target_words"]
    if not target["min"] <= voice_words <= target["max"]:
        raise RuntimeError(f"Voice word count {voice_words} is outside target {target}")
    if package["human_gate"]["status"] != "approved":
        raise RuntimeError("Human voice gate is not approved")
    return runtime, voice_words


def build_voice_script(data: dict, runtime: int, voice_words: int) -> str:
    lines = [
        "# Full Voice Script",
        "",
        f"Title: {data['package']['title']}",
        f"Subtitle: {data['package']['subtitle']}",
        f"Runtime target: {timecode(runtime)}",
        f"Voice word count: {voice_words}",
        "Status: full draft, operator-approved voice",
        "Source of truth: `SHOT-LIST.yml`",
        "",
    ]
    for segment in data["segments"]:
        lines.extend(
            [
                f"## {segment['segment_id']} - {segment['title']}",
                "",
                f"Act: `{segment['act_id']}`<br>",
                f"Target duration: `{segment['duration_seconds']}s`<br>",
                f"Concepts: {', '.join(segment['concepts'])}<br>",
                f"Sources: {', '.join(segment['source_refs'])}",
                "",
                segment["voice_copy"],
                "",
            ]
        )
    return "\n".join(lines)


def build_voice_model_input(data: dict) -> str:
    profile = data["voice_profile"]
    lines = [
        "# Voice Model Input",
        "",
        f"Delivery: {profile['delivery']}",
        f"Pace: approximately {profile['pace_words_per_minute']} words per minute",
        f"Pause policy: {profile['pause_policy']}",
        "Pronunciation:",
    ]
    for term, pronunciation in profile["pronunciation"].items():
        lines.append(f"- {term}: {pronunciation}")
    for segment in data["segments"]:
        lines.extend(
            [
                "",
                f"## {segment['segment_id']}",
                "",
                segment["voice_copy"],
            ]
        )
    return "\n".join(lines)


def build_written_copy(data: dict) -> str:
    lines = [
        "# On-Screen Written Copy",
        "",
        "Source of truth: `SHOT-LIST.yml`",
        "",
        "Exact typography is added in editorial. Visual models must not render this copy.",
        "",
    ]
    for segment in data["segments"]:
        lines.extend([f"## {segment['segment_id']} - {segment['title']}", ""])
        for item in segment["written_copy"]:
            lines.extend(
                [
                    f"### {item['role']}",
                    "",
                    item["text"],
                    "",
                    f"Position: `{item['position']}`<br>",
                    f"Display: `{item['display_seconds']}s`",
                    "",
                ]
            )
    return "\n".join(lines)


def build_visual_prompts(data: dict) -> str:
    projection = {
        "prompt_schema_version": "1.0",
        "package_id": data["package"]["package_id"],
        "aspect_ratio": data["package"]["aspect_ratio"],
        "editorial_text_policy": "Generate no precise typography; add written_copy during editing.",
        "assets": data["assets"],
        "prompts": [],
    }
    for segment in data["segments"]:
        projection["prompts"].append(
            {
                "segment_id": segment["segment_id"],
                "title": segment["title"],
                "visual_mode": segment["visual_mode"],
                "timeline_duration_seconds": segment["duration_seconds"],
                "generation_clip_seconds": segment["generation_clip_seconds"],
                "continuity_assets": segment["continuity_assets"],
                "prompt": segment["visual_prompt"],
                "negative_prompt": segment["negative_prompt"],
                "camera_and_motion": segment["camera_and_motion"],
                "transition_in": segment["transition_in"],
                "transition_out": segment["transition_out"],
            }
        )
    return yaml.safe_dump(projection, sort_keys=False, allow_unicode=False, width=100)


def build_edl(data: dict) -> str:
    lines = [
        "# Edit Decision List",
        "",
        "Source of truth: `SHOT-LIST.yml`",
        "",
        "Use two-second handles on generated media where the model allows it. Timeline",
        "duration can exceed generation-clip duration through editorial crops, holds,",
        "motion-graphic builds, or matched detail inserts named in `editor_notes`.",
        "",
        "| In | Out | Segment | Act | Voice words | Generated clip | Visual mode |",
        "| ---: | ---: | --- | --- | ---: | ---: | --- |",
    ]
    cursor = 0
    for segment in data["segments"]:
        end = cursor + segment["duration_seconds"]
        lines.append(
            "| "
            + " | ".join(
                [
                    timecode(cursor),
                    timecode(end),
                    segment["segment_id"],
                    segment["act_id"],
                    str(words(segment["voice_copy"])),
                    f"{segment['generation_clip_seconds']}s",
                    segment["visual_mode"],
                ]
            )
            + " |"
        )
        cursor = end

    for segment in data["segments"]:
        lines.extend(
            [
                "",
                f"## {segment['segment_id']} - {segment['title']}",
                "",
                f"- Transition in: {segment['transition_in']}",
                f"- Transition out: {segment['transition_out']}",
                f"- Sound: {segment['sound_direction']}",
                f"- Editorial assembly: {segment['editor_notes']}",
            ]
        )
    return "\n".join(lines)


def build_review(data: dict, runtime: int, voice_words: int) -> str:
    review_data = {
        "review_id": f"{data['package']['package_id']}-full-draft",
        "package": data["package"],
        "runtime": runtime,
        "voice_words": voice_words,
        "assets": data["assets"],
        "acts": data["acts"],
        "segments": data["segments"],
    }
    encoded = json.dumps(review_data, ensure_ascii=True).replace("<", "\\u003c")
    return TEMPLATE.read_text().replace("__VIDEO_DATA__", encoded)


def main() -> None:
    data = yaml.safe_load(SHOT_LIST.read_text())
    runtime, voice_words = validate(data)

    outputs = {
        "FULL-VOICE-SCRIPT.md": build_voice_script(data, runtime, voice_words),
        "VOICE-MODEL-INPUT.md": build_voice_model_input(data),
        "ON-SCREEN-WRITTEN-COPY.md": build_written_copy(data),
        "VISUAL-MODEL-PROMPTS.yml": build_visual_prompts(data),
        "EDIT-DECISION-LIST.md": build_edl(data),
        "review.html": build_review(data, runtime, voice_words),
    }
    for name, content in outputs.items():
        write(PACKAGE / name, content)

    print(f"PASS: generated {len(outputs)} artifacts")
    print(f"SEGMENTS: {len(data['segments'])}")
    print(f"RUNTIME: {timecode(runtime)}")
    print(f"VOICE WORDS: {voice_words}")


if __name__ == "__main__":
    main()
