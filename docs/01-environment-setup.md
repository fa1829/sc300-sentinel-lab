# 01. Environment setup

Built on 2026-11-16. Times in the logs are UTC.

## Which tenant, and why

I have two Microsoft accounts:

| Account | Role in its tenant | Azure subscription |
|---|---|---|
| University student account | Ordinary user | Azure for Students |
| Personal lab tenant | Global Administrator | None at the start |

Sentinel reads the sign-in and audit logs of the tenant it lives in, and connecting those logs needs Global Administrator or Security Administrator in that tenant. In the university tenant I am an ordinary user, so the lab had to be built in the personal tenant. That meant adding a subscription there.

## Steps

### 1. Subscription

Started an Azure free trial in the lab tenant. It created `Azure subscription 1` with a fixed credit that expires on 2026-12-12.

I did not upgrade to pay-as-you-go. While the subscription stays a trial, services stop when the credit runs out instead of billing the card.

### 2. Log Analytics workspace

| Setting | Value |
|---|---|
| Resource group | `rg-sentinel-lab` |
| Workspace name | `law-sentinel-lab` |
| Region | Canada Central |
| Daily cap | 1 GB |

The review screen showed "Pay-as-you-go". That is the workspace pricing tier (billed per GB), not the subscription type. I misread it at first.

### 3. Microsoft Sentinel

Added Sentinel to `law-sentinel-lab`. The free trial activated automatically: up to 10 GB/day free for both Sentinel and Log Analytics, valid 2026-11-16 to 2026-12-17.

The Azure credit expires five days before the Sentinel trial does, so 2026-12-12 is the real deadline.

### 4. Entra ID data connector

In Content hub I first installed **Microsoft Entra ID Protection** by mistake. That solution brings in risk alerts, not raw sign-in and audit logs. I removed it and installed **Microsoft Entra ID**.

On the connector page I enabled:

- Sign-in logs
- Non-interactive user sign-in logs
- Audit logs

The connector shows "Disconnected" until the first logs arrive. That is normal.

### 5. Licence

Exporting sign-in logs requires Entra ID P1 or P2. The tenant has a P2 trial; the evidence is that Privileged Identity Management appears on the role assignment page, which it only does with P2.

### 6. Test activity

| Action | Purpose |
|---|---|
| Created six test users | Targets for the spray |
| Entered wrong passwords for each user from one browser | Simulated password spray |
| Entered the correct password for each user | Intended as successful sign-ins (see below) |
| Assigned `test1` as Global Administrator, then removed it | Privileged role assignment event |

One test user was created as `tes4` instead of `test4`. I left it; it makes no difference to the detections.

The "correct password" sign-ins did not complete. They stopped at the forced password change and MFA enrolment prompts, so the logs contain no successful sign-ins. Details are in [04-lessons-learned.md](04-lessons-learned.md).

### 7. Verifying ingestion

Queries are run in **Sentinel > Logs**, with the editor switched from Simple mode to **KQL mode**. The editor was hidden behind a welcome pop-up the first time.

```kql
SigninLogs
| project TimeGenerated, UserPrincipalName, ResultType, ResultDescription, IPAddress, Location
| order by TimeGenerated desc
```

Result: 30 sign-in events, all from one IP, covering all six test users. A sanitised copy is in [../sample-data/signin-sample.csv](../sample-data/signin-sample.csv).

## Cost controls in place

- Trial subscription, not upgraded
- 1 GB daily cap on the workspace
- No virtual machines or other compute in this subscription
