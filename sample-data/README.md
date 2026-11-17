# Sample data

Sanitised copies of query output from the lab, kept so the detection logic can be checked without access to the tenant.

| File | Source query | Notes |
|---|---|---|
| `signin-sample.csv` | `SigninLogs` projection | 30 events, six test users, one source IP |
| `audit-sample.csv` | Role membership query | One add and one remove for `test1` |

Changes made before committing:

- Tenant domain replaced with `contoso-lab.onmicrosoft.com`
- Source IP replaced with `2001:db8::1` (an address range reserved for documentation)

In `audit-sample.csv`, the Target and Role values are the ones expected from the lab actions (assigning `test1` as Global Administrator). Confirm them against the live query output before relying on this file.
