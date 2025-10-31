# Communication Protocol

This document defines the communication protocol for agent-to-agent communication in recursive validation loops. It establishes standards for message formatting, communication flows, status signaling, and error handling.

## Protocol Overview

The recursive communication protocol enables structured interaction between:
- **Validation Orchestrator** (@validation-orchestrator): Coordinates validation workflow
- **Validation Specialists** (6 specialists): Execute validation checks
- **Main Agent** (@feature-implementer-main): Fixes validation failures

## Communication Patterns

### Pattern 1: Failure Notification

**Flow**: Specialist → Orchestrator → Main Agent

```
@specialist
  ↓ (detects failure)
@validation-orchestrator
  ↓ (formats failure report)
@feature-implementer-main
  ↓ (receives notification)
```

**Protocol**:
1. Specialist detects validation failure
2. Specialist reports failure to orchestrator with details
3. Orchestrator activates recursive-communicator skill
4. Orchestrator formats structured failure report
5. Orchestrator sends failure report to main agent
6. Orchestrator waits for main agent acknowledgment

### Pattern 2: Fix Request

**Flow**: Orchestrator ↔ Main Agent

```
@validation-orchestrator
  ↓ (requests fix)
@feature-implementer-main
  ↓ (fixes implementation)
  ↓ (signals completion)
@validation-orchestrator
  ↓ (acknowledges)
```

**Protocol**:
1. Orchestrator sends fix request with actionable items
2. Main agent acknowledges receipt
3. Main agent implements fixes
4. Main agent signals fix completion
5. Orchestrator confirms receipt and triggers re-validation

### Pattern 3: Re-validation Loop

**Flow**: Orchestrator → Specialist → Orchestrator

```
@validation-orchestrator
  ↓ (triggers re-check)
@specialist
  ↓ (re-runs validation)
  ↓ (reports result: PASS/FAIL)
@validation-orchestrator
  ↓ (if PASS: proceed)
  ↓ (if FAIL: repeat Pattern 1)
```

**Protocol**:
1. Orchestrator re-invokes specialist
2. Specialist re-runs validation checks
3. Specialist reports result (PASS/FAIL) to orchestrator
4. Orchestrator processes result:
   - **PASS**: Exit loop, proceed to next phase
   - **FAIL**: Increment iteration, return to Pattern 1

### Pattern 4: Escalation

**Flow**: Orchestrator → Main Orchestrator/User

```
@validation-orchestrator
  ↓ (detects unresolvable issue)
  ↓ (max iterations OR timeout)
@feature-implementer-main OR User
  ↓ (receives escalation)
  ↓ (makes decision)
```

**Protocol**:
1. Orchestrator detects escalation condition:
   - Max iterations exceeded (5)
   - Timeout (30 minutes)
   - Deadlock (no progress across iterations)
2. Orchestrator formats escalation report
3. Orchestrator sends escalation to main orchestrator or user
4. Orchestrator pauses validation workflow
5. Orchestrator awaits decision (manual fix, skip, abort, extend)

## Message Formatting Standards

### Message Structure

All messages between agents follow this structure:

```markdown
## [Message Type]

**Message ID**: [Type-IssueNumber-Iteration-Timestamp]
**From**: [Sender Agent]
**To**: [Recipient Agent]
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: [Critical / High / Medium / Low]

---

### [Section 1: Summary]
[Brief summary of message purpose]

### [Section 2: Details]
[Detailed information: failures, fixes, results, etc.]

### [Section 3: Actions Required]
[Actionable items for recipient]

### [Section 4: Expected Response]
[What sender expects from recipient]

---

**Sent by**: [Agent Name] ([Skill Name if applicable])
```

### Message Types

#### 1. Failure Report

```markdown
## Validation Failure Report

**Message ID**: VFR-{issue-number}-{specialist-name}-{iteration}
**From**: @validation-orchestrator
**To**: @feature-implementer-main
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: High

---

### Failure Summary
[Brief description of failures]

### Detailed Failures
[List of specific failures with file locations and errors]

### Suggested Fixes
[Specialist recommendations for resolving failures]

### Actions Required
[What main agent needs to do]

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
```

#### 2. Fix Request

