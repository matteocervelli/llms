---
name: message-templates
description: 'TODO: Brief description of what the Skill does and when to use it'
---

# Message Templates

Pre-defined message templates for agent-to-agent communication in recursive validation loops. Use these templates to ensure consistent, structured communication.

## Template 1: Validation Failure Report

Use when a validation specialist detects failures and needs to notify the main agent.

```markdown
## Validation Failure Report

**Report ID**: VFR-{issue-number}-{specialist-name}-{iteration}
**Generated**: {YYYY-MM-DD HH:MM:SS}
**Issue**: #{issue-number} - {Feature Name}
**Specialist**: {Specialist Name}
**Phase**: {Validation Phase Name}
**Iteration**: {current} / 5

---

### Failure Summary

**Status**: ❌ FAILED
**Failure Type**: {Test Failures / Quality Issues / Security Vulnerabilities / E2E Failures}
**Severity**: {Critical / High / Medium / Low}
**Total Failures**: {count}
**Impact**: Blocks progression to {Next Phase}

---

### Detailed Failures

#### Failure 1: {Test/Check Name}
- **File**: {file-path}
- **Line**: {line-number}
- **Error Type**: {AssertionError / TypeError / SecurityError / etc.}
- **Error Message**:
  ```
  {full-error-message-from-specialist}
  ```
- **Context**: {additional-context-about-the-failure}

#### Failure 2: {Test/Check Name}
- **File**: {file-path}
- **Line**: {line-number}
- **Error Type**: {error-type}
- **Error Message**:
  ```
  {full-error-message}
  ```
- **Context**: {additional-context}

{... repeat for additional failures ...}

---

### Suggested Fixes

#### Fix for Failure 1
**Recommendation**: {specialist-suggestion-for-fixing-issue}
**Approach**: {specific-steps-or-code-changes-needed}
**Priority**: {Critical / High / Medium / Low}
**Estimated Time**: {time-estimate}

#### Fix for Failure 2
**Recommendation**: {specialist-suggestion}
**Approach**: {specific-steps}
**Priority**: {priority-level}
**Estimated Time**: {time-estimate}

{... repeat for additional fixes ...}

---

### Required Actions

**Main Agent (@feature-implementer-main):**
1. Review failure details above
2. Implement suggested fixes (or alternative approach)
3. Verify fixes locally (if possible)
4. Signal completion to validation orchestrator
5. Await re-validation

**Expected Timeline**: {estimated-time-to-fix}
**Escalation**: If fixes cannot be completed, escalate to user

---

### Re-validation Plan

**After Fix Completion**:
1. Validation orchestrator will re-invoke {Specialist Name}
2. Specialist will re-run {Tests/Checks}
3. **IF pass**: Proceed to {Next Phase}
4. **IF fail**: Iteration {current+1} / 5
5. **IF max iterations exceeded**: Escalate to user intervention

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Awaiting**: Main Agent Fix Completion
**Timeout**: 30 minutes (reminder at 25 minutes)
```

---

## Template 2: Fix Request

Use when requesting the main agent to fix specific validation issues.

