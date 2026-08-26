#!/usr/bin/env python3
"""Persist a staged draft bundle, update its resolver index, and validate it."""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import shutil
import stat
import subprocess
import sys
import time
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


DIAGRAM_ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]*$")
REVISION_PATTERN = re.compile(r"^r[0-9]{4}$")


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path}: top level must be a mapping")
    return value


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def path_lexists(path: Path) -> bool:
    return os.path.lexists(path)


def is_reparse_or_link(path: Path) -> bool:
    metadata = os.lstat(path)
    attributes = getattr(metadata, "st_file_attributes", 0)
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return stat.S_ISLNK(metadata.st_mode) or bool(attributes & reparse_flag)


def assert_confined(output_root: Path, target: Path, *, label: str) -> None:
    """Reject lexical escapes and existing symlink/junction/reparse ancestors.

    The check is repeated immediately before every publication-sensitive write or
    rename. Python cannot make the full traversal race-free on Windows, but this
    prevents a pre-existing destination component from redirecting writes outside
    the resolved output root.
    """
    root = output_root.resolve(strict=True)
    absolute = Path(os.path.abspath(target))
    try:
        relative = absolute.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"{label} escapes output root: {target}") from exc
    current = root
    for component in relative.parts:
        current = current / component
        if not path_lexists(current):
            continue
        if is_reparse_or_link(current):
            raise ValueError(f"{label} traverses a symlink, junction, or reparse point: {current}")
        resolved = current.resolve(strict=True)
        try:
            resolved.relative_to(root)
        except ValueError as exc:
            raise ValueError(f"{label} resolves outside output root: {current}") from exc


def ensure_confined_directory(output_root: Path, directory: Path, *, label: str) -> None:
    assert_confined(output_root, directory, label=label)
    directory.mkdir(parents=True, exist_ok=True)
    assert_confined(output_root, directory, label=label)


def commit_marker_path(output_root: Path, diagram_id: str, revision: str) -> Path:
    return output_root / ".evidence-grounded-diagrams" / "commits" / diagram_id / f"{revision}.yml"


def write_commit_marker(
    output_root: Path,
    marker: Path,
    diagram_id: str,
    revision: str,
    bundle: Path,
) -> None:
    """Atomically record that this immutable revision completed persistence."""
    ensure_confined_directory(output_root, marker.parent, label="commit marker parent")
    assert_confined(output_root, marker, label="commit marker")
    value = {
        "contract_version": "1.0.0",
        "diagram_id": diagram_id,
        "revision": revision,
        "bundle_path": str(bundle),
        "manifest_sha256": sha256(bundle / "diagram.meta.yml"),
        "committed_at": (
            datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        ),
    }
    temporary = marker.with_name(f".{marker.name}.{uuid.uuid4().hex}.tmp")
    assert_confined(output_root, temporary, label="temporary commit marker")
    try:
        write_yaml(temporary, value)
        assert_confined(output_root, temporary, label="temporary commit marker")
        assert_confined(output_root, marker, label="commit marker")
        temporary.replace(marker)
    finally:
        if path_lexists(temporary):
            temporary.unlink()


def safe_member(staging: Path, relative: str) -> Path:
    candidate = Path(relative)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"unsafe member path: {relative}")
    resolved = (staging / candidate).resolve()
    resolved.relative_to(staging.resolve())
    return resolved


@contextmanager
def output_lock(output_root: Path, timeout_seconds: float = 30.0):
    """Hold one cross-platform lock for revision reservation and index mutation."""
    output_root.mkdir(parents=True, exist_ok=True)
    output_root = output_root.resolve(strict=True)
    lock_path = output_root / ".evidence-grounded-diagrams.lock"
    assert_confined(output_root, lock_path, label="output lock")
    handle = lock_path.open("a+b")
    if lock_path.stat().st_size == 0:
        handle.write(b"0")
        handle.flush()
    deadline = time.monotonic() + timeout_seconds
    acquired = False
    try:
        while not acquired:
            try:
                handle.seek(0)
                if os.name == "nt":
                    import msvcrt

                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
            except OSError:
                if time.monotonic() >= deadline:
                    raise TimeoutError(f"timed out acquiring output lock: {lock_path}")
                time.sleep(0.05)
        yield
    finally:
        if acquired:
            handle.seek(0)
            if os.name == "nt":
                import msvcrt

                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def quarantine_bundle(output_root: Path, final_dir: Path, diagram_id: str, revision: str) -> Path | None:
    assert_confined(output_root, final_dir, label="final bundle")
    if not path_lexists(final_dir):
        return None
    quarantine = output_root / ".quarantine" / diagram_id / f"{revision}-{uuid.uuid4().hex}"
    ensure_confined_directory(output_root, quarantine.parent, label="quarantine parent")
    assert_confined(output_root, final_dir, label="final bundle")
    assert_confined(output_root, quarantine, label="quarantine destination")
    final_dir.replace(quarantine)
    return quarantine


