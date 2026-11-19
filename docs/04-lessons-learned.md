# 04. Lessons learned

Things that did not behave the way I assumed. These are the parts I would not have learned from reading alone.

## A correct password is not a successful sign-in

I entered the right password for each test user and expected rows with `ResultType == "0"`. There were none. The sign-ins stopped at interrupts:

| ResultType | Meaning | Where I hit it |
|---|---|---|
| `50126` | Invalid username or password | The deliberate wrong-password attempts |
| `50055` | Password is expired | First sign-in with a temporary password; a change is forced |
| `50072` | User must enrol in MFA | After the password step, before access is granted |
| `50089` | Flow token expired | A sign-in page left open too long |

Consequence for detection: a rule that looks for "failures followed by a success" must decide how to treat these interrupt codes. They are not failures of the password, and they are not successes either.

## PIM changes the shape of audit events

With Privileged Identity Management active, a role assignment is logged as `Add member to role in PIM completed (permanent)`, and the first entry in `TargetResources` is the role, not the user. A query written against the non-PIM event shape returned the event but with an empty target. See [02-detections.md](02-detections.md).

General rule I took from it: select fields in `TargetResources` by their `type`, never by array index.

## Licences gate log export

Audit logs export on the free tier. Sign-in logs need Entra ID P1 or P2. Without the licence the workspace simply has no `SigninLogs` table, which looks like a broken connector.

## Similar product names, different data

"Microsoft Entra ID Protection" and "Microsoft Entra ID" are separate Content hub solutions. The first ingests risk alerts; the second ingests the raw sign-in and audit logs that custom rules query. I installed the wrong one first.

## "Pay-as-you-go" appears in two unrelated places

It is both a subscription type and a Log Analytics pricing tier. Seeing it on the workspace creation screen does not mean the subscription was upgraded.

## A default filter can hide working detections

The Defender portal's Cases view filtered out low-priority incidents by default, so two correctly generated incidents showed as an empty list. When a detection seems not to have fired, query `SecurityAlert` and `SecurityIncident` directly before assuming the rule is broken.

## The portal is moving

Sentinel in the Azure portal is scheduled for retirement on 2027-03-31, after which it is available only in the Defender portal. Rules were created in the Azure portal, and incidents already appear in Defender. New learning should happen in the Defender portal.

## The right tenant matters more than the available credit

My student subscription had credit but sat in a tenant where I have no admin rights. The detections needed a tenant I administer, even though that meant starting a new trial.

## Entra roles and Azure roles are separate systems

Power BI signed in to the Log Analytics API as the tenant's Global Administrator and was still refused ("Access to the resource is forbidden"). Global Administrator is an Entra directory role; the workspace is an Azure resource governed by Azure RBAC. The fix was a **Log Analytics Reader** assignment on the workspace. Details in [05-powerbi-pipeline.md](05-powerbi-pipeline.md).

## Not every non-zero result code is a failure

`50140` is the "Stay signed in?" prompt and `50074` is an MFA challenge. Counting every non-zero `ResultType` as a failure overstates attacks. Interrupts need their own category.

## An exported query can leak identifiers

Log Analytics' "Export to Power BI (M query)" file embeds the workspace ID, and a `.pbix` built on live data embeds real sign-in records. Neither belongs in a public repo; both are excluded in `.gitignore`.
