# Issue-to-draft-PR automation

The workflow scans open issues and pull requests, ranks eligible tasks, assigns approved issues to isolated GitHub-hosted runners, validates proposed patches, and opens draft pull requests after independent review. Maintainers decide when to merge.

## Setup

1. Review and merge the workflow PR. Keep the repository's existing branch protection and review rules.
2. Set `OPENAI_API_KEY` under **Settings → Environments → OPENAI_API_KEY → Environment secrets** or under **Settings → Secrets and variables → Actions → Repository secrets**. The environment secret takes precedence if both exist. Codex uses it for the single-issue pilot, optional AI triage, and independent review.
3. Under **Settings → Actions → General → Workflow permissions**, enable **Allow GitHub Actions to create and approve pull requests**. The pipeline only creates draft pull requests.
4. Keep `AGENT_WORKERS` unset for Codex-only operation, or set it to a comma-separated list such as `codex,claude,gemini`. Add `ANTHROPIC_API_KEY` for Claude Code and `GEMINI_API_KEY` for Gemini CLI before adding those workers. Each worker receives only its provider's secret. Codex supplies independent review for all workers.

## First runs

Open **Actions → Issue to draft PR → Run workflow**, selecting `main`.

- **Triage**. Leave `issue_number` at 0 and leave `run_approved` off. Download the JSON report from the run. When an OpenAI key is configured, the separate AI advisory adds suggested priority, severity, scope, dependencies, risk, and validation effort.
- **Single issue**. Enter an open issue number. The dispatch must come from the owner account, and it selects Codex. An issue with an existing draft or PR will be rejected. The initial HTTP chat pilot is tracked in [issue #1](https://github.com/superustc/simple-twitter/issues/1) and [PR #4](https://github.com/superustc/simple-twitter/pull/4). To validate the hosted worker while that fix is under review, dispatch a different small issue with a clear reproduction and test.
- **Approved batch**. Create the label `agent:approved` and apply it after reviewing scope and testability. Leave `issue_number` at 0 and turn on `run_approved`. The workflow reserves at most three coding jobs per UTC day across manual and scheduled runs and executes at most two issues concurrently.

The daily schedule runs at 14:23 UTC. It reports triage by default. After a successful single-issue hosted pilot and three independently selected tasks complete with credible verification, set the repository variable `AGENT_AUTOMATION` to `true` to enable scheduled coding. Remove it to return to triage.

## Selection and validation

- The deterministic shortlist uses reproduction and validation cues, severity labels, declared dependencies, and risk labels. An open PR referencing the issue or using its deterministic branch blocks duplicate dispatch. Labels `security`, `dependencies`, `agent:blocked`, and `agent:high-risk` block unattended execution. The AI report is advisory.
- An implementation job uses a fresh checkout and read-only GitHub permissions. Its scope is regular text files in the application, the test file, README, and the entry point. Codex can retry an empty or rejected patch once. Failed builds, tests, or reviews stop publication. Inspect the artifacts and logs before dispatching a revised task.
- A fresh verification runner applies the patch to the original base, checks its scope, compiles Python source, and runs `python -B test_app.py` without provider secrets or write access. A separate read-only Codex job reviews the proposed patch and test quality. Publication requires an approval verdict with no findings.
- A fresh publisher checks the issue, branch, and open PRs again, applies the verified patch, and pushes `agent/issue-N` before opening a draft. It refuses to overwrite a branch with different changes. If the push succeeds but PR creation fails, the same patch can reuse the existing branch. If `main` advances before publication, dispatch from the new base.
- GitHub may require a maintainer to select **Approve workflows to run** on a bot-created PR. The workflow already runs its independent verification before publishing. See [GitHub's token event rules](https://docs.github.com/en/actions/concepts/security/github_token#when-github_token-triggers-workflows).

## Evidence

Each workflow run retains its shortlist, coding-slot reservations, proposed patches, reviewer verdicts, job outcomes, and draft URLs. Use **Re-run all jobs** for a full replay so artifacts and the daily reservation correspond to one attempt. When reviewing the pilot, record candidate count, test/review failures, elapsed time, provider usage from its billing dashboard, and accepted PRs. The three-job budget measures admitted coding jobs. Review, advisory calls, and a Codex retry are additional model calls.