```markdown
## Fix Request

**Message ID**: FIXREQ-{issue-number}-{iteration}
**From**: @validation-orchestrator
**To**: @feature-implementer-main
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: High

---

### Request Summary
Please fix the following validation failures for feature #{issue-number}.

### Failures to Fix
1. [Failure 1 with details]
2. [Failure 2 with details]
...

### Suggested Approach
[Recommendations for fixes]

### Expected Outcome
After fixes: All tests pass, coverage ≥80%

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Awaiting**: Fix completion signal
```

#### 3. Fix Completion Signal

```markdown
## Fix Completion

**Message ID**: FIXDONE-{issue-number}-{iteration}
**From**: @feature-implementer-main
**To**: @validation-orchestrator
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: High

---

### Completion Summary
Fixes completed for feature #{issue-number}, iteration {iteration}.

### Fixes Applied
1. [Description of fix 1]
2. [Description of fix 2]
...

### Files Modified
- [File path 1]
- [File path 2]
...

### Ready for Re-validation
Yes - please re-run {specialist-name}.

---

**Sent by**: Feature Implementer Main Agent
```

#### 4. Re-validation Trigger

```markdown
## Re-validation Trigger

**Message ID**: REVAL-{issue-number}-{specialist-name}-{iteration}
**From**: @validation-orchestrator
**To**: @{specialist-name}
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: High

---

### Re-validation Request
Please re-run validation checks for feature #{issue-number}.

### Iteration
Current: {iteration} / Max: 5

### Previous Failures
[List of failures from previous iteration]

### Fixes Applied
[Summary of fixes from main agent]

### Expected Outcome
- All previous failures resolved
- New status: PASS

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
```

#### 5. Re-validation Result

```markdown
## Re-validation Result

**Message ID**: REVALRES-{issue-number}-{specialist-name}-{iteration}
**From**: @{specialist-name}
**To**: @validation-orchestrator
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: High

---

### Result Summary
**Status**: [PASS / FAIL]

### Details
[For PASS]: All previous failures resolved.
[For FAIL]: [Count] failures remain.

### Failure Details (if FAIL)
[List of remaining failures]

### Next Action
[For PASS]: Proceed to next phase
[For FAIL]: Continue recursive loop (iteration {current+1}/5)

---

**Sent by**: {Specialist Name}
```

#### 6. Success Notification

```markdown
## Validation Success

**Message ID**: SUCCESS-{issue-number}-{specialist-name}-{final-iteration}
**From**: @validation-orchestrator
**To**: @feature-implementer-main
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: Medium

---

### Success Summary
Validation phase {phase-name} completed successfully after {iteration-count} iterations.

### Final Status
- All failures resolved
- Quality gates passed
- Total time: [HH:MM:SS]

### Next Phase
Proceeding to: {next-phase-name}

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
```

#### 7. Escalation Report

```markdown
## Escalation: Unresolvable Issue

**Message ID**: ESC-{issue-number}-{specialist-name}-{timestamp}
**From**: @validation-orchestrator
**To**: @feature-implementer-main / User
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Priority**: Critical

---

### Escalation Summary
**Reason**: [Max Iterations Exceeded / Timeout / Deadlock]
**Iterations**: {max-iterations} (all failed)
**Time**: [HH:MM:SS]

### Persistent Failures
[List of failures across all iterations]

### Iteration History
[Table of all iterations with failures and fixes]

### Recommended Actions
[Options for user: manual fix, skip, abort, extend]

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
**Awaiting**: User Decision
```

## Status Signaling

### Status Codes

| Status Code | Meaning | Used By |
|-------------|---------|---------|
| `PENDING` | Validation not started | Orchestrator |
| `IN_PROGRESS` | Validation currently running | Orchestrator, Specialist |
| `AWAITING_FIX` | Waiting for main agent fix | Orchestrator |
| `FIXING` | Main agent fixing issues | Main Agent |
| `RE_CHECKING` | Re-running validation | Specialist |
| `PASS` | Validation passed | Specialist |
| `FAIL` | Validation failed | Specialist |
| `ESCALATED` | Unresolvable, escalated | Orchestrator |
| `COMPLETED` | Validation workflow complete | Orchestrator |

