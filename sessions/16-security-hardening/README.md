# Session 16: Kubernetes Security Hardening

This session teaches secure Pod and Namespace defaults.

## Sub-Session Order

1. `01-threat-model`: image, runtime, network, identity, and API risks.
2. `02-pod-security-standards`: privileged, baseline, restricted.
3. `03-security-context`: users, groups, capabilities, privilege escalation.
4. `04-seccomp-and-apparmor`: kernel-level controls.
5. `05-read-only-root-filesystem`: immutable runtime filesystem.
6. `06-image-security`: trusted registries and image scanning.
7. `07-runtime-hardening-checklist`: production checklist.

## Example Security Settings

```yaml
securityContext:
  runAsNonRoot: true
  allowPrivilegeEscalation: false
  readOnlyRootFilesystem: true
  capabilities:
    drop:
      - ALL
```

## Review Questions

1. Why should containers avoid running as root?
2. What do Linux capabilities control?
3. What does seccomp restrict?
4. Why is privileged mode dangerous?