```markdown
## Fix Request

**Message ID**: FIXREQ-{issue-number}-{iteration}
**From**: @validation-orchestrator
**To**: @feature-implementer-main
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: High
**Iteration**: {current} / 5

---

### Request Summary

Please fix the following validation failures for feature #{issue-number}.

**Validation Phase**: {Phase Name}
**Specialist**: {Specialist Name}
**Total Failures**: {count}

---

### Failures to Fix

1. **{Failure 1 Name}**
   - File: {file-path}
   - Line: {line-number}
   - Error: {error-message}
   - Suggested Fix: {fix-suggestion}

2. **{Failure 2 Name}**
   - File: {file-path}
   - Line: {line-number}
   - Error: {error-message}
   - Suggested Fix: {fix-suggestion}

{... repeat for additional failures ...}

---

### Suggested Approach

**Recommended Fix Strategy**:
1. {Step 1 of fixing process}
2. {Step 2 of fixing process}
3. {Step 3 of fixing process}

**Alternative Approaches**:
- {Alternative 1}
- {Alternative 2}

---

### Expected Outcome

**After Fixes**:
- All {count} failures resolved
- {Specific quality gate passed, e.g., "All tests pass", "Coverage ≥80%", "Zero security vulnerabilities"}
- Ready for re-validation

**Verification**:
- Main agent can optionally verify fixes locally before signaling completion
- Validation orchestrator will re-run {Specialist Name} for official verification

---

### Timeline

**Expected Fix Time**: {estimated-time}
**Timeout**: 30 minutes
**Reminder**: Will be sent at 25 minutes if no completion signal received
**Escalation**: Will escalate to user if timeout exceeded

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Awaiting**: Fix Completion Signal (FIXDONE-{issue-number}-{iteration})
```

---

## Template 3: Fix Completion Signal

Use when the main agent has completed fixes and is ready for re-validation.

```markdown
## Fix Completion

**Message ID**: FIXDONE-{issue-number}-{iteration}
**From**: @feature-implementer-main
**To**: @validation-orchestrator
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: High
**Iteration**: {current} / 5

---

### Completion Summary

Fixes completed for feature #{issue-number}, iteration {iteration}.

**Validation Phase**: {Phase Name}
**Specialist to Re-run**: {Specialist Name}
**Fix Duration**: {HH:MM:SS from failure report to completion}

---

### Fixes Applied

1. **Fix for {Failure 1}**
   - **Description**: {what-was-fixed}
   - **Approach**: {how-it-was-fixed}
   - **Files Modified**: {file-paths}
   - **Changes**: {brief-summary-of-changes}

2. **Fix for {Failure 2}**
   - **Description**: {what-was-fixed}
   - **Approach**: {how-it-was-fixed}
   - **Files Modified**: {file-paths}
   - **Changes**: {brief-summary-of-changes}

{... repeat for additional fixes ...}

---

### Files Modified

- {file-path-1}
- {file-path-2}
- {file-path-3}
{... list all modified files ...}

---

### Local Verification (Optional)

**Verification Performed**: {Yes / No}
**If Yes**:
- Tests run locally: {Yes / No}
- Result: {Pass / Fail / Partial}
- Notes: {any-notes-about-local-verification}

**If No**:
- Reason: {why-not-verified-locally}

---

### Ready for Re-validation

**Status**: Ready
**Request**: Please re-run {specialist-name} for official validation.

**Expected Outcome**:
- All {count} failures should be resolved
- {Specific quality gate should pass}

---

**Sent by**: Feature Implementer Main Agent
**Next Action**: Awaiting re-validation trigger from orchestrator
```

---

## Template 4: Re-validation Trigger

Use when triggering a specialist to re-run validation after fixes.

```markdown
## Re-validation Trigger

**Message ID**: REVAL-{issue-number}-{specialist-name}-{iteration}
**From**: @validation-orchestrator
**To**: @{specialist-name}
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: High
**Iteration**: {current} / 5

---

### Re-validation Request

Please re-run validation checks for feature #{issue-number}.

**Validation Phase**: {Phase Name}
**Reason**: Main agent has completed fixes for failures from iteration {previous-iteration}

---

### Iteration Information

**Current Iteration**: {current} / 5
**Previous Iteration**: {previous}
**Previous Status**: FAILED ({count} failures)
**Expected Status**: PASS

---

### Previous Failures

The following failures were reported in iteration {previous-iteration}:

1. {Failure 1 name} - {brief-description}
2. {Failure 2 name} - {brief-description}
{... list all previous failures ...}

**Total Previous Failures**: {count}

---

### Fixes Applied by Main Agent

The main agent has applied the following fixes:

1. {Fix 1 summary}
2. {Fix 2 summary}
{... list all fixes ...}

---

### Re-validation Instructions

**Please**:
1. Re-run all validation checks (same as initial validation)
2. Verify all previous failures are resolved
3. Check for any new failures introduced by fixes
4. Report result: PASS or FAIL

**Expected Outcome**:
- ✅ **PASS**: All previous failures resolved, no new failures
- ❌ **FAIL**: Some failures persist or new failures introduced

---

### Result Reporting

**Please Report**:
- Overall status (PASS / FAIL)
- Detailed results (for FAIL: list of remaining/new failures)
- Comparison to previous iteration (improvements, regressions)

**Report Format**: Use Re-validation Result template (REVALRES-{issue-number}-{specialist-name}-{iteration})

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Awaiting**: Re-validation Result
**Timeout**: 30 minutes
```

