# 03. Incident triage

Sentinel incidents now surface in the Microsoft Defender portal (security.microsoft.com), under Cases / Incidents.

## Incidents generated so far

| ID | Name | Severity | Category | Created (UTC) | Entities | Source |
|---|---|---|---|---|---|---|
| 2 | Privileged role assigned | High | Privilege Escalation | 2026-11-17 02:56 | 2 accounts | Scheduled detection, Microsoft Sentinel |
| 1 | Password spray: one IP, many accounts | Medium | Credential Access | 2026-11-17 02:47 | none listed | Scheduled detection, Microsoft Sentinel |

Incident 1 lists no impacted assets because its only mapped entity is an IP address, which the portal does not count as an asset.

## Triage notes

To be filled in as each incident is worked. Template:

### Incident 1: Password spray

- **What fired:**
- **What I checked:** (source IP, accounts targeted, whether any attempt succeeded, time window)
- **Finding:**
- **Classification:** Informational, expected activity > Security testing
- **What I would do if this were real:** (block or investigate the IP, check for any success from it, reset passwords for targeted accounts, confirm MFA coverage)

### Incident 2: Privileged role assigned

- **What fired:**
- **What I checked:** (who made the assignment, who received it, whether it was removed, what the account did while privileged)
- **Finding:**
- **Classification:** Informational, expected activity > Security testing
- **What I would do if this were real:** (confirm with the actor out of band, review the target account's sign-ins and audit activity during the window, remove the role if unapproved)

## Portal behaviour worth knowing

The Cases view opened with a default filter of **Priority score: 15 to 100**. Both lab incidents scored 1 and 2, so the list showed "No incident cases found" until I removed the filter. The rules had worked; the view was hiding the result.
