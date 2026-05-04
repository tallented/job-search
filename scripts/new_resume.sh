#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  new_resume.sh <cto|em|principal> <company> <role> [folder-name]

Examples:
  new_resume.sh cto "Acme" "CTO"
  new_resume.sh em "Acme" "Engineering Manager"
  new_resume.sh principal "ExampleCo" "Distinguished Engineer"
  new_resume.sh cto "Acme" "VP Engineering" "20260330 - Acme - VP Engineering"

Environment overrides:
  BASE_DIR    Directory containing the base resume .docx files
  SEND_TO_DIR Destination root for new resume folders
  JOB_LINK    Optional job posting URL for the NocoDB tracker row
  JOB_TYPE    Optional tracker type; defaults to "Full time"
  JOB_LOCATION Optional tracker location
  JOB_SALARY  Optional tracker salary text
  LISTING_SOURCE Optional tracker listing source
  NEXT_STEPS  Optional tracker next-steps text
  REF_NUMBER  Optional tracker reference number
  SKIP_TRACKER If set to 1, skip adding a Created row to the tracker
EOF
}

sanitize_component() {
  local value="$1"
  value="${value//$'\n'/ }"
  value="${value//\// - }"
  value="${value//:/ -}"
  printf '%s' "$value"
}

if [[ $# -lt 3 || $# -gt 4 ]]; then
  usage >&2
  exit 1
fi

track="$(printf '%s' "$1" | tr '[:upper:]' '[:lower:]')"
company="$(sanitize_component "$2")"
role="$(sanitize_component "$3")"
today_stamp="$(date +%Y%m%d)"
folder_name="$(sanitize_component "${4:-$today_stamp - $company - $role}")"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
workspace_dir="$(cd "$script_dir/.." && pwd)"

base_dir="${BASE_DIR:-$workspace_dir}"
send_to_dir="${SEND_TO_DIR:-$workspace_dir/Send To}"
tracker_script="${TRACKER_CREATE_SCRIPT:-$workspace_dir/job-tracker/create-application.sh}"

case "$track" in
  cto|exec|vp|head)
    base_resume="$base_dir/CANONICAL - Chris Tallent Resume - CTO.docx"
    track_label="CTO / VP Engineering"
    ;;
  em|manager|mgr|engmgr|engineering-manager|director|lead)
    base_resume="$base_dir/CANONICAL - Chris Tallent Resume - Engineering Manager.docx"
    track_label="Engineering Manager / Senior Engineering Manager / Director"
    ;;
  principal|engineer|pe|ic)
    base_resume="$base_dir/CANONICAL - Chris Tallent Resume - Principal Engineer.docx"
    track_label="Principal / Distinguished Engineer"
    ;;
  *)
    printf 'Unknown track: %s\n' "$track" >&2
    usage >&2
    exit 1
    ;;
esac

if [[ ! -f "$base_resume" ]]; then
  printf 'Base resume not found: %s\n' "$base_resume" >&2
  exit 1
fi

target_dir="$send_to_dir/$folder_name"
target_resume="$target_dir/Chris Tallent Resume - $company - $role.docx"
target_job_description="$target_dir/job description.txt"
target_draft="$target_dir/draft.md"

if [[ -e "$target_dir" ]]; then
  printf 'Target folder already exists: %s\n' "$target_dir" >&2
  exit 1
fi

mkdir -p "$target_dir"
cp "$base_resume" "$target_resume"
: > "$target_job_description"

cat > "$target_draft" <<EOF
# $company - $role

## Base
- Track: $track_label
- Source resume: $(basename "$base_resume")
- Output resume: $(basename "$target_resume")

## Job Requirements
- 

## Halo First 30 Seconds
- Headline:
- Summary:
- Core skills order:

## Targeted Bullet Swaps
- 

## Copy-Fit Notes
- The copied .docx is the master formatting shell. Edit inside that file rather than replacing it with a newly generated Word document by default.
- Prefer bullet swaps and summary tightening before touching margins.
- Keep the Word template intact unless a final pass still overflows.
EOF

printf 'Created:\n'
printf '  %s\n' "$target_dir"
printf '  %s\n' "$target_resume"
printf '  %s\n' "$target_job_description"
printf '  %s\n' "$target_draft"

if [[ "${SKIP_TRACKER:-0}" != "1" ]]; then
  if [[ ! -x "$tracker_script" ]]; then
    printf 'Warning: tracker helper not found or not executable: %s\n' "$tracker_script" >&2
  else
    tracker_args=(
      --company "$company"
      --title "$role"
      --status "CREATED"
      --created "$today_stamp"
      --resume-folder "$target_dir"
      --type "${JOB_TYPE:-Full time}"
      --skip-if-exists
    )
    [[ -n "${JOB_LINK:-}" ]] && tracker_args+=(--link "$JOB_LINK")
    [[ -n "${JOB_LOCATION:-}" ]] && tracker_args+=(--location "$JOB_LOCATION")
    [[ -n "${JOB_SALARY:-}" ]] && tracker_args+=(--salary "$JOB_SALARY")
    [[ -n "${LISTING_SOURCE:-}" ]] && tracker_args+=(--listing-source "$LISTING_SOURCE")
    [[ -n "${NEXT_STEPS:-}" ]] && tracker_args+=(--next-steps "$NEXT_STEPS")
    [[ -n "${REF_NUMBER:-}" ]] && tracker_args+=(--ref-number "$REF_NUMBER")

    if "$tracker_script" "${tracker_args[@]}" >/dev/null; then
      printf '  tracker row added in NocoDB\n'
    else
      printf 'Warning: unable to add tracker row in NocoDB\n' >&2
    fi
  fi
fi
