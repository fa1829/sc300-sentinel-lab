# 07. KQL notes

Patterns I used in this lab, with the reason each one mattered. Every example comes from a query in [../detections/](../detections/) or [05-powerbi-pipeline.md](05-powerbi-pipeline.md).

## Shape of a query

A KQL query is a table piped through operators, top to bottom:

```kql
SigninLogs                          // start from a table
| where TimeGenerated > ago(1d)     // filter early: less data, faster query
| extend Country = tostring(LocationDetails.countryOrRegion)   // add a column
| project TimeGenerated, UserPrincipalName, Country            // keep only what you need
| order by TimeGenerated desc
```

## Operators I used

| Operator | What it does | Where I used it |
|---|---|---|
| `where` | Filters rows | Every query |
| `project` | Chooses and renames columns | Output shaping |
| `extend` | Adds a computed column | `Country`, `Outcome`, `Actor` |
| `summarize ... by` | Groups and aggregates | Spray and travel rules |
| `bin(TimeGenerated, 30m)` | Buckets time into fixed windows | Spray rule |
| `dcount()` | Distinct count | Accounts per IP, countries per user |
| `make_set()` | Collects distinct values into an array | List of targeted users as evidence |
| `case()` | If/else chain | Turning result codes into readable outcomes |
| `mv-apply` | Runs a sub-query over each element of an array | Picking role and user out of `TargetResources` |
| `take_anyif()` | Takes a value that meets a condition | Same, by `type` |
| `has`, `has_any` | Whole-term text match, indexed and fast | Matching operation names |

## Lessons

**`has` vs `==`.** `OperationName == "Add member to role"` missed the PIM version of the event (`Add member to role in PIM completed (permanent)`). `has "member to role"` matched both.

**Never index into arrays by position.** `TargetResources[0]` was the user in one event type and the role in another. Selecting by `type` with `mv-apply` works for both:

```kql
| mv-apply tr = TargetResources on (
    summarize Role   = take_anyif(tostring(tr.displayName),       tostring(tr.type) == "Role"),
              Target = take_anyif(tostring(tr.userPrincipalName), tostring(tr.type) == "User")
  )
```

**Dynamic fields need `tostring()`.** `LocationDetails` and `TargetResources` are dynamic (JSON) columns. Comparing or grouping on a field inside them without `tostring()` gives errors or empty results.

**`ResultType` is a string.** It looks numeric, but compare it as text: `ResultType == "50126"`.

**Count distinct things, not events, to catch sprays.** A spray is a few attempts against many accounts. `count()` per account sees nothing unusual; `dcount(UserPrincipalName)` per IP does.

## Sign-in result codes seen in this lab

| Code | Meaning |
|---|---|
| `0` | Success |
| `50126` | Invalid username or password |
| `50055` | Password expired (forced change on first sign-in) |
| `50072` | User must enrol in MFA |
| `50074` | Strong authentication (MFA) required |
| `50089` | Flow token expired (sign-in page left open) |
| `50140` | "Stay signed in?" interrupt |

## Tables used

| Table | Contains |
|---|---|
| `SigninLogs` | Interactive user sign-ins |
| `AuditLogs` | Directory changes: users, groups, roles, apps |
| `SecurityAlert` | Alerts produced by analytics rules |
| `SecurityIncident` | Incidents grouped from alerts |
