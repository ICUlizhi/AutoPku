---
name: autopku
description: Use when the user wants Codex to automate PKU coursework workflows with AutoPku, including syncing course notices, organizing assignments, writing notes from course materials, and optionally completing a user-selected homework with confirmation before submission.
---

# AutoPku for Codex

## Purpose

This is the Codex entrypoint for the AutoPku repository.

- Claude Code users should use [skill.md](skill.md).
- Codex users should use this file.
- Treat [skill.md](skill.md) as the upstream domain reference and `sub-skills/` as the detailed workflow library.

## Use When

- The user wants to pull current PKU course notices or assignments.
- The user wants per-course folders with summaries and downloaded files.
- The user wants help finishing a specific homework, but only after explicitly choosing the target assignment.
- The user wants notes distilled from PKU course slides or PDFs.

## Safety Rules

- Never auto-select the latest homework.
- Never auto-submit without explicit confirmation of the exact course and assignment.
- Do not echo the user's password back in summaries or logs.
- When the repository reference says `AskUserQuestion`, ask the user directly in chat instead of assuming a Codex-only tool exists.
- Treat Claude-specific config as reference material, not as a required Codex configuration step.

## Default Workflow

1. Read [skill.md](skill.md) first, then load only the relevant files under `sub-skills/` for the task at hand.
2. Ask the user for student ID and password only when the task truly requires portal access.
3. Check whether `pku3b` is installed. If not, install the correct release for the local machine instead of assuming the example URL is still current.
4. Use a TTY-safe login flow such as `expect` for `pku3b init`.
5. Fetch course and assignment data, normalize ANSI-heavy output, and save machine-readable intermediates under a task-specific work directory.
6. For notice-sync mode:
   - identify current-term courses
   - create per-course directories
   - download available materials
   - generate one per-course summary plus an aggregate summary
7. For homework mode:
   - list candidate assignments for the chosen course
   - require the user to confirm the exact assignment
   - parse the homework source
   - draft answers
   - render deliverables
   - submit only after explicit confirmation
8. For note-writing mode:
   - ask which course materials or lecture range to process
   - confirm desired detail level
   - extract the mathematical core from slides or PDFs
   - generate Markdown notes and render PDF only when requested or clearly useful
9. Verify generated files exist before reporting completion.

## Codex-Specific Guidance

- When parallel work helps, use Codex native subagents for bounded per-course or per-phase work instead of Claude Agent Team wording.
- When spawning Codex subagents, use model `gpt-5.3-codex` by default unless the user explicitly requests a different model.
- Prefer a dedicated work directory such as `./autopku-work/` or a user-specified path instead of hardcoding `test/`.
- If live command behavior differs from the repository notes, trust current command output and update working notes during execution.
- If the request is only to install or inspect the skill, stop after setup verification.
- Prefer `pku3b` from `PATH`, but if Homebrew is installed on Apple Silicon, explicitly check `/opt/homebrew/bin/pku3b` as a common location.
- The standard local config path on macOS is `~/Library/Application Support/org.sshwy.pku3b/cfg.toml`; confirm it exists before attempting login flows that assume stored credentials.
- If `pku3b s -d major show` or similar syllabus commands fail with a redirect or auth error, treat them as optional enrichment rather than a hard prerequisite and continue with assignment-driven course discovery from `pku3b a ls` or `pku3b a ls --all-term`.

## Verification

- Confirm required tools exist before execution.
- Confirm login succeeded before fetching data.
- Confirm expected files exist on disk after downloads or rendering.
- Before any submission step, confirm the selected assignment matches the user's explicit choice.

## Validation Notes

- Verified against a local install at `/opt/homebrew/bin/pku3b`.
- Verified that `pku3b a ls` can return live assignment data with an existing config.
- Observed that `pku3b s -d major show` may fail with `302 Found` on some accounts, so the workflow must not depend exclusively on that command.
