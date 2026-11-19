# 00. Why this lab exists

## The question I could not answer well

I finished my MASc in Information Systems Security in summer 2026. Coursework, academic projects and research left me confident about the theory of cyber security.

Then an interviewer asked:

> What production experience do you have implementing, maintaining and troubleshooting IAM, responding to incidents, or triaging security alerts?

My honest answer was: very little, in the Microsoft identity and security stack specifically. Many students about to graduate, and recent graduates, face the same question.

## What I decided to do

Microsoft's own products (Entra ID, Microsoft 365, Azure, Sentinel, Defender and Power BI) can all be run for free or close to free on trial licences. That is enough to build a small but genuine version of the environment that IAM, Microsoft 365 administration and SOC roles work in, and to practise the actual tasks:

| Task an interviewer asks about | What I did in the lab |
|---|---|
| Implementing IAM | Created users, assigned and removed privileged roles through PIM, worked with licences |
| Maintaining and troubleshooting | Connected Entra ID logs to a SIEM; diagnosed missing data, wrong connectors, licence gates and an access-denied error |
| Detection | Wrote and deployed KQL analytics rules in Microsoft Sentinel |
| Triage and incident response | Worked the incidents my rules produced in the Defender portal |
| Reporting | Built a Power BI dashboard fed directly from Sentinel's Log Analytics workspace |

## What a lab can show, and what it cannot

**It can show** that I can set these tools up, connect them, write queries that work, read the logs they produce, and debug them when they do not behave. Every claim in this repo is backed by a query, a sample of the output, or a documented mistake.

**It cannot show** what real operations involve: thousands of users, noisy data, change control, false positives at volume, on-call pressure, and the consequences of getting it wrong. I do not describe this as production experience, and I would not expect an employer to treat it as such.

The aim is a better answer to that interview question: not "I have done it in production", but "here is what I built, here is what broke, here is how I fixed it, and here is what I would do differently at scale."
