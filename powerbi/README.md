# Power BI: identity sign-in dashboard

Built in Power BI Desktop from Entra ID `SigninLogs` in the lab's Log Analytics workspace. Pipeline and troubleshooting notes: [../docs/05-powerbi-pipeline.md](../docs/05-powerbi-pipeline.md).

The `.pbix` file built on live data is **not** committed: it holds the workspace ID and real sign-in records. A version built from the sanitised sample data may be added later.

## Data

One table, `SignIns`, with columns `TimeGenerated`, `UserPrincipalName`, `ResultType`, `Outcome`, `IPAddress`, `Country`, `AppDisplayName`, plus a calculated `Hour` column.

## Measures

All DAX is in [measures.dax](measures.dax).

| Measure | Meaning |
|---|---|
| Total Sign-ins | Every sign-in event in the period |
| Failed Sign-ins | Everything that is not `Success`, including interrupted sign-ins |
| Failure Rate | Failed / total |
| Accounts Targeted | Distinct accounts with at least one bad-password failure |

"Failed" deliberately includes interrupted sign-ins (forced password change, MFA enrolment, "stay signed in" prompt). That inflates the failure rate in a lab where every test user was new. In a real tenant, I would report interrupts separately.

## Page layout (1280 x 720)

| Visual | Fields | Position (x, y, width, height) |
|---|---|---|
| Title text box | Identity Sign-in Monitoring: Entra ID lab tenant | 20, 10, 1240, 50 |
| 4 cards | Total Sign-ins, Failed Sign-ins, Failure Rate, Accounts Targeted | y 70, height 100, width 230 each |
| Slicer (tiles) | Outcome | 1020, 70, 240, 100 |
| Stacked column chart | X: Hour, Y: Total Sign-ins, Legend: Outcome | 20, 190, 740, 510 |
| Table | IPAddress, Accounts Targeted, Failed Sign-ins | 780, 190, 480, 200 |
| Clustered bar chart | Y: UserPrincipalName, X: Failed Sign-ins, Legend: Outcome | 780, 410, 480, 290 |

## Page 2: Incidents (to do)

Source: `SecurityIncident`, one row per incident. Query and steps: [../docs/05-powerbi-pipeline.md](../docs/05-powerbi-pipeline.md#second-pipeline-sentinel-incidents-to-power-bi).

| Visual | Fields |
|---|---|
| 4 cards | Total Incidents, Open Incidents, High Severity Incidents, Mean Hours to Close |
| Clustered column chart | X: Severity, Y: Total Incidents, Legend: Status |
| Donut chart | Legend: Classification, Values: Total Incidents |
| Table | IncidentNumber, Title, Severity, Status, Tactics, CreatedTime, HoursToClose |
| Slicer | Severity |

With two lab incidents, this page is about proving the pipeline works, not about the numbers.

## What the dashboard shows from the lab data

- A spike of bad-password failures across five accounts from one IP in a few minutes overnight. This is the same password spray the Sentinel analytics rule detects.
- Successful sign-ins only appear later, after test users completed the password change and MFA enrolment.
- Selecting the spray in any visual cross-filters the rest of the page to the source IP and the targeted accounts.

## Screenshots

To be added under [../screenshots/](../screenshots/), with IP addresses and the tenant domain redacted.
