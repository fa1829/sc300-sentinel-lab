# 02. Detections

All three are Sentinel **scheduled query rules**. The KQL for each is in [../detections/](../detections/).

Common settings while testing:

| Setting | Lab value | What I would use in production |
|---|---|---|
| Run query every | 1 hour | 1 hour or less |
| Lookup data from the last | 1 day | Same as the run interval, to avoid repeat alerts |
| Alert threshold | Greater than 0 results | Same |

The 1-day lookup is deliberate: it let a newly created rule catch test events that were already an hour old. The cost is that the same events can alert again on each hourly run for a day.

---

## 1. Password spray: one IP, many accounts

File: [password-spray.kql](../detections/password-spray.kql)

**Idea.** A spray tries one or two passwords against many accounts, staying under the per-account lockout threshold. Per-account failure counts miss it. Counting distinct accounts per source IP does not.

**Logic.** Bad-password failures (`ResultType == "50126"`), grouped by IP in 30-minute bins, alerting when 5 or more distinct accounts are targeted.

**Test.** One IP failed against `test2`, `test3`, `tes4`, `test5` and `test6` between 01:46 and 01:57 UTC on 2026-11-17. Five accounts in one 30-minute bin, so the rule fired.

**Entity mapping.** IP > Address > `IPAddress`.

**Known weaknesses.**

- An attacker who rotates source IPs (the common case in real sprays) stays under the per-IP threshold. A stronger version would also count failures across all IPs per time window, or group by ASN or user agent.
- A shared corporate egress IP or NAT gateway with several users mistyping passwords can trigger it. I have no real traffic to measure how often.
- Fixed 30-minute bins can split one spray across two bins and miss it. A sliding window would fix that.
- The threshold of 5 is sized to a six-user lab.

---

## 2. Privileged role assigned

File: [privileged-role-assigned.kql](../detections/privileged-role-assigned.kql)

**Idea.** Adding an account to a high-privilege role is a standard persistence and escalation step, and it should be rare enough to review every time.

**Logic.** Audit events for a completed role addition, with the role and the target user pulled out of `TargetResources`, filtered to a short list of high-privilege roles.

**Test.** `test1` was assigned Global Administrator at 19:11 UTC on 2026-11-16 and removed at 01:32 UTC on 2026-11-17. The rule fired on the assignment.

**Entity mapping.** Account > FullName > `Target`, and Account > FullName > `Actor`.

**What I got wrong first.** My first version filtered on `OperationName == "Add member to role"` and read the user from `TargetResources[0]`. With PIM active in the tenant:

- the operation is named `Add member to role in PIM completed (permanent)`
- `TargetResources[0]` is the role, not the user
- the removal reads `Remove member from role ...`, which a filter on "member to role" does not match

The fix was to match on substrings and to select the role and user by their `type` field with `mv-apply`, not by array position.

**Known weaknesses.**

- The role list is hard-coded and short. Microsoft marks many more roles as privileged.
- It covers active assignments. Eligible (just-in-time) PIM assignments and role-assignable group membership changes are separate events that this rule does not look at.
- In an organisation with routine admin onboarding, this needs an allow-list of expected actors or a change-ticket check, or it becomes noise.

---

## 3. Impossible travel (simplified)

File: [impossible-travel.kql](../detections/impossible-travel.kql)

**Status: not tested.** Successful sign-ins now exist (from 2026-11-17), but all from one country, so the rule has nothing to match yet.

**Idea.** The same account signing in successfully from two countries within an hour is unlikely to be one person.

**Logic.** Successful sign-ins (`ResultType == "0"`), grouped by user in 1-hour bins, alerting when more than one country appears.

**Known weaknesses.**

- It compares country names, not distance and time. Two countries an hour apart by train will alert; two distant cities in one large country will not.
- VPNs, mobile carriers and cloud proxies produce exactly this pattern for legitimate users.
- Entra ID Protection already does a proper version of this with learned behaviour. This rule is for learning KQL, not for replacing that.

**To test it.** Sign in as a test user normally, then sign in again through a VPN exit in another country within the same hour.
