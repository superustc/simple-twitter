# Codex issue-to-PR pilot

This opt-in pipeline is a **manual** first step toward an Enzyme-style issue scanner and multi-agent development system. It never merges PRs or deploys the app.

## What is set up
- `AGENTS.md`: repository instructions for coding agents.
- `.github/workflows/codex-pilot.yml`: manual workflow taking one issue number, invoking the official `openai/codex-action`, running tests, and opening a **draft PR** only after tests pass.
- Pilot issue: https://github.com/superustc/simple-twitter/issues/1
- Staged plan: https://github.com/superustc/simple-twitter/issues/2

## One-time prerequisites (owner)
1. Review and merge the bootstrap PR so the workflow is available from the default branch. Do not turn on schedules yet.
2. Create an OpenAI API key for this automation (OpenAI API usage is separate from ChatGPT subscriptions).
3. Set the repository Actions secret **OPENAI_API_KEY** in repository Settings → Secrets and variables → Actions.
4. Confirm GitHub Actions is permitted to create pull requests (repository Settings → Actions → General → Workflow permissions, if this setting is exposed and editable).
5. Keep branch protections and required human review for `main`.

## Run the first test
- Open Actions → **Codex issue pilot** → Run workflow.
- Set `issue_number` to `1`.
- The workflow runs only when triggered by repository owner `superustc`, reads the issue, starts Codex with restricted workspace permissions, runs `python test_app.py`, and creates a draft PR if changes pass.
- Review the draft PR and CI logs; do not merge until the bug and tests are verified.

## Why only manual dispatch now?
GitHub Issues may contain malicious or misleading instructions. Automatic triage should never translate untrusted issue body text into unrestricted CI jobs. The manual owner gate limits the blast radius until basic correctness, token costs, and review quality are known.

## Next milestones
1. Pilot produces a reviewable draft PR for #1.
2. Fix any CI breakage, confirm isolated SQLite test setup, and record outcome.
3. Add a read-only daily triage workflow for approved issue labels only.
4. Add per-issue concurrency limits, duplicate-PR checks, retry bounds, and budget tracking.
5. Add Gemini/Claude workers and an independent reviewer *after* a sustained passing pilot.

## Failure modes
- No `OPENAI_API_KEY`: fail before calling Codex. Do not commit API keys or place them into issue text.
- Dependency/test errors: stop without creating a PR and inspect the Actions logs.
- Zero code changes: stop without creating a PR.
- AI produces incorrect code or falsely claims test results: runner checks the actual test exit code and human review remains required.
