# 03. Incident response

Sentinel incidents surface in the Microsoft Defender portal (security.microsoft.com) under Incidents. This page is the runbook I follow and the record of each lab incident.

The phases follow the NIST incident handling lifecycle (preparation; detection and analysis; containment, eradication and recovery; post-incident activity), scaled down to a lab.

## Incidents generated so far

| ID | Name | Severity | Category | Created (UTC) | Entities | Source |
|---|---|---|---|---|---|---|
| 2 | Privileged role assigned | High | Privilege Escalation | 2026-11-17 02:56 | 2 accounts | Scheduled detection, Microsoft Sentinel |
| 1 | Password spray: one IP, many accounts | Medium | Credential Access | 2026-11-17 02:47 | 1 IP | Scheduled detection, Microsoft Sentinel |

## Runbook

### 1. Triage (first 15 minutes)

1. Open the incident. Assign it to yourself and set status to **Active / In progress**.
2. Read the alert: which rule fired, which entities (accounts, IPs), what time window.
3. Decide: is this expected activity, a true positive, or a false positive? Write the reason in a comment.

### 2. Investigate

Run the queries below in Sentinel > Logs or Defender > Advanced hunting, replacing the placeholders.

Password spray: what else did the source IP do, and did anything succeed?

```kql
SigninLogs
| where IPAddress == "<source IP>"
| summarize Attempts = count(),
            Accounts = dcount(UserPrincipalName),
            Successes = countif(ResultType == "0"),
            First = min(TimeGenerated), Last = max(TimeGenerated)
    by IPAddress
```

```kql
SigninLogs
| where IPAddress == "<source IP>" and ResultType == "0"
| project TimeGenerated, UserPrincipalName, AppDisplayName, Location
```

Privileged role: what did the account do while it held the role?

```kql
AuditLogs
| where TimeGenerated between (datetime(<assigned>) .. datetime(<removed>))
| where tostring(InitiatedBy.user.userPrincipalName) == "<target account>"
| project TimeGenerated, OperationName, Result, TargetResources
```

### 3. Contain and recover (if it were real)

| Incident | Containment | Recovery |
|---|---|---|
| Password spray, no success | Block the source IP with a Conditional Access named location (exclude break-glass accounts) | Confirm MFA is enforced for all targeted accounts |
| Password spray, with a success | Revoke sessions for the compromised account; force a password reset; block the IP | Review that account's sign-ins and audit activity after the success |
| Unapproved privileged role | Remove the role; revoke the account's sessions | Review every change the account made while privileged; require PIM approval for that role |

In the lab I carry out the actions that are safe and reversible (revoking sessions and forcing password resets for test users), and document the others.

### 4. Close

Set classification and determination, add a closing comment, close. For lab-generated activity: **Informational, expected activity > Security testing**.

## Incident records

### Incident 1: Password spray

- **Triage:** _
- **Investigation findings:** _ (source IP, accounts targeted, attempt count, any successes)
- **Actions taken:** _
- **Classification:** Informational, expected activity > Security testing
- **Time to close:** _
- **What I would change:** _

### Incident 2: Privileged role assigned

- **Triage:** _
- **Investigation findings:** _ (who assigned, who received, duration, activity while privileged)
- **Actions taken:** _
- **Classification:** Informational, expected activity > Security testing
- **Time to close:** _
- **What I would change:** _

## Portal behaviour worth knowing

The Cases view opened with a default filter of **Priority score: 15 to 100**. Both lab incidents scored 1 and 2, so the list showed "No incident cases found" until I removed the filter. The rules had worked; the view was hiding the result.
