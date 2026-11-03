"""Generates the SVG graphics used by the profile README into assets/."""
import math
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).parent / "assets"
OUT.mkdir(exist_ok=True)

BG, PANEL, BORDER = "#192C25", "#21382F", "#687764"
SAGE, CORAL, CREAM, MUTED = "#BFD6CA", "#E47761", "#DCE0C7", "#9AA590"
MONO = "ui-monospace,'SF Mono','Cascadia Code',Consolas,Menlo,monospace"
SANS = "-apple-system,'Segoe UI',Helvetica,Arial,sans-serif"


def text(x, y, s, size, fill, family=MONO, weight=400, anchor="start", spacing=0):
    return (
        f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}">{escape(s)}</text>'
    )


def bars(x, base, count, gap, width, max_h, color, seed=1):
    """Equaliser bars that loop forever; each bar gets its own rhythm."""
    out = []
    for i in range(count):
        a = 0.25 + 0.75 * abs(math.sin((i + seed) * 1.7))
        b = 0.2 + 0.8 * abs(math.cos((i + seed) * 0.9))
        h1, h2 = round(max_h * a), round(max_h * b)
        dur = round(1.1 + (i * 7 % 10) / 10, 1)
        px = x + i * gap
        out.append(
            f'<rect x="{px}" y="{base - h1}" width="{width}" height="{h1}" rx="{width / 2}" fill="{color}">'
            f'<animate attributeName="height" values="{h1};{h2};{h1}" dur="{dur}s" repeatCount="indefinite"/>'
            f'<animate attributeName="y" values="{base - h1};{base - h2};{base - h1}" dur="{dur}s" repeatCount="indefinite"/>'
            f"</rect>"
        )
    return "".join(out)


def save(name, w, h, label, body):
    (OUT / name).write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
        f'role="img" aria-label="{escape(label)}">{body}</svg>\n',
        encoding="utf-8",
    )


def hero():
    w, h = 1000, 280
    b = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="14" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>'
    b += f'<path d="M1 46V15a14 14 0 0 1 14-14h{w-30}a14 14 0 0 1 14 14v31z" fill="{PANEL}"/>'
    b += f'<line x1="1" y1="46" x2="{w-1}" y2="46" stroke="{BORDER}"/>'
    for i, c in enumerate((CORAL, CREAM, SAGE)):
        b += f'<circle cx="{28 + i * 22}" cy="24" r="6" fill="{c}"/>'
    b += text(w / 2, 29, "MAHMOOD_OS // ADOXCOL.SYS  v2.4.0", 13, MUTED, anchor="middle", spacing=1)
    b += text(w - 24, 29, "DHAKA, BD", 13, MUTED, anchor="end", spacing=1)
    b += text(44, 96, "adoxcol@mahmood-os:~$ whoami", 16, CORAL)
    b += text(44, 158, "Mahmood Tauhidul", 54, SAGE, SANS, 700)
    b += text(44, 198, "Full-Stack AI Developer & Systems Maker", 22, CREAM, SANS, 500)
    b += text(44, 236, "Scalable web platforms, local desktop software, and LLM systems.", 15, MUTED, SANS)
    b += bars(690, 244, 21, 13, 7, 170, SAGE, 2)
    b += f'<line x1="690" y1="250" x2="956" y2="250" stroke="{CORAL}" stroke-width="2"/>'
    save("hero.svg", w, h, "Mahmood Tauhidul, Full-Stack AI Developer and Systems Maker", b)


def section(name, index, title):
    w, h = 1000, 54
    b = f'<rect width="46" height="34" y="10" rx="7" fill="{CORAL}"/>'
    b += text(23, 33, index, 16, BG, weight=700, anchor="middle")
    b += text(60, 34, title, 19, CORAL, weight=700, spacing=1.5)
    b += bars(930, 44, 6, 11, 6, 30, CORAL, int(index))
    save(name, w, h, f"Section {index}: {title}", b)


def card(name, title, kind, desc, chips, accent, seed):
    w, h = 490, 230
    b = f'<rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{BORDER}" stroke-width="2"/>'
    b += f'<rect x="1" y="1" width="8" height="{h-2}" rx="4" fill="{accent}"/>'
    b += text(30, 36, kind, 12, accent, weight=700, spacing=1.5)
    b += text(30, 74, title, 29, SAGE, SANS, 700)
    for i, line in enumerate(desc):
        b += text(30, 108 + i * 23, line, 15, CREAM, SANS)
    x = 30
    for chip in chips:
        cw = 16 + len(chip) * 7.6
        b += f'<rect x="{x}" y="176" width="{cw}" height="28" rx="6" fill="{PANEL}" stroke="{BORDER}"/>'
        b += text(x + cw / 2, 195, chip, 12.5, SAGE, anchor="middle")
        x += cw + 8
    b += bars(w - 92, 58, 6, 11, 6, 34, accent, seed)
    save(name, w, h, f"{title}: {' '.join(desc)}", b)


hero()
section("s-stats.svg", "01", "SYSTEM_TELEMETRY.LOG")
section("s-audio.svg", "02", "NOW_PLAYING")
section("s-projects.svg", "03", "FEATURED_EXECUTABLES")
section("s-stack.svg", "04", "HARDWARE & SOFTWARE MATRIX")
section("s-snake.svg", "05", "CONTRIBUTION_GRID_SNAKE")
section("s-contact.svg", "06", "INITIATE_COMMUNICATION")

card("velo.svg", "Velo", "DOWNLOAD MANAGER",
     ["Open-source download manager: Windows desktop and", "browser integration, plus a Linux and macOS CLI."],
     ["Go", "Windows", "Linux", "macOS"], CORAL, 3)
card("studio.svg", "Studio", "DESKTOP AUDIO",
     ["A fast, customizable desktop music player with a", "local library first and self-hosted streaming."],
     ["Flutter", "Riverpod", "SQLite", "libmpv"], SAGE, 5)
card("uniplan.svg", "UniPlan", "ACADEMIC PLANNING",
     ["Real-time academic roadmaps, degree audits, and", "course path visualization for students."],
     ["Next.js", "TypeScript", "WebSockets", "Supabase"], SAGE, 7)
card("wellness.svg", "MentalWellness", "AI COMPANION",
     ["An AI companion exploring calm, non-clinical", "reflective check-ins and empathetic interaction."],
     ["Next.js", "React", "Tailwind", "OpenAI"], CORAL, 9)
card("hospital.svg", "Hospital CMS", "PUBLIC PORTAL",
     ["High-traffic portal for a national institute's", "medical services and announcements."],
     ["React", "Node.js", "Express", "PayloadCMS"], CORAL, 11)
card("tonekith.svg", "ToneKith", "MUSIC COMMUNITY",
     ["A community-based tone library for sharing", "and discovering sounds."],
     ["TypeScript"], SAGE, 13)
