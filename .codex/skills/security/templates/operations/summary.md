# Operations Security — L1 Essentials

**Stack**: GitHub + SSH deployment, secrets manager CLI, Ubuntu VPS | Solo or small team

| Control           | Requirement                                      |
| ----------------- | ------------------------------------------------ |
| Secrets source    | secrets manager CLI, never .env in git or hardcoded    |
| Secret injection  | Docker secrets (file-based), read at deploy time |
| Deployment        | Git-based, no manual file transfers              |
| Health check      | Verify /health before marking deploy complete    |
| Rollback          | Documented procedure, tested regularly           |
| Backups           | Daily encrypted (GPG) to Backblaze B2            |
| Backup testing    | Monthly restoration verification                 |
| Monitoring        | /health endpoint with component status           |
| Error tracking    | Generic errors with correlation error_id         |
| Incident response | Playbook with severity levels and SLAs           |

**Deeper**: Ask for patterns (Don't/Do/Best) or full SOP.
