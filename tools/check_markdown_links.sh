#!/usr/bin/env bash
set -u -o pipefail

usage() {
	cat <<'EOF'
Usage:
  bash tools/check_markdown_links.sh <markdown-file> [--check-anchors]

Examples:
  bash tools/check_markdown_links.sh framework/MARKDOWN-LINKING-CONSTITUTION.md
  bash tools/check_markdown_links.sh framework/MARKDOWN-LINKING-CONSTITUTION.md --check-anchors
EOF
}

if [[ ${1:-} == "-h" || ${1:-} == "--help" ]]; then
	usage
	exit 0
fi

if [[ $# -lt 1 || $# -gt 2 ]]; then
	usage
	exit 2
fi

markdown_file="$1"
check_anchors=0
if [[ ${2:-} == "--check-anchors" ]]; then
	check_anchors=1
elif [[ $# -eq 2 ]]; then
	usage
	exit 2
fi

if [[ ! -f "$markdown_file" ]]; then
	echo "ERROR: file not found: $markdown_file"
	exit 2
fi

markdown_dir="$(dirname "$markdown_file")"
missing=0

extract_links() {
	local file="$1"
	if command -v rg >/dev/null 2>&1; then
		rg -o '\[[^]]+\]\([^)]+\)' "$file" | sed -E 's/^.*\(([^)]+)\).*$/\1/' || true
	else
		grep -oE '\[[^]]+\]\([^)]+\)' "$file" | sed -E 's/^.*\(([^)]+)\).*$/\1/' || true
	fi
}

slugify_heading() {
	printf '%s' "$1" |
		tr '[:upper:]' '[:lower:]' |
		sed -E 's/`//g; s/[*_~]//g; s/[^a-z0-9 -]//g; s/[[:space:]]+/-/g; s/-+/-/g; s/^-//; s/-$//'
}

anchor_exists() {
	local file="$1"
	local anchor="$2"
	local heading
	while IFS= read -r heading; do
		heading="${heading#\#}"
		heading="${heading#\#}"
		heading="${heading#\#}"
		heading="${heading#\#}"
		heading="${heading#\#}"
		heading="${heading#\#}"
		heading="${heading#"${heading%%[![:space:]]*}"}"
		if [[ "$(slugify_heading "$heading")" == "$anchor" ]]; then
			return 0
		fi
	done < <(grep -E '^#{1,6}[[:space:]]+' "$file" || true)
	return 1
}

while IFS= read -r link; do
	[[ -z "$link" ]] && continue

	if [[ "$link" == http* || "$link" == mailto:* ]]; then
		continue
	fi

	base="${link%%#*}"
	anchor=""
	if [[ "$link" == *"#"* ]]; then
		anchor="${link#*#}"
	fi

	if [[ -z "$base" ]]; then
		target="$markdown_file"
	else
		base="${base//%20/ }"
		target="$markdown_dir/$base"
	fi

	if [[ ! -e "$target" ]]; then
		echo "MISSING $link"
		missing=1
		continue
	fi

	if [[ $check_anchors -eq 1 && -n "$anchor" && "$target" == *.md ]]; then
		if ! anchor_exists "$target" "$anchor"; then
			echo "MISSING_ANCHOR $link"
			missing=1
		fi
	fi
done < <(extract_links "$markdown_file")

if [[ $missing -eq 0 ]]; then
	echo "OK: all markdown links resolve"
	exit 0
fi

echo "FAIL: one or more markdown links are missing"
exit 1
