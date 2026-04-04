---
name: autopku
description: Use when the user wants Codex to automate PKU coursework workflows with AutoPku, including syncing course notices, organizing assignments, and optionally completing a user-selected homework with confirmation before submission.
---

# AutoPku for Codex

## Purpose

This is the Codex entrypoint for the AutoPku project.

- Claude Code users should use the repository root `skill.md`.
- Codex users should use this file.
- If this skill was installed standalone, use [references/upstream-skill.md](references/upstream-skill.md) as the bundled upstream reference.

## Use When

- The user wants to pull current PKU course notices or assignments.
- The user wants per-course folders with summaries and downloaded files.
- The user wants help finishing a specific homework, but only after explicitly choosing the target assignment.

## Safety Rules

- Never auto-select the latest homework.
- Never auto-submit without explicit confirmation of the exact course and assignment.
- Do not echo the user's password back in summaries or logs.
- Treat upstream Claude-specific config as reference material, not as a required Codex configuration step.

## Default Workflow

1. Read the bundled reference [references/upstream-skill.md](references/upstream-skill.md). If the checked-out repository root `skill.md` is also available, prefer the newer copy as domain guidance for PKU-specific commands, parsing quirks, and pitfalls.
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
8. Verify generated files exist before reporting completion.

## Codex-Specific Guidance

- When parallel work helps, use Codex native subagents for bounded per-course or per-phase work instead of relying on Claude Agent Team wording.
- Prefer a dedicated work directory such as `./autopku-work/` or a user-specified path instead of hardcoding `test/`.
- If live command behavior differs from the repository notes, trust current command output and update working notes during execution.
- If the request is only to install or inspect the skill, stop after setup verification.

## Verification

- Confirm required tools exist before execution.
- Confirm login succeeded before fetching data.
- Confirm expected files exist on disk after downloads or rendering.
- Before any submission step, confirm the selected assignment matches the user's explicit choice.
