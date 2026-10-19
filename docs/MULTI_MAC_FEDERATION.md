# Multi-Mac Federation

Federation is zero-trust between nodes. Each installation has a cryptographic node identity. Transport must be mutually authenticated and encrypted.

## Message requirements
`request_id`, `node_id`, `actor_id`, `capability`, `intent_hash`, `timestamp`, `nonce`, state version and signature.

## State
Project locks and lifecycle state require authoritative ownership/versioning; last-packet-wins is forbidden for safety-critical state. Conflicts are quarantined for reconciliation. Offline nodes queue signed events and reconcile on reconnect.

## Replication
Do not blindly replicate credentials. Policies, project metadata, event summaries and approved artifacts have explicit replication classes. Node keys remain local.
