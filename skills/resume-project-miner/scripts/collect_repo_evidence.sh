#!/usr/bin/env bash
set -euo pipefail
umask 077

usage() {
  printf '%s\n' 'Usage: collect_repo_evidence.sh --source PATH|OWNER/REPO|URL --output DIR [--ref REF] [--since DATE] [--until DATE] [--author IDENTITY]...'
}

source_arg=''
output=''
ref=''
since=''
until=''
authors=()
is_remote=0
while (($#)); do
  case "$1" in
    --source) source_arg=${2-}; shift 2 ;;
    --output) output=${2-}; shift 2 ;;
    --ref) ref=${2-}; shift 2 ;;
    --since) since=${2-}; shift 2 ;;
    --until) until=${2-}; shift 2 ;;
    --author) authors+=("${2-}"); shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) printf 'Unknown argument: %s\n' "$1" >&2; usage >&2; exit 2 ;;
  esac
done
[[ -n "$source_arg" && -n "$output" ]] || { usage >&2; exit 2; }
if [[ -e "$output" ]]; then
  [[ -d "$output" && -z "$(find "$output" -mindepth 1 -maxdepth 1 -print -quit)" ]] || { printf 'Output path must be nonexistent or an empty directory: %s\n' "$output" >&2; exit 2; }
fi

for dependency in git sed awk find sort head; do
  command -v "$dependency" >/dev/null || { printf 'Missing required dependency: %s\n' "$dependency" >&2; exit 3; }
done

escape_git_regex() {
  printf '%s' "$1" | sed 's/[][\\.^$*+?(){}|]/\\&/g'
}

mkdir -p "$output"
chmod 700 "$output"
tmp_root=$(mktemp -d "${TMPDIR:-/tmp}/resume-project-miner.XXXXXX")
cleanup() { rm -rf "$tmp_root"; }
trap cleanup EXIT INT TERM

repo=''
remote_slug=''
if [[ -d "$source_arg" ]]; then
  repo=$(git -C "$source_arg" rev-parse --show-toplevel 2>/dev/null) || { printf 'Not a Git repository: %s\n' "$source_arg" >&2; exit 4; }
