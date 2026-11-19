# 05. Sentinel to Power BI pipeline

Goal: a sign-in monitoring dashboard in Power BI, fed directly from the Log Analytics workspace behind Microsoft Sentinel.

Status: connection working, dashboard in progress, publishing to the Power BI service not done yet.

## How it works

```
KQL query in Sentinel > Logs
   |  Export > Export to Power BI (as an M query)
   v
PowerBIQuery.txt   (Power Query M script that calls the Log Analytics query API)
   |  Power BI Desktop > Get data > Blank query > Advanced Editor > paste
   v
SignIns table in Power BI  ->  DAX measures  ->  report page
```

The exported file is not data. It is a script that runs the KQL against the Log Analytics API each time the report refreshes. It contains the workspace ID, so **it is excluded from this repo** (see `.gitignore`).

## Source query

```kql
SigninLogs
| where TimeGenerated > ago(30d)
| extend Country = tostring(LocationDetails.countryOrRegion),
         Outcome = case(ResultType == "0", "Success",
                        ResultType == "50126", "Bad password",
                        ResultType in ("50055","50072","50140"), "Interrupted (password change / MFA / KMSI)",
                        "Other failure")
| project TimeGenerated, UserPrincipalName, ResultType, Outcome, IPAddress, Country, AppDisplayName
```

Grouping result codes into a readable `Outcome` column in KQL, before Power BI sees the data, kept the report simple. Raw codes such as `50055` mean nothing to someone reading a dashboard.

## Accounts and permissions

| Need | Account | Why |
|---|---|---|
| Power BI Desktop (build) | None | Desktop works without signing in |
| Data source credential for the API | Lab tenant work account, as **Organizational account** | Must be able to read the workspace |
| Power BI service (publish) | Lab tenant work account | Consumer addresses (outlook.com, gmail.com) cannot sign up for the Power BI service |

## What broke, and the fix

### "Expression.Error: Access to the resource is forbidden"

The data source sign-in succeeded with the tenant's Global Administrator account, and the query was still refused.

**Cause.** Global Administrator is an **Entra ID role**: it controls the directory (users, groups, licences, directory roles). The Log Analytics workspace is an **Azure resource**, governed by **Azure RBAC**, a separate permission system. The workspace's subscription had been created by a different account, so the Global Administrator had no Azure role on it at all.

**Fix.**

1. Workspace > Access control (IAM) > Add role assignment.
2. Role: **Log Analytics Reader** (read-only; least privilege for a reporting connection).
3. Member: the account Power BI signs in with.
4. In Power BI: File > Options and settings > Data source settings > select the Log Analytics source > Clear Permissions, then refresh and sign in again.

This is the most useful thing the Power BI work taught me, and it is directly SC-300 material: Entra roles and Azure roles are assigned, scoped and audited separately.

### Date/time type

The API returns `TimeGenerated` as date/time with time zone. Changing it to plain **Date/Time** in Power Query made it usable for the hourly `Hour` column. Values remain in UTC.

### Report building mistakes

- Working in **focus mode** (the "Back to report" view) meant every change went to the same visual, so one chart kept being overwritten.
- Selecting a chart type while a visual is selected **changes** that visual instead of adding a new one. Click an empty part of the canvas first.
- Stacking unrelated measures (a percentage on top of counts) in one column chart produced a misleading picture. One stack should be parts of one whole.

## Still to do

- Finish the page layout and colour series by meaning (success green, bad password red, interrupted amber, other grey).
- Publish to the Power BI service under the lab tenant account, on a Fabric/Power BI trial.
- Rebuild a shareable copy of the report from `sample-data/signin-sample.csv` so the `.pbix` file can be committed without live tenant data.

Report details (measures and layout): [../powerbi/README.md](../powerbi/README.md).
