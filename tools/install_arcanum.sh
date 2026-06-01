#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
Usage: install_arcanum.sh [installer-options] -- [bootstrap-options]
       install_arcanum.sh [installer-options] [bootstrap-options]

Download Arcanum from GitHub and run the repository bootstrap script.

Installer options:
  --repo <owner/name>     GitHub repository. Default: cyberAlchemyAI/arcanum.
  --ref <ref>             Branch, tag, or commit archive ref. Default: main.
  --archive-url <url>     Explicit archive URL. Overrides --repo and --ref.
  -h, --help              Show this help.

Bootstrap options are forwarded to tools/bootstrap_arcanum.sh, for example:
  --target <path>
  --sigils <list|all>
  --spells <list|all|none>
  --profile <personal-codex,repo-codex,repo-local,github-copilot,claude,observability|all|none>
  --profiles <personal-codex,repo-codex,repo-local,github-copilot,claude,observability|all|none>
  --runtime <claude|copilot|github-copilot|all|none>
  --surfaces <claude|copilot|github-copilot|all|none>
  --default-adapter <native-skill|codex-skill|claude-skill|copilot-instructions|local-skill|codex-exec|codex-bypass|dry-run|none>
  --codex-home <path>
  --legacy-codex-commands
  --clean-legacy-codex-commands
  --prefixed-skill-packages
  --force
  --dry-run

Examples:
  curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --sigils all --spells all --profile all

  curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/arcanum/main/tools/install_arcanum.sh | bash -s -- --target . --sigils ontology-vault,context-builder --spells ontology-harness --profiles repo-codex,repo-local,github-copilot,claude

  curl -fsSL https://raw.githubusercontent.com/cyberAlchemyAI/arcanum/main/tools/install_arcanum.sh | bash -s -- --profile personal-codex --codex-home "$HOME/.codex"
USAGE
}

repo="${ARCANUM_REPO:-cyberAlchemyAI/arcanum}"
ref="${ARCANUM_REF:-main}"
archive_url="${ARCANUM_ARCHIVE_URL:-}"
bootstrap_args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      repo="$2"
      shift 2
      ;;
    --ref)
      ref="$2"
      shift 2
      ;;
    --archive-url)
      archive_url="$2"
      shift 2
      ;;
    --)
      shift
      bootstrap_args+=("$@")
      break
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      bootstrap_args+=("$1")
      shift
      ;;
  esac
done

if [[ -z "$archive_url" ]]; then
  archive_url="https://github.com/$repo/archive/$ref.tar.gz"
fi

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/arcanum-install-XXXXXX")"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

archive="$tmpdir/arcanum.tar.gz"

download_archive() {
  if command -v curl >/dev/null 2>&1; then
    curl -fsSL "$archive_url" -o "$archive"
  elif command -v wget >/dev/null 2>&1; then
    wget -qO "$archive" "$archive_url"
  else
    echo "curl or wget is required to download Arcanum." >&2
    exit 1
  fi
}

echo "Downloading Arcanum from $archive_url"
download_archive

tar -xzf "$archive" -C "$tmpdir"
source_root="$(find "$tmpdir" -mindepth 1 -maxdepth 1 -type d | sort | head -n 1)"

if [[ -z "$source_root" || ! -f "$source_root/tools/bootstrap_arcanum.sh" ]]; then
  echo "Downloaded archive does not contain tools/bootstrap_arcanum.sh." >&2
  exit 1
fi

bash "$source_root/tools/bootstrap_arcanum.sh" "${bootstrap_args[@]}"
