# Infrastructure Security — L1 Essentials

**Stack**: Docker + Compose + Nginx + Garage S3 + Cloudflare | Single Ubuntu VPS

| Control      | Requirement                                              |
| ------------ | -------------------------------------------------------- |
| Docker user  | Non-root (USER directive), no-new-privileges             |
| Capabilities | `cap_drop: ALL`                                          |
| Filesystem   | `read_only: true` + tmpfs for /tmp                       |
| Networks     | Internal network for postgres/redis, DMZ for nginx       |
| Nginx        | server_tokens off, rate limiting zones, security headers |
| TLS          | TLSv1.3 only, Cloudflare origin certs                    |
| Firewall     | UFW: default deny, allow 22/80/443 only                  |
| SSH          | Key-only auth, PermitRootLogin no, fail2ban              |
| Cloudflare   | Strict SSL, Always HTTPS, WAF rules                      |
| Garage S3    | Tenant-prefixed keys, admin API on localhost only        |

**Deeper**: Ask for patterns (Don't/Do/Best) or full SOP.
