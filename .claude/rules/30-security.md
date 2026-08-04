# Security rules

- Never read, write, echo, commit, or expose real secrets, private keys, access tokens, credentials, or production environment files.
- Treat `.env`, `.env.*`, `*.pem`, `*.key`, credential files, and secret-manager exports as sensitive unless they are explicit safe examples.
- Do not weaken authentication, authorization, validation, rate limits, audit logging, or cryptographic controls merely to satisfy a test.
- Security-sensitive assumptions must be surfaced during architecture critique and backed by evidence.
- Prefer least privilege for subagent tools and project permissions.