else
  is_remote=1
  command -v gh >/dev/null || { printf 'Remote sources require GitHub CLI (gh).\n' >&2; exit 5; }
  gh auth status >/dev/null || { printf 'GitHub authentication unavailable; run gh auth login outside this script.\n' >&2; exit 5; }
  remote_slug=${source_arg#https://github.com/}
  remote_slug=${remote_slug#git@github.com:}
  remote_slug=${remote_slug%.git}
  remote_slug=${remote_slug%/}
  [[ "$remote_slug" == */* && "$remote_slug" != */*/* ]] || { printf 'Unsupported GitHub source: %s\n' "$source_arg" >&2; exit 5; }
  gh repo clone "$remote_slug" "$tmp_root/repo" -- --filter=blob:none --bare --quiet >/dev/null
  repo="$tmp_root/repo"
fi

if [[ -n "$ref" ]]; then
  resolved=$(git -C "$repo" rev-parse --verify "${ref}^{commit}" 2>/dev/null) || { printf 'Unknown ref: %s\n' "$ref" >&2; exit 6; }
else
  resolved=$(git -C "$repo" rev-parse HEAD 2>/dev/null) || { printf 'Repository has no resolvable HEAD.\n' >&2; exit 6; }
fi

log_args=(--no-merges --date=iso-strict --format='%H%x09%aN%x09%aE%x09%ad%x09%s')
[[ -z "$since" ]] || log_args+=("--since=$since")
[[ -z "$until" ]] || log_args+=("--until=$until")
for author in "${authors[@]}"; do log_args+=("--author=$(escape_git_regex "$author")"); done
git -C "$repo" log "${log_args[@]}" "$resolved" | awk 'BEGIN {FS=OFS="\t"} {$3="[REDACTED]"; print}' > "$output/history.tsv"
git -C "$repo" shortlog -sne "$resolved" | sed -E 's/[[:space:]]+<[^>]*>/ <[REDACTED]>/' > "$output/contributors.tsv"

git -C "$repo" ls-tree -r -z --name-only "$resolved" | tr '\0' '\n' | awk '
  BEGIN { OFS="\t" }
  /(^|\/)(node_modules|vendor|dist|build|target|coverage|\.next|\.git)(\/|$)/ { next }
  /(^|\/)(\.env([^\/]*)?|id_rsa|id_ed25519|credentials([^\/]*)?|secrets?([^\/]*)?)(\/|$)/ { next }
  /\.(pem|key|p12|pfx|jks|keystore|mobileprovision)$/ { next }
  { kind="source" }
  /(^|\/)(README|CHANGELOG|CONTRIBUTING|ARCHITECTURE)(\.|$)/ { kind="docs" }
  /(^|\/)(package(-lock)?\.json|pnpm-lock\.yaml|yarn\.lock|pyproject\.toml|poetry\.lock|requirements[^\/]*\.txt|go\.mod|go\.sum|Cargo\.(toml|lock)|pom\.xml|build\.gradle(\.kts)?|Podfile|Package\.swift)$/ { kind="manifest" }
  /(^|\/)(Dockerfile|docker-compose[^\/]*|\.github\/workflows\/[^\/]+|Makefile|Justfile)$/ { kind="delivery" }
  /(^|\/)(test|tests|spec|specs|__tests__)(\/|$)|(_test|\.test|\.spec)\./ { kind="test" }
  /(^|\/)(migrations?|schema|models?)(\/|$)/ { kind="data" }
  { print kind, $0 }
' > "$output/manifest.tsv"

{
  printf 'field\tvalue\n'
  if ((is_remote)); then source_kind=remote; else source_kind=local; fi
  printf 'source_kind\t%s\n' "$source_kind"
  printf 'repository\t%s\n' "${remote_slug:-$(basename "$repo")}"
  printf 'resolved_commit\t%s\n' "$resolved"
  printf 'ref\t%s\n' "${ref:-HEAD}"
  printf 'since\t%s\n' "$since"
  printf 'until\t%s\n' "$until"
  printf 'git_user_name\t%s\n' "$(git -C "$repo" config user.name 2>/dev/null || true)"
  if [[ -n "$(git -C "$repo" config user.email 2>/dev/null || true)" ]]; then
    printf 'git_user_email\t[REDACTED]\n'
  else
    printf 'git_user_email\t\n'
  fi
  printf 'tracked_paths\t%s\n' "$(wc -l < "$output/manifest.tsv" | tr -d ' ')"
  printf 'selected_commits\t%s\n' "$(wc -l < "$output/history.tsv" | tr -d ' ')"
} > "$output/summary.md"

: > "$output/ownership.tsv"
if ((${#authors[@]})); then
  author_args=()
  for author in "${authors[@]}"; do author_args+=("--author=$(escape_git_regex "$author")"); done
  git -C "$repo" log --format= --name-only "${author_args[@]}" "$resolved" -- |
    sed '/^$/d' |
    awk '
      /(^|\/)(node_modules|vendor|third_party|third-party|external|dist|build|target|coverage|\.next|\.git)(\/|$)/ { next }
      /(^|\/)(\.env([^\/]*)?|id_rsa|id_ed25519|credentials([^\/]*)?|secrets?([^\/]*)?)(\/|$)/ { next }
      /\.(pem|key|p12|pfx|jks|keystore|mobileprovision)$/ { next }
      { print }
    ' | sort | uniq -c | sort -nr | awk 'BEGIN {OFS="\t"} {count=$1; $1=""; sub(/^ /, ""); print count, $0}' > "$output/ownership.tsv"
fi

if [[ -n "$remote_slug" ]]; then
  login=$(gh api user --jq .login 2>/dev/null || true)
  if command -v jq >/dev/null; then
    gh repo view "$remote_slug" --json nameWithOwner,description,isPrivate,primaryLanguage,repositoryTopics,defaultBranchRef,createdAt,updatedAt,url 2>/dev/null |
      jq --arg login "$login" '. + {authenticatedLogin: $login}' > "$output/github.json" || true
  else
    printf '{"note":"jq unavailable; GitHub JSON metadata omitted"}\n' > "$output/github.json"
  fi
fi

printf 'Evidence collected at %s\n' "$output"
