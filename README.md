# SC-300 and Microsoft Sentinel lab journal

A working record of how I am learning Microsoft identity and security operations: studying for SC-300 (Identity and Access Administrator) and building a Microsoft Sentinel detection lab on top of my own Entra ID tenant.

This is lab work in a personal tenant with test users. It is not production experience, and nothing here claims to be.

## What is in this repo

| Path | Contents |
|---|---|
| [docs/01-environment-setup.md](docs/01-environment-setup.md) | How the lab was built, step by step, including the wrong turns |
| [docs/02-detections.md](docs/02-detections.md) | The detection rules, how each was tested, and their known weaknesses |
| [docs/03-incident-triage.md](docs/03-incident-triage.md) | The incidents the rules produced and how I handle them |
| [docs/04-lessons-learned.md](docs/04-lessons-learned.md) | Things that did not work the way I expected |
| [docs/sc300-study-log.md](docs/sc300-study-log.md) | SC-300 study tracker and dated log |
| [detections/](detections/) | KQL for each rule, one file per rule |
| [sample-data/](sample-data/) | Sanitised query output used to validate the rules |
| [screenshots/](screenshots/) | Evidence screenshots (redacted before commit) |

## Current status

Last updated: 2026-11-16

| Item | Status |
|---|---|
| Azure free trial subscription in lab tenant | Done |
| Log Analytics workspace with 1 GB daily cap | Done |
| Microsoft Sentinel enabled (31-day trial) | Done |
| Entra ID sign-in and audit logs connected | Done |
| Rule: password spray | Deployed, fired on test data |
| Rule: privileged role assigned | Deployed, fired on test data |
| Rule: impossible travel | Query written, **not tested** (no successful sign-ins from two countries yet) |
| Incident triage and closure notes | To do |
| Logic Apps playbook (SOAR) | To do |
| Exported rule JSON | To do |
| SC-300 exam | Studying |

## Lab architecture

```
Entra ID lab tenant (P2 trial licence)
  |  diagnostic setting: SignInLogs, NonInteractiveUserSignInLogs, AuditLogs
  v
Log Analytics workspace  law-sentinel-lab  (Canada Central, 1 GB/day cap)
  |
  v
Microsoft Sentinel  ->  scheduled analytics rules (KQL)  ->  incidents in the Defender portal
```

## Detections at a glance

| Rule | Table | Logic | MITRE ATT&CK | Severity |
|---|---|---|---|---|
| Password spray: one IP, many accounts | `SigninLogs` | One IP with bad-password failures against 5 or more accounts in 30 minutes | T1110 (Brute Force) | Medium |
| Privileged role assigned | `AuditLogs` | A user is added to a high-privilege Entra role, including through PIM | T1098 (Account Manipulation) | High |
| Impossible travel (simplified) | `SigninLogs` | Successful sign-ins from more than one country within an hour | T1078 (Valid Accounts) | Medium |

## Limits of this lab

- Six test users and one source IP. The thresholds are tuned to that, not to a real organisation's traffic.
- The rules have only been tested against activity I generated myself. I have no false-positive data from real users.
- The Azure credit and the Sentinel trial both end in December 2026, so the environment is temporary. The queries, exported rules and notes in this repo are what persists.
- Tenant name, IP addresses and subscription identifiers are replaced with placeholders throughout.

## Author

Faisal. MASc in Information Systems Security (Concordia University), about 16 years in telecommunications before that.
