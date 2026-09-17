#!/usr/bin/env bash

# All inputs are explicit arguments (the drivers pass them); nothing is read from
# the environment or from the host conf, so a run is fully described by its
# command line.
#   -b BINARY   solver binary to run (required)
#   -s SIG      Cpc.eo signature to include in the proof  (ignored here)
#   -e ETHOS    ethos binary  (ignored here)
#   -l LOGOS    logos binary  (ignored here)
# followed by BENCHMARK [solver options...]
BIN=""; SIG=""; ETHOS=""; LOGOS=""
while [ $# -gt 0 ]; do
  case "$1" in
    -b) BIN=$2; shift 2 ;;
    -s) SIG=$2; shift 2 ;;
    -e) ETHOS=$2; shift 2 ;;
    -l) LOGOS=$2; shift 2 ;;
    --) shift; break ;;
    -*) echo "$(basename "$0"): unknown option $1" >&2; exit 2 ;;
    *) break ;;
  esac
done
[ -n "$BIN" ] || { echo "$(basename "$0"): -b is required" >&2; exit 2; }
[ $# -ge 1 ] || { echo "$(basename "$0"): no benchmark given" >&2; exit 2; }
BENCH=$1

# Why a failure happened is recorded to $HEURESIS_ERRLOG when the drivers set
# it.  It deliberately does NOT go into the result token: tools/heuresis/gap
# has a fixed column list (solved/sat/unsat/unknown/timeout/error), so a token
# like "error-segfault" would be counted in no column and the benchmark would
# quietly leave the accounting.  The token stays "error"; the reason goes here.
log_reason() {
  [ -n "${HEURESIS_ERRLOG:-}" ] || return 0
  printf '%s\t%s\n' "$1" "$(printf '%s' "$2" | head -1 | tr -d '\t' | cut -c1-200)" >> "$HEURESIS_ERRLOG"
}

function trywith {
  limit=$1; shift;
  result="$({ ulimit -S -t "$limit"; $BIN "$@"; } 2>&1)"
  # necessary since we can't silent warnings from z3?
  last_line=$(echo "$result" | tail -n 1)
  case "$last_line" in
    sat|unsat|unknown) echo "$last_line"; exit 0;;
    *)         echo "error"; log_reason "$BENCH" "$result";;
  esac
}

trywith 1800 $@