def update_index(output_root: Path, index_path: Path, manifest: dict[str, Any], bundle: Path) -> None:
    assert_confined(output_root, index_path, label="resolver index")
    if index_path.is_file():
        index = load_yaml(index_path)
    else:
        index = {"index_version": "1.0.0", "generated_at": None, "entries": []}
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{index_path}: entries must be a list")
    diagram_id = manifest["diagram_id"]
    revision = manifest["revision"]
    entries = [
        entry
        for entry in entries
        if not (
            entry.get("diagram_id") == diagram_id
            and entry.get("revision") == revision
        )
    ]
    entries.append(
        {
            "diagram_id": diagram_id,
            "revision": revision,
            "lifecycle_status": manifest["lifecycle_status"],
            "diagram_kind": manifest["tags"]["diagram_kind"],
            "epistemic_status": manifest["aggregate_status"],
            "topics": manifest["tags"]["topics"],
            "bundle_path": str(bundle),
            "validation_overall": "pending",
        }
    )
    entries.sort(key=lambda item: (item["diagram_id"], item["revision"]))
    index["generated_at"] = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    index["entries"] = entries
    temporary = index_path.with_name(f".{index_path.name}.{uuid.uuid4().hex}.tmp")
    assert_confined(output_root, temporary, label="temporary resolver index")
    try:
        write_yaml(temporary, index)
        assert_confined(output_root, temporary, label="temporary resolver index")
        assert_confined(output_root, index_path, label="resolver index")
        temporary.replace(index_path)
    finally:
        if path_lexists(temporary):
            temporary.unlink()


def set_index_validation(
    output_root: Path,
    index_path: Path,
    diagram_id: str,
    revision: str,
    overall: str | None,
) -> None:
    assert_confined(output_root, index_path, label="resolver index")
    index = load_yaml(index_path)
    entries = index.get("entries")
    if not isinstance(entries, list):
        raise ValueError(f"{index_path}: entries must be a list")
    if overall is None:
        entries = [
            entry for entry in entries
            if not (
                entry.get("diagram_id") == diagram_id
                and entry.get("revision") == revision
            )
        ]
    else:
        matched = 0
        for entry in entries:
            if entry.get("diagram_id") == diagram_id and entry.get("revision") == revision:
                entry["validation_overall"] = overall
                matched += 1
        if matched != 1:
            raise ValueError("resolver index entry disappeared during validation")
    for entry in entries:
        bundle_value = entry.get("bundle_path")
        receipt_path = Path(str(bundle_value)) / "validation.receipt.yml"
        try:
            receipt = load_yaml(receipt_path)
            if (
                receipt.get("diagram_id") == entry.get("diagram_id")
                and receipt.get("revision") == entry.get("revision")
            ):
                entry["validation_overall"] = str(receipt.get("overall", "unknown"))
            else:
                entry["validation_overall"] = "unknown"
        except (OSError, UnicodeError, ValueError, yaml.YAMLError):
            entry["validation_overall"] = "unknown"
    index["entries"] = entries
    index["generated_at"] = (
        datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    )
    temporary = index_path.with_name(f".{index_path.name}.{uuid.uuid4().hex}.tmp")
    assert_confined(output_root, temporary, label="temporary resolver index")
    try:
        write_yaml(temporary, index)
        assert_confined(output_root, temporary, label="temporary resolver index")
        assert_confined(output_root, index_path, label="resolver index")
        temporary.replace(index_path)
    finally:
        if path_lexists(temporary):
            temporary.unlink()


def snapshot_index(output_root: Path, index_path: Path) -> tuple[bool, bytes | None]:
    assert_confined(output_root, index_path, label="resolver index")
    if not path_lexists(index_path):
        return False, None
    if not index_path.is_file():
        raise ValueError(f"resolver index is not a regular file: {index_path}")
    return True, index_path.read_bytes()