### Status Transitions

```
PENDING → IN_PROGRESS → PASS → COMPLETED
                     ↓
                   FAIL → AWAITING_FIX → FIXING → RE_CHECKING → PASS
                                                              ↓
                                                            FAIL (repeat)
                                                              ↓
                                                          (after 5 iterations)
                                                              ↓
                                                          ESCALATED
```

### Status Messages

**Status Change Notification**:
```markdown
## Status Change

**Entity**: [Specialist Name / Orchestrator]
**Previous Status**: [Status Code]
**New Status**: [Status Code]
**Timestamp**: [YYYY-MM-DD HH:MM:SS]
**Reason**: [Brief explanation of status change]
```

## Timeout and Escalation Procedures

### Timeout Settings

| Operation | Timeout | Action on Timeout |
|-----------|---------|-------------------|
| Specialist Validation | 30 minutes | Send reminder, escalate after 5 min |
| Main Agent Fix | 30 minutes | Send reminder, escalate after 5 min |
| Re-validation | 30 minutes | Send reminder, escalate after 5 min |
| Total Iteration | 30 minutes | Escalate immediately |

### Timeout Protocol

**Step 1: Detect Timeout**
```markdown
IF elapsed_time > timeout_threshold:
  1. Log timeout event
  2. Record timeout details (operation, elapsed time, expected completion)
```

**Step 2: Send Reminder**
```markdown
## Timeout Reminder

**Message ID**: TIMEOUT-{issue-number}-{operation}-{timestamp}
**To**: [Agent with timeout]
**Elapsed**: [MM:SS]
**Timeout**: [Timeout threshold]

---

### Reminder
Operation [{operation}] has been running for {elapsed_time}.
Expected completion within {timeout_threshold}.

**Current Status**: [Status of operation]
**Action Required**: Complete operation or signal issue

**Escalation**: If no response within 5 minutes, will escalate to user.

---

**Sent by**: Validation Orchestrator (recursive-communicator skill)
```

**Step 3: Escalate (if no response)**
```markdown
IF no_response_after_reminder (5 minutes):
  1. Format escalation report
  2. Send to user/main orchestrator
  3. Pause validation workflow
  4. Await user decision
```

### Escalation Conditions

**Condition 1: Max Iterations Exceeded**
```markdown
IF iteration_count > max_iterations (5):
  Escalation Reason: "Max iterations exceeded"
  Action: Format escalation report, send to user
```

**Condition 2: Timeout**
```markdown
IF elapsed_time > timeout + reminder_window (35 minutes):
  Escalation Reason: "Timeout exceeded"
  Action: Format escalation report, send to user
```

**Condition 3: Deadlock**
```markdown
IF same_failures_across_3_iterations:
  Escalation Reason: "Deadlock - no progress"
  Action: Format escalation report, send to user
```

**Condition 4: Specialist Error**
```markdown
IF specialist_fails_unexpectedly (not validation failure, but error):
  Escalation Reason: "Specialist error"
  Action: Report to main orchestrator for debugging
```

## Error Handling

### Error Types

#### Type 1: Communication Error
```markdown
**Error**: Message not delivered
**Cause**: Agent unreachable, network issue, etc.
**Handling**:
1. Log error
2. Retry delivery (max 3 attempts)
3. If all retries fail: Escalate to main orchestrator
```

#### Type 2: Invalid Response
```markdown
**Error**: Agent response doesn't match expected format
**Cause**: Protocol violation, malformed message
**Handling**:
1. Log invalid response
2. Send protocol violation notice to agent
3. Request properly formatted response
4. If persists: Escalate
```

#### Type 3: Specialist Failure
```markdown
**Error**: Specialist fails to execute (not validation failure)
**Cause**: Bug in specialist, missing dependencies, etc.
**Handling**:
1. Log specialist error with stack trace
2. Attempt specialist re-invocation (1 retry)
3. If retry fails: Escalate to main orchestrator
```

#### Type 4: Main Agent Unresponsive
```markdown
**Error**: Main agent doesn't signal fix completion
**Cause**: Main agent stuck, crashed, or unable to fix
**Handling**:
1. Send timeout reminder
2. Wait 5 minutes
3. If no response: Escalate to user
```

