# common.sh -- sourced by job_launcher/submit, job_launcher/status and job_launcher/checks.
#   Locates this project's site file and the launcher checkout, and compares
#   the checkout against launcher.lock.  Nothing here is machine-specific:
#   everything personal comes from job_launcher/site.conf (git-ignored) or the
#   environment.
#
#   Resolution order for the launcher checkout:
#     1. $LAUNCHER_DIR in the environment
#     2. LAUNCHER_DIR= in job_launcher/site.conf
#   Site file: $TACHYON_SITE, else job_launcher/site.conf.

HERE=${HERE:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
SITE=${TACHYON_SITE:-$HERE/site.conf}
[ -f "$SITE" ] || { echo "job_launcher: no site file $SITE (copy job_launcher/site.conf.example to job_launcher/site.conf and edit)" >&2; exit 2; }

ENV_LAUNCHER_DIR=${LAUNCHER_DIR:-}
LAUNCHER_DIR=""
# shellcheck disable=SC1090
source "$SITE"
WANT_DIR=${ENV_LAUNCHER_DIR:-${LAUNCHER_DIR:-}}
[ -n "$WANT_DIR" ] \
  || { echo "job_launcher: no launcher checkout (set LAUNCHER_DIR in job_launcher/site.conf or the environment)" >&2; exit 2; }
WANT_DIR=${WANT_DIR/#\~/$HOME}
LAUNCHER_DIR=$(cd "$WANT_DIR" 2>/dev/null && pwd) \
  || { echo "job_launcher: no launcher checkout at $WANT_DIR (set LAUNCHER_DIR in job_launcher/site.conf or the environment)" >&2; exit 2; }
for f in submit status; do
  [ -x "$LAUNCHER_DIR/$f" ] || { echo "job_launcher: $LAUNCHER_DIR does not look like a launcher checkout: no executable $f" >&2; exit 2; }
done

# The pin.  A mismatch is a warning, not an error: the wrappers only depend on
# submit's interface (SUBMIT_SITE, config resolution, log.txt), which is
# stable, but the lock records what was actually tested.
LOCK=$HERE/launcher.lock
WANT=$(sed -n 's/^commit=//p' "$LOCK" 2>/dev/null | tail -1)
HAVE=$(git -C "$LAUNCHER_DIR" rev-parse HEAD 2>/dev/null || echo unknown)
LAUNCHER_PINNED=1
if [ -n "$WANT" ] && [ "$HAVE" != "$WANT" ]; then
  LAUNCHER_PINNED=0
  echo "job_launcher: warning: the launcher at $LAUNCHER_DIR is at ${HAVE:0:10}; launcher.lock pins ${WANT:0:10} (see job_launcher/README.md, 'The pin')" >&2
fi