def restore_index(
    output_root: Path,
    index_path: Path,
    existed: bool,
    contents: bytes | None,
) -> None:
    """Restore the exact pre-publication index bytes after any later failure."""
    assert_confined(output_root, index_path, label="resolver index rollback")
    if not existed:
        if path_lexists(index_path):
            if not index_path.is_file():
                raise ValueError(f"cannot roll back non-file resolver index: {index_path}")
            index_path.unlink()
        return
    if contents is None:
        raise ValueError("resolver index snapshot is missing")
    temporary = index_path.with_name(f".{index_path.name}.{uuid.uuid4().hex}.rollback")
    assert_confined(output_root, temporary, label="temporary resolver index rollback")
    try:
        temporary.write_bytes(contents)
        assert_confined(output_root, temporary, label="temporary resolver index rollback")
        assert_confined(output_root, index_path, label="resolver index rollback")
        temporary.replace(index_path)
    finally:
        if path_lexists(temporary):
            temporary.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staging-dir", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    staging = args.staging_dir.resolve()
    output_root = args.output_root.resolve()
    manifest_path = staging / "diagram.meta.yml"
    model_path = staging / "diagram.model.yml"
    manifest = load_yaml(manifest_path)
    request_member = manifest.get("members", {}).get("request", {})
    if not isinstance(request_member, dict) or not isinstance(request_member.get("path"), str):
        raise ValueError("manifest requires a request member path")
    request_path = safe_member(staging, request_member["path"])
    receipt_path = staging / "validation.receipt.yml"
    model = load_yaml(model_path)
    request = load_yaml(request_path)
    receipt = load_yaml(receipt_path)
    diagram_id = manifest.get("diagram_id")
    revision = manifest.get("revision")
    if not isinstance(diagram_id, str) or not isinstance(revision, str):
        raise ValueError("manifest requires diagram_id and revision")
    if DIAGRAM_ID_PATTERN.fullmatch(diagram_id) is None:
        raise ValueError(f"unsafe diagram_id: {diagram_id!r}")
    if REVISION_PATTERN.fullmatch(revision) is None:
        raise ValueError(f"unsafe revision: {revision!r}")
    if manifest.get("lifecycle_status") != "draft":
        raise ValueError("initial persistence accepts draft lifecycle only")
    if manifest.get("promotion_status") != "not-promoted":
        raise ValueError("initial draft persistence accepts not-promoted artifacts only")
    if manifest.get("promotion_evidence") is not None:
        raise ValueError("initial draft persistence cannot carry promotion evidence")
    if request.get("mode") not in {"create", "revise"}:
        raise ValueError("diagram persistence accepts create or revise requests only")
    for label, artifact in (("model", model), ("receipt", receipt)):
        if (artifact.get("diagram_id"), artifact.get("revision")) != (diagram_id, revision):
            raise ValueError(f"{label} identity does not match manifest")

    final_dir = output_root / diagram_id / revision
    index_path = output_root / "index.yml"
    commit_marker = commit_marker_path(output_root, diagram_id, revision)
    validator = Path(__file__).with_name("validate_diagram_bundle.py")
    with output_lock(output_root):
        assert_confined(output_root, final_dir, label="final bundle")
        assert_confined(output_root, index_path, label="resolver index")
        assert_confined(output_root, commit_marker, label="commit marker")
        if path_lexists(final_dir):
            if commit_marker.is_file():
                raise FileExistsError(
                    "refusing to overwrite existing revision or reuse its committed identity, "
                    f"even when its bytes are invalid: {final_dir}"
                )
            existing = subprocess.run(
                [sys.executable, str(validator), str(final_dir)],
                check=False,
                capture_output=True,
                text=True,
            )
            if existing.returncode == 0:
                write_commit_marker(output_root, commit_marker, diagram_id, revision, final_dir)
                print(f"FINALIZED_UNMARKED_COMMIT={commit_marker}", file=sys.stderr)
                print(f"PERSISTED_BUNDLE={final_dir}")
                return 0
            if index_path.is_file():
                try:
                    set_index_validation(output_root, index_path, diagram_id, revision, None)
                except Exception:
                    pass
            recovered = quarantine_bundle(output_root, final_dir, diagram_id, revision)
            if recovered is not None:
                print(f"RECOVERED_ORPHAN_TO_QUARANTINE={recovered}", file=sys.stderr)
        index_existed, index_contents = snapshot_index(output_root, index_path)
        ensure_confined_directory(output_root, final_dir.parent, label="bundle parent")
        temp_dir = final_dir.parent / f".{revision}.staging-{uuid.uuid4().hex}"
        assert_confined(output_root, temp_dir, label="temporary bundle")
        temp_dir.mkdir()
        assert_confined(output_root, temp_dir, label="temporary bundle")
        published_final = False
        try:
            members = manifest.get("members")
            if not isinstance(members, dict):
                raise ValueError("manifest.members must be a mapping")
            copied_names: set[str] = set()
            for member_name, record in members.items():
                if record is None:
                    continue
                if not isinstance(record, dict) or not isinstance(record.get("path"), str):
                    raise ValueError(f"invalid member record: {member_name}")
                source = safe_member(staging, record["path"])
                if not source.is_file():
                    raise FileNotFoundError(f"missing staged member: {source}")
                destination = temp_dir / record["path"]
                ensure_confined_directory(
                    output_root, destination.parent, label=f"member parent {member_name}"
                )
                assert_confined(output_root, destination, label=f"member {member_name}")
                shutil.copy2(source, destination)
                copied_names.add(member_name)

            required_members = (
                "request", "source", "semantic_model", "textual_equivalent", "validation_receipt"
            )
            for required in required_members:
                if required not in copied_names:
                    raise ValueError(f"missing required staged member: {required}")

            request_record = members["request"]
            persisted_request = load_yaml(temp_dir / request_record["path"])
            persisted_request["storage"]["output_root"] = str(output_root)
            write_yaml(temp_dir / request_record["path"], persisted_request)
            request_digest = sha256(temp_dir / request_record["path"])
            binding = {
                "request_id": persisted_request["request_id"],
                "evidence_set_id": persisted_request["evidence_set"]["evidence_set_id"],
                "request_sha256": request_digest,
                "evidence_snapshot_digest": persisted_request["evidence_set"].get("snapshot_digest"),
            }
            model["request_binding"] = binding
            manifest["request_binding"] = binding
            write_yaml(temp_dir / members["semantic_model"]["path"], model)

            for member_name in (
                "request", "source", "render", "semantic_model", "textual_equivalent"
            ):
                record = members.get(member_name)
                if isinstance(record, dict):
                    record["sha256"] = sha256(temp_dir / record["path"])

            manifest["persistence"] = {
                "state": "saved",
                "output_root": str(output_root),
                "bundle_path": str(final_dir),
                "index_path": str(index_path),
            }
            write_yaml(temp_dir / "diagram.meta.yml", manifest)
            preflight_result = subprocess.run(
                [sys.executable, str(validator), str(temp_dir), "--preflight"],
                check=False,
                capture_output=True,
                text=True,
            )
            sys.stdout.write(preflight_result.stdout)
            sys.stderr.write(preflight_result.stderr)
            if preflight_result.returncode:
                return preflight_result.returncode

            assert_confined(output_root, temp_dir, label="temporary bundle")
            assert_confined(output_root, final_dir, label="final bundle")
            if path_lexists(final_dir):
                raise FileExistsError(f"refusing to overwrite concurrently created revision: {final_dir}")
            temp_dir.replace(final_dir)
            published_final = True
            update_index(output_root, index_path, manifest, final_dir)

            write_result = subprocess.run(
                [sys.executable, str(validator), str(final_dir), "--write-receipt"],
                check=False,
                capture_output=True,
                text=True,
            )
            sys.stdout.write(write_result.stdout)
            sys.stderr.write(write_result.stderr)
            if write_result.returncode:
                raise ValueError("persisted bundle failed receipt generation")
            verify_result = subprocess.run(
                [sys.executable, str(validator), str(final_dir)],
                check=False,
                capture_output=True,
                text=True,
            )
            sys.stdout.write(verify_result.stdout)
            sys.stderr.write(verify_result.stderr)
            if verify_result.returncode:
                raise ValueError("persisted bundle failed final verification")
            persisted_receipt = load_yaml(final_dir / "validation.receipt.yml")
            set_index_validation(
                output_root,
                index_path,
                diagram_id,
                revision,
                str(persisted_receipt.get("overall", "DRAFT")),
            )
            write_commit_marker(output_root, commit_marker, diagram_id, revision, final_dir)
        except Exception as original:
            cleanup_errors: list[str] = []
            if published_final:
                try:
                    quarantine = quarantine_bundle(output_root, final_dir, diagram_id, revision)
                    if quarantine is not None:
                        print(f"QUARANTINED_INCOMPLETE_BUNDLE={quarantine}", file=sys.stderr)
                except Exception as exc:
                    cleanup_errors.append(f"bundle quarantine failed: {exc}")
            try:
                restore_index(output_root, index_path, index_existed, index_contents)
            except Exception as exc:
                cleanup_errors.append(f"index rollback failed: {exc}")
            if cleanup_errors:
                raise RuntimeError(
                    f"persistence failed ({original}); cleanup incomplete: {'; '.join(cleanup_errors)}"
                ) from original
            raise
        finally:
            if temp_dir.exists():
                assert_confined(output_root, temp_dir, label="temporary bundle cleanup")
                shutil.rmtree(temp_dir)
    print(f"PERSISTED_BUNDLE={final_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
