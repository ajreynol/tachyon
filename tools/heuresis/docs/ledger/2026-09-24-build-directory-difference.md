# 2026-09-24 — two builds of one commit differ by 26 solves

**A caveat on every number this project records.** The reference configuration
was run twice at the same cvc5 revision, from two different build directories,
and the results are not the same. The difference is larger than most of the
option effects measured the day before.

## 1. What was asked

Wave 2 builds each branch in a build directory of its own, so that a branch
build cannot damage the launcher's. That raised a question worth answering
before the branch arms were trusted: does the new build directory measure the
same solver as the old one?

## 2. What was run

The reference configuration, `-q --no-cbqi --user-pat=strict
--sat-solver=cadical`, at cvc5
`d7d5b948c11d2d83be0212d4a954ef49740ecdab`, twice:

| run | build directory | binary |
| --- | --- | --- |
| 2026-09-23 | the launcher's, `BUILDDIR` from `site.conf` | `$REPO_BINARY`, installed by `run_install.sh` |
| 2026-09-24 | a separate clone and build directory used only for arms | built with `make`, installed under its own name |

Both `CMakeCache.txt` files record `CMAKE_BUILD_TYPE=Production`, the same
`ENABLE_ASSERTIONS=IGNORE`, empty `CMAKE_CXX_FLAGS`, and the same GCC 10
compiler. Both binaries verify as `git d7d5b948c1`.

## 3. The set

`quant-07-25`, 6124 benchmarks, 30 s, idle host.

## 4. What came back

| build | solved | unknown | timeout | PAR2 |
| --- | ---: | ---: | ---: | ---: |
| launcher's build directory | 5550 | 5 | 569 | 41055.9 |
| separate build directory | **5576** | 5 | 543 | **39304.4** |

Compared directly: the newer build solves **26 benchmarks the older one does
not and loses none** — a strict improvement, not a trade. PAR2 falls 4.3%.

## 5. What it settled

**Naming the revision is not enough; the build has to be named too.** Two
Production builds of one commit, same compiler and same declared settings,
differ by 26 solves on this set. For scale, the best option result of
2026-09-23 was `--ee-mode=central` at +67 and the second best `--ieval=off` at
+14; this build difference is between them.

**What is not established.** Why they differ. The older directory has been in
use for weeks and its dependencies were repaired earlier the same day after a
broken GMP rebuild; either accumulated state or that repair could explain it,
and neither was tested. A clean rebuild of the older directory would settle it
and was not run.

**Consequence for the register.** Figures measured in one build are not
comparable with figures measured in the other. The 2026-09-23 option sweep is
anchored to 5550 in the launcher's build; the branch arms of 2026-09-24 are
anchored to 5576 in the separate build. Each cell names the ledger entry that
carries its own reference, and the two are not to be read against each other.
