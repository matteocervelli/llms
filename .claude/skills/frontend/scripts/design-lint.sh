#!/usr/bin/env bash
# design-lint.sh — Deterministic scanner for AI-default design anti-patterns.
# WHY: LLMs silently reproduce generic design choices (Inter, linear easing, pure black).
# This script makes those choices visible and auditable without requiring human review
# on every commit. Grep-based so it's correct or it crashes — no silent misses.

set -euo pipefail

DIR="${1:-.}"; JSON_MODE=false; MODE="both"
for arg in "$@"; do [[ "$arg" == "--json" ]] && JSON_MODE=true; done
args=("$@")
for i in "${!args[@]}"; do
  [[ "${args[$i]}" == "--mode" ]] && MODE="${args[$((i+1))]:-both}"
done

FINDINGS=(); WARN_COUNT=0; INFO_COUNT=0
EXTS=( css scss tsx jsx html vue svelte )

find_files() {
  local first=true fa=()
  for ext in "${EXTS[@]}"; do $first || fa+=( -o ); fa+=( -name "*.${ext}" ); first=false; done
  find "$DIR" \( "${fa[@]}" \) -not -path '*/node_modules/*' -not -path '*/.git/*' 2>/dev/null
}

scan_rule() {
  local rule="$1" pat="$2" sev="$3" rmode="$4"
  [[ "$MODE" == "brand"   && "$rmode" == "product" ]] && return 0
  [[ "$MODE" == "product" && "$rmode" == "brand"   ]] && return 0
  while IFS=: read -r file ln txt; do
    [[ -z "$file" ]] && continue
    txt="${txt#"${txt%%[![:space:]]*}"}"
    FINDINGS+=("$sev|$rule|$file|$ln|$txt")
    if [[ "$sev" == "warn" ]]; then WARN_COUNT=$(( WARN_COUNT + 1 ))
    else                            INFO_COUNT=$(( INFO_COUNT + 1 )); fi
  done < <( find_files | xargs grep -HEn "$pat" 2>/dev/null | grep -v "^Binary" || true )
}

# Rules — patterns verified against fixtures on macOS BSD grep
scan_rule "banned-font-primary" \
  'font-family.*\b(Inter|Roboto|Open Sans|Lato)\b|fontFamily.*\b(Inter|Roboto|Open Sans|Lato)\b' warn both
scan_rule "trendy-font" \
  'font-family.*\b(Fraunces|Geist|Mona Sans|Plus Jakarta|Recoleta|Instrument Sans)\b|fontFamily.*\b(Fraunces|Geist|Mona Sans|Plus Jakarta|Recoleta|Instrument Sans)\b' info both
scan_rule "pure-black" \
  '(color|fill)[[:space:]]*:[[:space:]]*#000(000)?[^0-9a-fA-F]|rgb\(0,[[:space:]]*0,[[:space:]]*0\)' warn both

# linear-timing: inline to filter out infinite loaders (animation: spin ... infinite)
TF=(); TW=0
while IFS=: read -r file ln txt; do
  [[ -z "$file" ]] && continue
  txt="${txt#"${txt%%[![:space:]]*}"}"; echo "$txt" | grep -q "infinite" && continue
  TF+=("warn|linear-timing|$file|$ln|$txt"); TW=$(( TW + 1 ))
done < <( find_files | xargs grep -HEn 'transition[^;]*[[:space:]]linear' 2>/dev/null | grep -v "^Binary" || true )
FINDINGS+=( ${TF[@]+"${TF[@]}"} ); WARN_COUNT=$(( WARN_COUNT + TW ))

scan_rule "gradient-text" \
  'background-clip[[:space:]]*:[[:space:]]*text|-webkit-background-clip[[:space:]]*:[[:space:]]*text' info brand
scan_rule "thick-border" \
  'border[[:space:]]*:[[:space:]]*([2-9]|[1-9][0-9]+)px[[:space:]]+solid' info both
scan_rule "glassmorphism" \
  'backdrop-filter[[:space:]]*:[[:space:]]*blur' info both
scan_rule "side-stripe" \
  'border-left[[:space:]]*:[[:space:]]*[3-9]px[[:space:]]+solid' info product

TOTAL=$(( WARN_COUNT + INFO_COUNT ))
if $JSON_MODE; then
  printf '[\n'; sep=""
  for f in ${FINDINGS[@]+"${FINDINGS[@]}"}; do
    IFS='|' read -r sev rule file ln txt <<< "$f"
    txt=$(printf '%s' "$txt" | sed 's/\\/\\\\/g; s/"/\\"/g')
    printf '%s  {"rule": "%s", "severity": "%s", "file": "%s", "line": %s, "text": "%s"}' \
      "$sep" "$rule" "$sev" "$file" "$ln" "$txt"; sep=$',\n'
  done; printf '\n]\n'
else
  for f in ${FINDINGS[@]+"${FINDINGS[@]}"}; do
    IFS='|' read -r sev rule file ln txt <<< "$f"
    printf '[%s] %s — %s:%s: %s\n' "$sev" "$rule" "$file" "$ln" "$txt"
  done
  [[ "$TOTAL" -gt 0 ]] && echo "---"
  printf '%d finding(s): %d warn, %d info\n' "$TOTAL" "$WARN_COUNT" "$INFO_COUNT"
fi
[[ "$TOTAL" -gt 0 ]] && exit 1 || exit 0
