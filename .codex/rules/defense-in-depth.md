# Defense in Depth — 6 Guardrail Layers

Agents that modify code need enforcement, not suggestions. Six stacked layers, each catching a different error class.

## The 6 Layers

| Layer               | Mechanism                                                           | Timing               | What it catches                                                          |
| ------------------- | ------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------------ |
| 1. Hook preventivi  | `bash.py` exit 2, `supply-chain-guard.py`, `lockfile-edit-guard.py` | PreToolUse           | Dangerous commands, supply chain attacks, lockfile corruption            |
| 2. TDD              | rule `tdd.md` — tests fail before implementation                    | During work          | Logic errors, missing edge cases                                         |
| 3. Security scan    | `/security-verify scan` — rule `security-gate.md`                   | Before commit        | CVEs, secrets, OWASP violations                                          |
| 4. Companion review | `/review gate` → Codex/Gemini                                       | Post-implementation  | Design errors, subtle bugs — cross-model catches what self-review misses |
| 5. CI               | Forgejo workflows: lint, typecheck, test suite                      | Post-push            | Integration failures, regressions                                        |
| 6. Human gate       | ExitPlanMode, HARD STOP in `/implementation`, confirm in `/deploy`  | Irreversible actions | Intent mismatch, scope creep                                             |

## The Key Design Choice

Enforcement is in **code** (Python hooks, exit codes), not in **prompts**.

- "Don't run `rm -rf`" in a prompt = suggestion (model can ignore)
- `exit 2` in `bash.py` when pattern matches = block (cannot be bypassed)

The companion rule ("never fall back to Claude's own analysis") exists for the same reason: self-review has confirmation bias. Codex and Gemini have different training, different failure modes, different blind spots.

## When a Layer Fails

A mistake that reaches production has defeated all 6 layers. Investigate which layer should have caught it and strengthen that layer, not just the symptom.

Example: if a bad commit message slips through → strengthen Layer 3 (add semantic validation of commit messages to the hook).

## Scope

This applies to all code-modifying operations. For read-only analysis or conversational tasks, layers 2-6 are not relevant. Layer 1 (hooks) is always active.
