# ADR-007: Weekly Documentation Update Automation

**Status**: Accepted
**Date**: 2025-10-26
**Deciders**: Matteo Cervelli
**Context**: [Issue #7](https://github.com/matteocervelli/llms/issues/7)

---

## Context

The LLM Configuration Management System includes a documentation fetcher tool that downloads and tracks documentation from LLM providers (Anthropic, OpenAI, etc.). To keep this documentation up-to-date without manual intervention, we need an automated mechanism for periodic updates.

### Requirements

1. **Automated Updates**: Documentation should update automatically on a regular schedule
2. **Error Handling**: Failed updates should be logged and optionally reported
3. **Logging**: Comprehensive logs for troubleshooting and audit
4. **Minimal Maintenance**: System should run reliably with minimal user intervention
5. **Flexibility**: Users should be able to enable, disable, and customize the schedule
6. **Security**: No hardcoded credentials, proper file permissions
7. **Performance**: Efficient execution, no resource waste

### Constraints

- **Platform**: macOS/Linux development environments
- **User Level**: Single-user installations (not system-wide services)
- **Dependencies**: Should leverage existing doc_fetcher tool
- **Simplicity**: Prefer standard Unix tools over complex frameworks

---

## Decision

Implement a **cron-based automation system** with a bash wrapper script that:

1. Provides logging, error handling, and email notifications
2. Wraps the existing `doc_fetcher update` command
3. Runs on a weekly schedule (Sundays at 2 AM)
4. Rotates logs automatically (30-day retention)
5. Supports optional email notifications on errors

### Components

**1. Bash Wrapper Script** (`scripts/update_docs.sh`)
- Environment validation (Python version, dependencies, directory)
- Log rotation (deletes logs older than 30 days)
- Optional email notifications via `mail` command
- Proper exit codes for cron monitoring
- Comprehensive error handling and logging

**2. Log Management**
- Timestamped log files: `logs/doc_fetcher/update_YYYYMMDD_HHMMSS.log`
- Cron output log: `logs/doc_fetcher/cron.log`
- Automatic rotation after 30 days
- File permissions: 640 (owner read/write, group read)

**3. Cron Job Template**
```bash
# Update LLM documentation weekly (Sundays at 2 AM)
0 2 * * 0 cd ~/.claude/llms && ./scripts/update_docs.sh >> logs/doc_fetcher/cron.log 2>&1
```

**4. Email Notifications** (Optional)
- Enabled via `DOC_UPDATER_EMAIL` environment variable
- Uses standard `mail` command (mailutils package)
- Only sends on errors, not on success

---

## Rationale

### Why Cron?

**Advantages**:
- **Universal**: Available on all macOS/Linux systems
- **Simple**: No complex setup, single line in crontab
- **Reliable**: Proven technology with decades of production use
- **Flexible**: Easy to enable, disable, or change schedule
- **Standard**: Well-documented, widely understood
- **User-level**: Runs as current user, no sudo required

**Alternatives Considered**:

1. **systemd timers** (Linux only)
   - ❌ Not available on macOS (primary platform)
   - ✅ More modern, better logging
   - Decision: Rejected due to macOS incompatibility

2. **launchd** (macOS only)
   - ❌ More complex setup (plist files)
   - ❌ Not portable to Linux
   - ✅ Native macOS integration
   - Decision: Rejected for complexity and portability

3. **Python scheduler** (APScheduler, Celery)
   - ❌ Adds significant dependencies
   - ❌ Requires background process management
   - ❌ More complex error handling
   - ✅ Cross-platform, programmatic control
   - Decision: Rejected for added complexity

4. **GitHub Actions** (CI/CD)
   - ❌ Requires pushing to GitHub
   - ❌ Not suitable for local-first workflow
   - ✅ No local setup required
   - Decision: Rejected for local-first architecture

### Why Bash Wrapper?

The bash wrapper provides:

1. **Environment Validation**: Ensures Python, dependencies, and project structure are correct
2. **Logging**: Structured, timestamped logs with rotation
3. **Error Handling**: Graceful failures with informative messages
4. **Email Notifications**: Optional alerts on errors
5. **Exit Codes**: Proper codes for cron monitoring
6. **Path Safety**: Validates running from correct directory

**Alternative**: Direct cron call to Python
```bash
# Direct approach (not chosen)
0 2 * * 0 cd ~/.claude/llms && python -m src.tools.doc_fetcher update
```

**Issues with direct approach**:
- No structured logging
- No environment validation
- No error notifications
- No log rotation
- Poor troubleshooting experience

### Why Weekly Schedule?

**Rationale**:
- **Balance**: Frequent enough for timely updates, infrequent enough to respect provider resources
- **Sunday 2 AM**: Minimal user disruption, low provider traffic
- **Typical Update Frequency**: Documentation typically updates weekly or less

**Alternatives**:
- Daily: Excessive, wastes resources, rarely needed
- Monthly: Too infrequent, documentation may be outdated
- Real-time: Complex, requires webhooks/polling, overkill

---

## Security Considerations

### File Permissions

- **Script**: `chmod 750` (owner execute, group read, no world access)
- **Logs**: `chmod 640` (owner read/write, group read, no world access)
- **Log Directory**: `chmod 750` (owner full, group read/execute, no world access)

### Credential Management

- **Email Credentials**: Via `DOC_UPDATER_EMAIL` environment variable only
- **No Hardcoding**: Script contains no hardcoded credentials or sensitive data
- **Mail Configuration**: Uses system mail configuration (`~/.mailrc`, `/etc/mail.rc`)

### Path Validation

- Script validates it's running from correct directory (`~/.claude/llms`)
- Prevents execution from arbitrary locations
- Uses absolute paths for all file operations

### Input Sanitization

- No user input accepted (runs autonomously)
- Configuration files (provider YAML) already validated by doc_fetcher
- Log filenames use timestamp (no user-controlled values)

---

## Performance Characteristics

### Execution Time

- **Typical**: 30-60 seconds (22 documents @ 2-3s each with rate limiting)
- **Maximum**: < 5 minutes (includes rate limiting, network delays)
- **Empty Run**: < 5 seconds (manifest check only)

### Resource Usage

- **CPU**: Minimal (< 5% during execution)
- **Memory**: ~50-100 MB (Python process)
- **Disk I/O**: Minimal (small markdown files)
- **Network**: Respectful (rate limited @ 1 req/sec)

### Disk Space

- **Log Files**: ~10 KB per run
- **30-Day Retention**: ~300 KB total (assuming weekly runs)
- **Documentation**: ~500 KB total (22 markdown files)

### Network Traffic

- **Per Update**: 0-500 KB (depending on changes)
- **Weekly**: Typically 50-200 KB (only changed documents)
- **Rate Limiting**: 1 request/second (respects provider ToS)

---

## Monitoring & Observability

### Logs

**Detailed Logs** (`logs/doc_fetcher/update_*.log`):
- Timestamped entries (ISO 8601)
- Log levels: INFO, WARN, ERROR, SUCCESS
- Environment validation results
- Per-document fetch results
- Execution duration and exit code

**Cron Output** (`logs/doc_fetcher/cron.log`):
- Stdout/stderr from cron execution
- Useful for debugging cron issues
- Appends on each run

### Exit Codes

- `0`: Success (all documents updated or unchanged)
- `1`: Partial failure (some documents failed, see logs)
- `2`: Fatal error (environment issue, see logs)

### Email Notifications

- **Trigger**: Exit code != 0 (errors only)
- **Subject**: `[ERROR] Documentation Update Failed`
- **Body**: Error summary + log file path
- **Frequency**: Once per failed run

---

## Alternatives & Future Improvements

### Considered But Not Implemented

1. **Web Dashboard**: Overkill for single-user tool
2. **Slack/Discord Notifications**: More dependencies, setup complexity
3. **Real-time Updates**: Webhooks not available from providers
4. **Database Logging**: Unnecessary for current scale

### Future Enhancements

1. **Metrics Collection**: Track update frequency, success rates, document changes
2. **Health Checks**: External monitoring (e.g., healthchecks.io)
3. **Rate Limit Auto-tuning**: Adjust based on provider response times
4. **Parallel Fetching**: Speed up multi-provider updates
5. **GUI Configuration**: macOS app for non-technical users
6. **Cloud Backup**: Sync documentation to S3/Cloud Storage

---

## Testing Strategy

### Manual Testing Checklist

- [x] Script runs successfully from project root
- [x] Script fails gracefully from wrong directory
- [x] Logs are created with correct permissions
- [x] Log rotation deletes old logs correctly
- [x] Email notification sends on error (if enabled)
- [x] Exit codes are correct (0=success, 1=error, 2=fatal)
- [x] Cron syntax validates (`crontab -l`)

### Integration Testing

1. **Happy Path**: All documents up-to-date, no changes
2. **Updates**: Simulate changed documents, verify refetch
3. **Network Errors**: Disconnect WiFi, verify graceful failure
4. **Permission Errors**: Wrong directory permissions, verify error handling
5. **Missing Dependencies**: Uninstall Python packages, verify detection
6. **Empty Manifest**: No documents tracked, verify no-op behavior

---

## Documentation

### User Documentation

- **README.md**: "Automation" section with setup, troubleshooting, advanced config
- **scripts/update_docs.sh**: Inline comments and header documentation
- **logs/doc_fetcher/.gitkeep**: Log directory structure documentation

### Architecture Documentation

- **This ADR**: Comprehensive decision rationale
- **Implementation Guide**: `docs/implementation/issue-7-automation.md`
- **CHANGELOG.md**: Feature announcement and version tracking

---

## Migration Path

### Enabling Automation

1. Test script manually: `./scripts/update_docs.sh`
2. Add to crontab: `crontab -e`
3. Verify: `crontab -l`

### Disabling Automation

1. Comment out cron line: `crontab -e` (add `#`)
2. Or remove line completely
3. Verify: `crontab -l`

### Migrating to Different Scheduler

If moving to systemd timers or launchd:

1. Wrapper script remains unchanged (interface contract)
2. Replace cron with new scheduler
3. Test thoroughly (schedule, logging, permissions)
4. Update documentation

---

## Impact Analysis

### Benefits

1. **Automation**: No manual intervention required for doc updates
2. **Freshness**: Documentation stays current automatically
3. **Observability**: Comprehensive logs for troubleshooting
4. **Reliability**: Proven technology with minimal failure modes
5. **Simplicity**: Easy to understand, configure, and maintain
6. **Security**: Proper permissions, no credential exposure

### Risks

1. **Cron Not Configured**: User must manually set up (mitigated by clear docs)
2. **Email Misconfiguration**: Optional feature, fallback to logs
3. **Disk Space**: Log rotation prevents bloat
4. **Network Failures**: Graceful handling, retry next week
5. **Provider Rate Limits**: Existing rate limiting in doc_fetcher

### Maintenance Burden

**Low**: System runs autonomously with minimal maintenance
- Logs rotate automatically
- No database to maintain
- No background processes to monitor
- Cron handles scheduling reliably

---

## Success Criteria

- [x] Weekly updates run automatically via cron
- [x] Comprehensive logging with 30-day retention
- [x] Optional email notifications on errors
- [x] Environment validation prevents silent failures
- [x] Clear documentation for setup and troubleshooting
- [x] Script tested manually with all scenarios
- [x] Proper file permissions (750 script, 640 logs)
- [x] Exit codes correct for cron monitoring

---

## References

- [Issue #7: Set Up Weekly Documentation Update Automation](https://github.com/matteocervelli/llms/issues/7)
- [ADR-003: Documentation Fetcher Tool](./ADR-003-documentation-fetcher.md)
- [ADR-006: Crawl4AI Integration](./ADR-005-crawl4ai-integration.md)
- [cron Manual Page](https://man7.org/linux/man-pages/man5/crontab.5.html)
- [Bash Best Practices](https://google.github.io/styleguide/shellguide.html)

---

## Changelog

- **2025-10-26**: Initial version, automation system implemented
