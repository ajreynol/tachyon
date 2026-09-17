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

function trywith {
  limit=$1; shift;
  result="$({ ulimit -S -t "$limit"; $BIN "$@"; } 2>&1)"
  # necessary since we can't silent warnings from z3?
  last_line=$(echo "$result" | tail -n 1)
  case "$last_line" in
    sat|unsat|unknown) echo "$last_line"; exit 0;;
    *)         echo "error";;
  esac
}

trywith 1800 $@