---

## Template 5: Re-validation Result (PASS)

Use when re-validation succeeds and all failures are resolved.

```markdown
## Re-validation Result: PASS

**Message ID**: REVALRES-{issue-number}-{specialist-name}-{iteration}
**From**: @{specialist-name}
**To**: @validation-orchestrator
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: High
**Iteration**: {current} / 5

---

### Result Summary

**Status**: ✅ PASS
**Previous Failures**: {count} failures
**Current Failures**: 0 failures
**Resolution**: All issues successfully fixed by main agent

---

### Validation Results

**{Validation Type} Results**:
- Total Tests/Checks: {count}
- Passed: {count}
- Failed: 0
- {Additional metric, e.g., "Coverage: XX.X%"}

**Quality Gate**: ✅ PASSED

---

### Comparison to Previous Iteration

**Iteration {previous-iteration} (Previous)**:
- Status: FAILED
- Failures: {count}
- {metric}: {value}

**Iteration {current} (Current)**:
- Status: ✅ PASS
- Failures: 0
- {metric}: {value}

**Improvement**:
- All {count} failures resolved
- {metric} improved from {old-value} to {new-value}

---

### Previous Failures (Now Resolved)

1. ✅ {Failure 1 name} - RESOLVED
2. ✅ {Failure 2 name} - RESOLVED
{... list all previous failures, now resolved ...}

---

### New Failures

**None** - No new failures introduced by fixes.

---

### Next Action

**Recommendation**: Proceed to {Next Phase}
**Validation Phase {Phase Name}**: Complete
**Overall Validation Status**: In Progress ({current-phase} of {total-phases} complete)

---

**Sent by**: {Specialist Name}
**Validation Duration**: {HH:MM:SS for this iteration}
**Total Iterations**: {current} / 5 (Success on iteration {current})
```

---

## Template 6: Re-validation Result (FAIL)

Use when re-validation fails and some failures persist or new failures are introduced.