### Error Message Format

```markdown
## Error Notification

**Error ID**: ERR-{issue-number}-{error-type}-{timestamp}
**Error Type**: [Communication / Invalid Response / Specialist Failure / Unresponsive]
**From**: [Agent that detected error]
**Context**: [Operation when error occurred]
**Timestamp**: [YYYY-MM-DD HH:MM:SS]

---

### Error Details
**Error Message**: [Full error message]
**Stack Trace**: [If applicable]
**Context**: [What was happening when error occurred]

### Recovery Actions Attempted
1. [Action 1]
2. [Action 2]
...

### Current Status
**Recovered**: [Yes / No]
**Next Action**: [If recovered: continue | If not: escalate]

---

**Sent by**: [Agent Name]
```

## Communication Logging

### Log Entry Format

```markdown
## Communication Log Entry

**Entry ID**: LOG-{issue-number}-{iteration}-{message-count}
**Timestamp**: [YYYY-MM-DD HH:MM:SS]

**Participants**:
- Sender: [Agent Name]
- Recipient: [Agent Name]

**Message Type**: [Failure Report / Fix Request / Fix Completion / etc.]
**Message ID**: [Full message ID]

**Summary**: [One-line summary of message content]

**Status Before**: [Status before this message]
**Status After**: [Status after this message]

**Iteration**: [Current/Max]
```

### Full Communication Log

```markdown
## Full Communication Log: Feature #{issue-number}

**Issue**: #{issue-number} - [Feature Name]
**Started**: [YYYY-MM-DD HH:MM:SS]
**Completed**: [YYYY-MM-DD HH:MM:SS]
**Total Duration**: [HH:MM:SS]
**Total Messages**: [Count]
**Total Iterations**: [Count]

---

### Chronological Message Log

**[Timestamp 1]** @specialist → @orchestrator: Failure detected
- Message ID: [ID]
- Summary: [Summary]

**[Timestamp 2]** @orchestrator → @main-agent: Failure report
- Message ID: VFR-{issue}-{specialist}-1
- Summary: [Summary]

**[Timestamp 3]** @main-agent → @orchestrator: Fix completion
- Message ID: FIXDONE-{issue}-1
- Summary: [Summary]

**[Timestamp 4]** @orchestrator → @specialist: Re-validation trigger
- Message ID: REVAL-{issue}-{specialist}-2
- Summary: [Summary]

**[Timestamp 5]** @specialist → @orchestrator: Re-validation result (PASS)
- Message ID: REVALRES-{issue}-{specialist}-2
- Summary: [Summary]

**[Timestamp 6]** @orchestrator → @main-agent: Success notification
- Message ID: SUCCESS-{issue}-{specialist}-2
- Summary: [Summary]

---

### Communication Statistics

**Total Messages**: 6
**Failure Reports**: 1
**Fix Requests**: 1
**Fix Completions**: 1
**Re-validation Triggers**: 1
**Re-validation Results**: 1
**Success Notifications**: 1

**Iterations**: 2 (1 initial + 1 retry)
**Outcome**: Success (all validations passed)
```

## Best Practices

### 1. Always Use Structured Messages
- Follow message templates exactly
- Include all required sections
- Use consistent formatting
- Provide message IDs for traceability

### 2. Clear Status Signaling
- Update status immediately when changes occur
- Use standard status codes
- Communicate status changes to all relevant parties
- Log all status transitions

### 3. Comprehensive Logging
- Log every message sent and received
- Include timestamps for all events
- Maintain chronological order
- Preserve full message content for audit

### 4. Proactive Timeout Management
- Monitor operation durations
- Send reminders before escalation
- Escalate gracefully when timeouts occur
- Provide clear timeout thresholds

### 5. Graceful Error Handling
- Detect errors immediately
- Attempt recovery before escalation
- Log all errors with full context
- Provide actionable error messages

### 6. Iteration Tracking
- Always include current/max iteration
- Document what changed between iterations
- Analyze patterns across iterations
- Enforce max iteration limits strictly

---

**Version**: 2.0.0
**Created**: 2025-10-29
**Updated**: 2025-10-29
