# Acceptance audit — 2026-11-22

Scope: existing work at `origin/main` `0ebd73e6e671c84c71ecb653e3708ef06b71f3a0`; all merged PRs from the paginated GitHub API; all tracked instructions, docs and Python entry points. Only [ACCEPTANCE.md](../ACCEPTANCE.md) and its incorporated repository instructions apply. Historical work is assessed against today's standard, not assumed to have been governed by it at the time.

| # | Item | Fails rule | Source rule | Fix or not fixable |
|---|------|------------|-------------|--------------------|
| 1 | README and historical write-up omitted product status and next action | "Demo ≠ product"; "LIVE / BLOCKED / LOCAL ONLY + next human action in one line" | `ACCEPTANCE.md` §5, quoting `ship-visible-mvp.mdc` | Added LOCAL ONLY and specific next human actions. Homepage is null, Pages API returns HTTP 404, deployments API returns zero entries. The write-up's external Tinker inference endpoint returns HTTP 405 to unauthenticated GET; that provider endpoint is not a deployed Ripple product. |
| 2 | Historical recap measurements/quality conclusions and SFT loss figures lacked accessible source artifacts | "Point to artifacts: screenshots, `verify-report.json`, CI output, command output"; "Do not claim verified if you did not observe it" | `ACCEPTANCE.md` §2, quoting `verification.mdc` / `AGENTS.md` | Preserved the original numbers, filenames and narrative; explicitly marked them as unverified historical reports in the write-up and SFT docstring, and qualified the proof conclusion. Re-verifying the original result is **not fixable here**: original picks, response/logs, source footage, recap and training checkpoint are not supplied. No invented job-ID requirement, replacement paid run or fabricated output. |

## Evidence and checks

- Exactly one merged PR: [#1](https://github.com/lilaclilac09/ripple/pull/1), acceptance/process files only. Its current body passes `python3 scripts/check_acceptance.py`; its merge SHA is an ancestor of `origin/main`. No merged UI PRs or browser app exist in this repository, so 390×844 browser evidence is not applicable.
- Read root `AGENTS.md`, `CLAUDE.md`, `.cursor/rules/acceptance.mdc` and README instructions. README requires stills/text only for model input, per-asset size below 2,097,152 bytes and local ffmpeg cutting. No additional English-only/privacy rule exists. No footage or media was uploaded during this audit; the music-clearance warning remains intact.
- `inkling-video-picks-inkling.jsonl`, `inkling-video-picks-inkling-cut.jsonl`, `inkling-video-playground-pack.txt`, `recap-inkling.mp4` and `inkling-video-picks.jsonl` are absent from this checkout. A prose reference to a filename is not a retrieved artifact. No original Tinker request was executed or original cost/quality result verified.
- No existing test suite, lint configuration, dependency manifest or build command was found. Syntax compilation of all seven tracked Python files passed (in memory, no cache files in the repo); four argparse CLI help commands passed.
- Real ffmpeg smoke on a clearly synthetic six-second test video, supplied synthetic transcript and one manually specified synthetic pick: pipeline wrote a pack and one sub-2-MB keyframe; cutter wrote a clip; recap output duration was between 0.8 and 1.5 seconds. This tests local plumbing only, not model performance or the reported event result.
- Full command output for the smoke checks above and below: [smoke-2026-11-22.log](acceptance-audit-evidence/smoke-2026-11-22.log), produced by [smoke.py](acceptance-audit-evidence/smoke.py).
- Missing-video input exited 1 with `Video not found`. MCP initialize, tools/list (five tools) and ping passed. No external inference or training calls were made. Whisper transcription and original end-to-end workflow were not run.
- Forbidden-claim search found no unsupported completion phrases in the existing product files; acceptance-rule prohibitions/source quotations are not completion claims. `git diff --check` and the prepared PR body's repo checker passed.

| blocked_on | evidence | impact | human_action | not_doing |
|------------|----------|--------|--------------|-----------|
| Original result artifacts and approved model access | Named picks/pack/recap absent; no original response or training checkpoint supplied | degraded: original measurements remain unverified | Supply original artifacts and approve any separate paid rerun | No synthetic fixture presented as the original event or training result |

Passed: merged PR #1's current closer and merge ancestry; no applicable UI PRs; synthetic local ffmpeg/MCP smoke and syntax checks; original music-clearance warning preserved.

Observed, no rule covers it: this repo has no okc/job-ID counting rule, so no such requirement was imported. The historical cost arithmetic and editorial taste were not re-judged without source artifacts. No hosting service was added to this local CLI project.