```markdown
## Re-validation Result: FAIL

**Message ID**: REVALRES-{issue-number}-{specialist-name}-{iteration}
**From**: @{specialist-name}
**To**: @validation-orchestrator
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: High
**Iteration**: {current} / 5

---

### Result Summary

**Status**: ❌ FAIL
**Previous Failures**: {count-previous} failures
**Current Failures**: {count-current} failures
**Progress**: {count-resolved} resolved, {count-persisting} persisting, {count-new} new

---

### Validation Results

**{Validation Type} Results**:
- Total Tests/Checks: {count}
- Passed: {count-passed}
- Failed: {count-failed}
- {Additional metric, e.g., "Coverage: XX.X% (target: ≥80%)"}

**Quality Gate**: ❌ FAILED

---

### Comparison to Previous Iteration

**Iteration {previous-iteration} (Previous)**:
- Status: FAILED
- Failures: {count-previous}
- {metric}: {value-previous}

**Iteration {current} (Current)**:
- Status: ❌ FAIL
- Failures: {count-current}
- {metric}: {value-current}

**Analysis**:
- Resolved: {count-resolved} failures fixed
- Persisting: {count-persisting} failures still present
- New: {count-new} new failures introduced
- Overall Progress: {improved / regressed / no change}

---

### Resolved Failures (From Previous Iteration)

1. ✅ {Failure 1 name} - RESOLVED in this iteration
2. ✅ {Failure 2 name} - RESOLVED in this iteration
{... list resolved failures ...}

---

### Persisting Failures (Still Failing)

1. ❌ {Failure 1 name} - Still failing
   - **File**: {file-path}
   - **Error**: {error-message}
   - **Iterations Failed**: {previous-iteration}, {current}
   - **Note**: {why-this-failure-persists}

2. ❌ {Failure 2 name} - Still failing
   - **File**: {file-path}
   - **Error**: {error-message}
   - **Iterations Failed**: {list-of-iterations}
   - **Note**: {why-this-failure-persists}

{... list persisting failures ...}

---

### New Failures (Introduced in This Iteration)

1. 🆕 {New Failure 1 name}
   - **File**: {file-path}
   - **Line**: {line-number}
   - **Error**: {error-message}
   - **Likely Cause**: {possible-cause, e.g., "Introduced by fix for Failure X"}

2. 🆕 {New Failure 2 name}
   - **File**: {file-path}
   - **Line**: {line-number}
   - **Error**: {error-message}
   - **Likely Cause**: {possible-cause}

{... list new failures ...}

---

### Suggested Fixes for Remaining Failures

#### Persisting Failure 1
**Recommendation**: {updated-suggestion-based-on-iteration-history}
**Approach**: {specific-steps}
**Priority**: {priority}

#### New Failure 1
**Recommendation**: {suggestion-for-new-failure}
**Approach**: {specific-steps}
**Priority**: {priority}

{... repeat for all remaining failures ...}

---

### Next Action

**Decision**:
IF iteration < 5:
  ✅ Continue recursive loop
  ✅ Return to main agent for additional fixes
  ✅ Next iteration: {current+1} / 5
ELSE (iteration >= 5):
  ⛔ Max iterations exceeded
  ⛔ Escalate to user intervention

**Current Iteration**: {current} / 5
**Action**: {Continue Loop / Escalate}

---

**Sent by**: {Specialist Name}
**Validation Duration**: {HH:MM:SS for this iteration}
**Total Time Across Iterations**: {HH:MM:SS cumulative}
```

---

## Template 7: Success Notification

Use when a validation phase completes successfully after recursive loop.

```markdown
## Validation Success

**Message ID**: SUCCESS-{issue-number}-{specialist-name}-{final-iteration}
**From**: @validation-orchestrator
**To**: @feature-implementer-main
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: Medium
**Iteration**: {final-iteration} / 5

---

### Success Summary

✅ Validation phase **{Phase Name}** completed successfully.

**Specialist**: {Specialist Name}
**Final Status**: PASS
**Total Iterations**: {iteration-count} / 5
**Total Time**: {HH:MM:SS across all iterations}

---

### Iteration History

| Iteration | Status | Failures | Action Taken |
|-----------|--------|----------|--------------|
| 1 | FAIL | {count} | Main agent fixed → Re-validation |
| 2 | FAIL | {count} | Main agent fixed → Re-validation |
| ... | ... | ... | ... |
| {final} | ✅ PASS | 0 | Success - Exit loop |

**Total Recursive Fix Cycles**: {count}

---

### Final Validation Results

**{Validation Type}**:
- All tests/checks: PASSED
- {Specific metric}: {value}
- Quality gate: ✅ PASSED

---

### Acknowledgment

Thank you for addressing the validation failures through {iteration-count} iteration(s).
All quality standards for {Phase Name} are now met.

---

### Next Phase

**Current Phase**: {Phase Name} - ✅ COMPLETE
**Next Phase**: {Next Phase Name}
**Overall Progress**: {X} of {total} validation phases complete

**Action**: Proceeding to {Next Phase Name}.

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Validation Phase**: Complete
```

