# SC-300 study log

Exam: Microsoft Identity and Access Administrator (SC-300).

## Skill areas

The four areas below are from the SC-300 study guide as I understand it. Microsoft revises the guide, so check the current version on Microsoft Learn before relying on this list.

| Area | Status | Lab evidence in this repo |
|---|---|---|
| Implement and manage user identities | | Created and managed test users in the lab tenant |
| Implement authentication and access management | | Observed forced password change and MFA enrolment in sign-in logs |
| Plan and implement workload identities | | |
| Plan and automate identity governance | | Assigned and removed a role through PIM; read the resulting audit events |

Fill in **Status** with: not started, in progress, or done.

## Log

### 2026-11-16

- Built a Sentinel lab on the Entra ID lab tenant: subscription, workspace, Sentinel, Entra ID connector.
- Generated test activity: six users, a password spray, a PIM role assignment and removal.
- Wrote and deployed two KQL detection rules; both produced incidents.
- Learned the sign-in result codes 50126, 50055, 50072 and 50089 from my own logs.
- Learned how PIM role assignments appear in `AuditLogs`.

Relevance to SC-300: monitoring and reporting on identity (sign-in and audit logs, diagnostic settings), PIM role assignment, licence requirements for identity features.

### 2026-11-17 to 2026-11-18

- Connected Power BI Desktop to the Log Analytics workspace using a KQL query exported as an M query.
- Hit "Access to the resource is forbidden": Global Administrator (Entra role) gave no access to the workspace (Azure resource). Fixed with a Log Analytics Reader assignment.
- Learned result codes 50074 and 50140 and moved interrupts into their own category.
- Built DAX measures and most of a sign-in monitoring dashboard.

Relevance to SC-300: the difference between Entra roles and Azure RBAC, least-privilege role choice, sign-in log analysis.

### Template for new entries

```
### YYYY-MM-DD

- What I studied or built:
- What I got wrong:
- What I would explain differently now:
- Maps to skill area:
```

## Related: SC-200

The Sentinel and KQL work here overlaps with SC-200 (Security Operations Analyst). I am using this lab for both.
