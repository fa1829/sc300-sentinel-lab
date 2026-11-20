import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

W, H = 16.6, 9
fig, ax = plt.subplots(figsize=(W, H), dpi=100)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
fig.patch.set_facecolor("white")

INK = "#1b1f24"; MUTED = "#57606a"
C = {"id": "#0b5cad", "log": "#0f7b6c", "siem": "#5b3fa8", "resp": "#b4461b", "bi": "#a37c00"}

def box(x, y, w, h, color, step, title, lines):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.18",
                                linewidth=2, edgecolor=color, facecolor=color + "14"))
    ax.add_patch(Circle((x + 0.38, y + h - 0.38), 0.24, color=color))
    ax.text(x + 0.38, y + h - 0.38, str(step), color="white", ha="center", va="center",
            fontsize=13, fontweight="bold")
    ax.text(x + 0.75, y + h - 0.38, title, color=INK, ha="left", va="center",
            fontsize=14, fontweight="bold")
    for i, t in enumerate(lines):
        ax.text(x + 0.3, y + h - 0.95 - i * 0.42, t, color=MUTED, ha="left", va="center", fontsize=11.2)

def arrow(x1, y1, x2, y2, label=None, lx=None, ly=None, dashed=False):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=22,
                                 linewidth=2, color="#8c959f", linestyle="--" if dashed else "-"))
    if label:
        ax.text(lx if lx is not None else (x1 + x2) / 2, ly if ly is not None else (y1 + y2) / 2 + 0.22,
                label, ha="center", va="bottom", fontsize=10.5, color=MUTED, style="italic")

ax.text(0.45, 8.45, "Microsoft identity & security lab pipeline", fontsize=24, fontweight="bold", color=INK)
ax.text(0.45, 7.95, "Built on free trial licences  ·  1 tenant  ·  6 test users  ·  lab scale, not production",
        fontsize=13, color=MUTED)

bw, bh = 2.95, 2.45
xs = [0.45, 4.7, 8.95, 13.2]
ytop = 4.75
box(xs[0], ytop, bw, bh, C["id"], 1, "Entra ID", ["Test users, P2 trial", "PIM role assignments", "Sign-ins and audit events"])
box(xs[1], ytop, bw, bh, C["log"], 2, "Log Analytics", ["SigninLogs", "AuditLogs", "SecurityIncident"])
box(xs[2], ytop, bw, bh, C["siem"], 3, "Sentinel (SIEM)", ["KQL analytics rules:", "password spray,", "privileged role assigned"])
box(xs[3], ytop, bw, bh, C["siem"], 4, "Incidents", ["Defender portal", "Triage, assign,", "classify, close"])

ybot = 1.1
box(xs[1], ybot, bw, bh, C["bi"], 6, "KQL → M query", ["Export from Logs", "Sign-ins + incidents", "Power Query in Desktop"])
box(xs[2], ybot, bw, bh, C["bi"], 7, "Power BI", ["Sign-in monitoring page", "Incident metrics page", "Published to the service"])
box(xs[3], ybot, bw, bh, C["resp"], 5, "SOAR playbook", ["Logic Apps", "Runs on the spray incident:", "notify / revoke sessions"])

mid = ytop + bh / 2
arrow(xs[0] + bw, mid, xs[1], mid, "diagnostic\nsetting", ly=mid + 0.12)
arrow(xs[1] + bw, mid, xs[2], mid, "scheduled\nKQL rules", ly=mid + 0.12)
arrow(xs[2] + bw, mid, xs[3], mid, "alerts →\nincidents", ly=mid + 0.12)
arrow(xs[3] + bw / 2, ytop, xs[3] + bw / 2, ybot + bh, "automation rule", lx=xs[3] + bw / 2 + 1.15, ly=(ytop + ybot + bh) / 2 - 0.15)
arrow(xs[1] + bw / 2, ytop, xs[1] + bw / 2, ybot + bh, "Log Analytics Reader", lx=xs[1] + bw / 2 + 1.2, ly=(ytop + ybot + bh) / 2 - 0.15)
arrow(xs[1] + bw, ybot + bh / 2, xs[2], ybot + bh / 2, "import", ly=ybot + bh / 2 + 0.12)

ax.text(0.45, 0.45, "Queries, write-ups and lessons learned: github.com/fa1829/sc300-sentinel-lab",
        fontsize=12, color=MUTED)

fig.savefig("pipeline.png", bbox_inches="tight", pad_inches=0.3, facecolor="white")
