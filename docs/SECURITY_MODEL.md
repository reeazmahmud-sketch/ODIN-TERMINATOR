# Security Model

## Authority
No AI has permanent root authority. TERMINATOR may be eligible to request high-risk capabilities; ODIN independently evaluates policy and human authorization.

## Risk classes
- R0 Read-only
- R1 Reversible user-space mutation
- R2 Significant project/browser mutation
- R3 Privileged system or credential-mediated operation
- R4 Protected/unsupported operation — deny by default

## macOS
Touch ID/user-presence verification and privileged authorization are separate concerns. Production implementation should use supported macOS LocalAuthentication for identity confirmation and supported Authorization Services/privileged helper mechanisms where privilege is required. SIP, TCC, Accessibility, Automation, Full Disk Access, Keychain ACLs and the sealed system volume remain authoritative. ODIN never bypasses them.

## Secrets
Secrets remain in macOS Keychain or an approved secret provider. Audit logs record secret identifiers and outcomes, never values. Browser typing into password/token fields is redacted at source.

## Commands
Capabilities use typed APIs. Never construct privileged shell strings from untrusted arguments. Destructive actions require explicit targets, precondition checks and transaction/recovery metadata.

## Learning
Approval history is advisory. Learning may propose a scoped policy amendment; a human must approve the policy version. Denials, privileged actions and FINAL/ARCHIVED overrides never become auto-approved from frequency.
