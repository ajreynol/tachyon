# common.sh -- sourced by job_launcher/deploy and job_launcher/checks.
#   Locates this project's site file.  Nothing here is machine-specific:
#   everything personal comes from job_launcher/site.conf (git-ignored) or the
#   environment.
#
#   Site file: $TACHYON_SITE, else job_launcher/site.conf.
#
#   There is no launcher checkout to find.  submit, status, deploy and the
#   host scripts in host/ are all part of this repository; see README.md.

HERE=${HERE:-$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
SITE=${TACHYON_SITE:-$HERE/site.conf}
[ -f "$SITE" ] || { echo "job_launcher: no site file $SITE (copy job_launcher/site.conf.example to job_launcher/site.conf and edit)" >&2; exit 2; }
# shellcheck disable=SC1090
source "$SITE"