---

## Template 8: Escalation Report

Use when max iterations are exceeded or timeout occurs, requiring user intervention.

```markdown
## Escalation: Unresolvable Validation Issue

**Escalation ID**: ESC-{issue-number}-{specialist-name}-{timestamp}
**Generated**: {YYYY-MM-DD HH:MM:SS}
**Issue**: #{issue-number} - {Feature Name}
**Specialist**: {Specialist Name}
**Phase**: {Validation Phase}
**Escalation Reason**: {Max Iterations Exceeded / Timeout / Deadlock / Other}

---

### Escalation Summary

**Status**: ⛔ UNRESOLVABLE (Requires User Intervention)
**Total Iterations**: 5 / 5 (Max exceeded)
**Total Time**: {HH:MM:SS across all iterations}
**Persistent Failures**: {count}

---

### Iteration History

| Iteration | Failures | Fixes Applied | Result | Duration |
|-----------|----------|---------------|--------|----------|
| 1 | {count} | {fix-summary} | FAIL | {MM:SS} |
| 2 | {count} | {fix-summary} | FAIL | {MM:SS} |
| 3 | {count} | {fix-summary} | FAIL | {MM:SS} |
| 4 | {count} | {fix-summary} | FAIL | {MM:SS} |
| 5 | {count} | {fix-summary} | FAIL | {MM:SS} |

**Pattern Analysis**: {analysis-of-why-failures-persist-across-iterations}

---

### Persistent Failures

#### Failure 1: {Failure Name}
- **File**: {file-path}
- **Line**: {line-number}
- **Error**: {error-message}
- **Iterations Failed**: 1, 2, 3, 4, 5 (All)
- **Fixes Attempted**:
  - Iteration 1: {fix-1-description}
  - Iteration 2: {fix-2-description}
  - Iteration 3: {fix-3-description}
  - Iteration 4: {fix-4-description}
  - Iteration 5: {fix-5-description}
- **Why Unresolved**: {detailed-analysis-of-why-this-failure-persists}
- **Root Cause Hypothesis**: {hypothesis-about-root-cause}

#### Failure 2: {Failure Name}
- **File**: {file-path}
- **Line**: {line-number}
- **Error**: {error-message}
- **Iterations Failed**: {list-of-iterations}
- **Fixes Attempted**: {list-of-fixes}
- **Why Unresolved**: {analysis}
- **Root Cause Hypothesis**: {hypothesis}

{... repeat for all persistent failures ...}

---

### Recommended Actions

#### Option 1: User Manual Fix ✋
**Description**: User reviews failures and provides manual fix
**Process**:
1. User analyzes persistent failures and root causes
2. User implements fix manually
3. User signals validation orchestrator to re-run validation
4. Validation orchestrator re-invokes {Specialist Name}
**Risk**: Requires user expertise and time
**Success Likelihood**: High (if user has technical expertise)

#### Option 2: Skip Validation (Proceed with Known Issues) ⚠️
**Description**: Mark validation as "failed but proceeding"
**Process**:
1. Document all unresolved failures
2. Mark feature as "deployed with known issues"
3. Continue to deployment phase
4. Create follow-up tasks to address failures
**Risk**: Deploy with validation failures - may cause bugs in production
**Success Likelihood**: N/A (bypasses validation)

#### Option 3: Abort Feature Implementation ⛔
**Description**: Stop implementation and return feature to design phase
**Process**:
1. Halt validation workflow
2. Mark feature as "implementation failed"
3. Return to Phase 2 (Design) for re-evaluation
4. Redesign architecture to address validation issues
**Risk**: Wasted effort on current implementation
**Success Likelihood**: High (after redesign)

#### Option 4: Extend Max Iterations (Retry) 🔄
**Description**: Allow additional iterations beyond max (5)
**Process**:
1. User grants extension (e.g., 3 more iterations → 8 total)
2. Validation orchestrator continues recursive loop
3. Monitor for progress or continued stagnation
**Risk**: Potentially infinite loop if issues are truly unresolvable
**Success Likelihood**: Low (if 5 iterations already failed)

---

### Recommendation

**Based on failure analysis, we recommend**: {Option X}

**Rationale**: {explanation-of-why-this-option-is-recommended}

---

### User Decision Required

**Please select one of the above options**:
- [ ] Option 1: User Manual Fix
- [ ] Option 2: Skip Validation
- [ ] Option 3: Abort Feature
- [ ] Option 4: Extend Max Iterations

**After Decision**:
- Validation orchestrator will execute selected option
- Validation workflow will resume or terminate based on decision

---

**Escalated To**: User / Main Orchestrator
**Awaiting Decision**: Yes
**Validation Workflow**: ⏸️ PAUSED
**Timeout**: None (awaiting user intervention)

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Escalation Level**: Critical
```

