# 06. Learning roadmap

Target roles: IAM administrator, Microsoft 365 / IT administrator, moving towards security operations.

Checked 2026-11-18. Microsoft changes certifications and trial terms often, so confirm on Microsoft Learn before booking an exam or starting a trial.

## Products, in the order I am learning them

| Product | Why it matters for these roles | Status |
|---|---|---|
| Microsoft Entra ID | Identities, authentication, roles, PIM, Conditional Access: the core of IAM | In progress |
| Azure RBAC | Access to Azure resources; separate from Entra roles | Learned the hard way (see doc 05) |
| Log Analytics and KQL | The query language behind Sentinel, Defender hunting and Azure Monitor | In progress |
| Microsoft Sentinel | SIEM: ingestion, analytics rules, incidents | In progress |
| Microsoft Defender portal | Where Sentinel incidents and Defender XDR alerts are worked | Started |
| Power BI | Reporting security and identity data to people who do not read KQL | In progress |
| Logic Apps (Sentinel playbooks) | Automated response (SOAR) | Next |
| Microsoft Intune | Device enrolment, compliance, the device side of Conditional Access | Next |
| Microsoft Defender for Business / Endpoint | Endpoint detection and response | Next |
| Microsoft Purview | Data protection: sensitivity labels, DLP, audit | Later |

## Certifications

| Exam | Role | Notes |
|---|---|---|
| SC-300 | Identity and Access Administrator | Current focus |
| SC-200 | Security Operations Analyst | Sentinel, Defender XDR, KQL; overlaps heavily with this lab |
| PL-300 | Power BI Data Analyst | Optional; the Power BI work here is a start |
| MD-102 | Endpoint Administrator | If going towards IT admin / Intune |
| SC-401 | Information Security Administrator | Purview; replaced SC-400 in 2025 |
| SC-500 | Cloud and AI Security Engineer | Replaced AZ-500 on 2026-08-31 |

**Not pursuing MS-102** (Microsoft 365 Administrator): it is being retired around the end of 2026 (sources differ on the exact date), so it is not worth starting now.

## What free trials allow

| Trial | What it gives | Length | Caveats |
|---|---|---|---|
| Azure free account | Credit for Log Analytics, Logic Apps, VMs | 30 days of credit | Do not upgrade to pay-as-you-go if you want a hard stop |
| Microsoft Sentinel | Up to 10 GB/day free for Sentinel and Log Analytics | 31 days per workspace | |
| Entra ID P2 | PIM, Identity Protection, sign-in log export | 30 days | |
| Fabric / Power BI | Publishing to the Power BI service | 60 days | Needs a work account, not outlook.com or gmail.com |
| Microsoft 365 Business Premium | Intune, Defender for Business, Entra ID P1, Exchange, Teams | 30 days, 25 users | Needs a card; **converts to paid unless cancelled**, so turn off recurring billing on day one |
| Microsoft 365 E5 developer sandbox | Full E5 tenant | 90 days, renewable | Now restricted to qualifying members (for example Visual Studio Professional or Enterprise subscribers); I do not qualify |

## Next labs

1. **SOAR.** A Logic Apps playbook that runs on the password-spray incident and notifies or revokes sessions.
2. **Impossible travel.** Generate a successful sign-in from a second country (VPN) and test the rule.
3. **Conditional Access.** Require MFA for admins, block legacy authentication, then watch the effect in `SigninLogs`.
4. **Intune and Defender for Business.** Enrol a Windows VM, apply a compliance policy, connect Defender alerts to Sentinel.
5. **Workbook.** Rebuild the Power BI dashboard as a Sentinel workbook and compare the two.
