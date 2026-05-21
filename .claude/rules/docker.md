---
paths:
  - "Dockerfile*"
  - "*.dockerfile"
  - "compose*.yaml"
  - "compose*.yml"
  - "docker-compose*.yml"
  - ".dockerignore"
---

# Docker Rules

## Images

- Pin exact versions: `node:22.12-alpine`, never `node:latest`
- Prefer alpine, slim, or distroless base images

## Build Efficiency

- Order layers by change frequency: OS deps → app deps → source code
- Combine RUN commands and clean up in the same layer
- Use multi-stage builds: build stage + minimal runtime stage
- Create `.dockerignore` for every project with Docker

## Security

- Never run as root: create and switch to a non-root USER
- Never put secrets in ENV, ARG, or COPY directives
- Use `--mount=type=secret` for build-time secrets, runtime env for runtime secrets
- Add HEALTHCHECK directive to every production image

## Compose

- Use `docker compose` not `docker-compose` (deprecated)
- Name files `compose.yaml` not `docker-compose.yml` (modern convention)
- Use `compose.override.yaml` for dev overrides (loaded automatically)
- Pin image versions, set resource limits, use named volumes in production
- Define healthcheck for each service
