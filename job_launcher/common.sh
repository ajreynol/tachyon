# common.sh -- sourced by job_launcher/submit, job_launcher/status and job_launcher/checks.
#   Locates this project's site file and the run-dev checkout, and compares
#   the checkout against run-dev.lock.  Nothing here is machine-specific:
#   everything personal comes from job_launcher/site.conf (git-ignored) or the
#   environment.
#
#   Resolution order for the run-dev checkout:
#     1. $RUN_DEV in the environment
#     2. RUN_DEV= in job_launcher/site.conf
#     3. ../run-dev next to this repository
#   Site file: $TACHYON_SITE, else job_launcher/site.conf.

HERE=${HERE:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
SITE=${TACHYON_SITE:-$HERE/site.conf}
[ -f "$SITE" ] || { echo "job_launcher: no site file $SITE (copy job_launcher/site.conf.example to job_launcher/site.conf and edit)" >&2; exit 2; }

ENV_RUN_DEV=${RUN_DEV:-}
RUN_DEV=""
# shellcheck disable=SC1090
source "$SITE"
RUN_DEV=${ENV_RUN_DEV:-${RUN_DEV:-$HERE/../../run-dev}}
RUN_DEV=${RUN_DEV/#\~/$HOME}
RUN_DEV=$(cd "$RUN_DEV" 2>/dev/null && pwd) \
  || { echo "job_launcher: no run-dev checkout at ${ENV_RUN_DEV:-${RUN_DEV:-../run-dev}} (set RUN_DEV in job_launcher/site.conf or the environment)" >&2; exit 2; }
for f in submit status; do
  [ -x "$RUN_DEV/$f" ] || { echo "job_launcher: $RUN_DEV does not look like a run-dev checkout: no executable $f" >&2; exit 2; }
done

# The pin.  A mismatch is a warning, not an error: the wrappers only depend on
# submit's interface (SUBMIT_SITE, config resolution, log.txt), which is
# stable, but the lock records what was actually tested.
LOCK=$HERE/run-dev.lock
WANT=$(sed -n 's/^commit=//p' "$LOCK" 2>/dev/null | tail -1)
HAVE=$(git -C "$RUN_DEV" rev-parse HEAD 2>/dev/null || echo unknown)
RUN_DEV_PINNED=1
if [ -n "$WANT" ] && [ "$HAVE" != "$WANT" ]; then
  RUN_DEV_PINNED=0
  echo "job_launcher: warning: run-dev at $RUN_DEV is at ${HAVE:0:10}; run-dev.lock pins ${WANT:0:10} (see job_launcher/README.md, 'The pin')" >&2
fi
