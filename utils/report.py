import io
from datetime import datetime


def generate_text_report(
    name: str,
    role: str,
    experience: str,
    match_score: float,
    readiness: dict,
    strengths: list,
    missing_skills: list,
    roadmap: list,
    timeline: str,
) -> str:
    """Generate a plain-text downloadable report."""
    now = datetime.now().strftime("%B %d, %Y")
    user_label = f"for {name}" if name else ""

    lines = [
        "=" * 64,
        "  SKILLSYNC AI — SKILL GAP ANALYSIS REPORT",
        "=" * 64,
        f"  Date         : {now}",
    ]
    if name:
        lines.append(f"  Candidate    : {name}")
    lines += [
        f"  Target Role  : {role}",
        f"  Experience   : {experience}",
        "=" * 64,
        "",
        "  SUMMARY",
        "  " + "-" * 30,
        f"  Match Score   :  {match_score}%",
        f"  Readiness     :  {readiness['score']}%  ({readiness['label']})",
        f"  Est. Timeline :  {timeline}",
        "",
        "  EXISTING STRENGTHS",
        "  " + "-" * 30,
    ]
    for i, s in enumerate(strengths, 1):
        lines.append(f"  {i:>2}. {s.title()}")

    lines += [
        "",
        "  SKILL GAPS TO ADDRESS",
        "  " + "-" * 30,
    ]
    for i, s in enumerate(missing_skills[:10], 1):
        lines.append(f"  {i:>2}. {s.title()}")

    lines += [
        "",
        "  PERSONALIZED LEARNING ROADMAP",
        "  " + "-" * 30,
    ]
    priority_order = {"Critical": 1, "High": 2, "Medium": 3, "Low": 4}
    sorted_roadmap = sorted(roadmap, key=lambda x: priority_order.get(x["priority"], 5))
    for item in sorted_roadmap:
        lines += [
            f"  [{item['priority'].upper()}] {item['skill']}",
            f"    Resource  : {item['resource']}",
            f"    Duration  : {item['duration']}",
            "",
        ]

    lines += [
        "=" * 64,
        "  Total Estimated Learning Time:  " + timeline,
        "=" * 64,
        "",
    ]
    return "\n".join(lines)