---

## Template 9: Timeout Reminder

Use when an operation is approaching timeout.

```markdown
## Timeout Reminder

**Message ID**: TIMEOUT-{issue-number}-{operation}-{timestamp}
**To**: {Agent with approaching timeout}
**From**: @validation-orchestrator
**Timestamp**: {YYYY-MM-DD HH:MM:SS}
**Priority**: High

---

### Reminder

Operation **{operation-name}** has been running for **{elapsed-time}**.

**Timeout Threshold**: {timeout-threshold}
**Time Remaining**: {remaining-time}
**Escalation Time**: {time-until-escalation}

---

### Current Status

**Operation**: {operation-name}
**Started**: {start-timestamp}
**Elapsed**: {HH:MM:SS}
**Expected Completion**: Within {timeout-threshold}

---

### Action Required

Please complete operation **{operation-name}** or signal if unable to complete.

**If Completed**: Send completion signal ({completion-message-id})
**If Unable to Complete**: Signal issue/blocker to validation orchestrator
**If No Response**: Will escalate to user in {time-until-escalation}

---

### Next Steps

**Within {time-until-escalation}**:
- [ ] Complete operation and signal
- [ ] OR report issue preventing completion

**After {time-until-escalation} without response**:
- Escalate to user intervention
- Pause validation workflow
- Await user decision

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Reminder Level**: Warning (Escalation pending)
```

---

## Template Usage Guidelines

### When to Use Each Template

| Template | Use Case |
|----------|----------|
| **Failure Report** | Specialist detects validation failures (first iteration) |
| **Fix Request** | Requesting main agent to fix specific issues |
| **Fix Completion** | Main agent signals fixes are complete |
| **Re-validation Trigger** | Triggering specialist to re-check after fixes |
| **Re-validation Result (PASS)** | Re-validation succeeds, exit loop |
| **Re-validation Result (FAIL)** | Re-validation fails, continue loop |
| **Success Notification** | Validation phase completes successfully |
| **Escalation Report** | Max iterations exceeded or unresolvable issue |
| **Timeout Reminder** | Operation approaching timeout threshold |

### Template Customization

- Replace all `{placeholders}` with actual values
- Maintain all section headers (marked with `###`)
- Keep markdown formatting consistent
- Include all required fields (Report ID, timestamps, etc.)
- Add additional failures/fixes/details as needed
- Preserve message structure for consistency

### Message ID Conventions

- **VFR**: Validation Failure Report
- **FIXREQ**: Fix Request
- **FIXDONE**: Fix Completion
- **REVAL**: Re-validation Trigger
- **REVALRES**: Re-validation Result
- **SUCCESS**: Success Notification
- **ESC**: Escalation Report
- **TIMEOUT**: Timeout Reminder

---

**Version**: 2.0.0
**Created**: 2025-10-29
**Updated**: 2025-10-29
