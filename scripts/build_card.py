# build_card.py
# ---------------------------------------------------------------------------
# One-time generator for Rahul's profile snapshot card (dark_mode.svg and
# light_mode.svg). Run this by hand whenever you want to change the ASCII
# portrait or any of the static text fields (Role, Institution, Toolchain...).
#
# The ONE field that is NOT static is "Uptime" -- that one is recomputed
# every day automatically by scripts/update_snapshot.py (see the GitHub
# Action). This script just needs to give that line an id so the daily
# script can find it later.
# ---------------------------------------------------------------------------
import datetime
from dateutil import relativedelta

with open('ascii_art.txt') as f:
    ascii_lines = f.read().split('\n')


def esc(s):
    """Escape characters that are special in XML/SVG text."""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def uptime_string(birthday):
    """'22 years, 8 months, 15 days' style string, same approach as Andrew's daily_readme()."""
    d = relativedelta.relativedelta(datetime.date.today(), birthday)
    def plural(n, word):
        return f"{n} {word}{'s' if n != 1 else ''}"
    return f"{plural(d.years,'year')}, {plural(d.months,'month')}, {plural(d.days,'day')}"


def justify(label, value, total_width=17):
    """
    Builds ('. Label:', ' .... ', value)
    All lines line up in the same visual column because the font is monospace.
    """
    prefix = f'. {label}:'
    dots_needed = max(2, total_width - len(prefix))
    dots = ' ' + ('.' * dots_needed) + ' '
    return prefix, dots, value


MAIN = [
    ('Role', 'Final-Year B.Tech EEE Undergraduate'),
    ('__UPTIME__', None),  # placeholder, filled in below with a live-updating id
    ('Institution', 'Aditya College of Engg. & Tech.'),
    ('Location', 'Surampalem, Andhra Pradesh, IN'),
    ('Focus', 'IoT / Embedded Systems / Power Systems'),
    ('Current', 'IoT Internship, 26_Cohort_3_IoT (Emertxe)'),
    ('Past Training', 'OJT, Nepal Electricity Authority'),
    ('Language', 'Japanese (JLPT N5), English (B2), Hindi, Nepali, Bhojpuri'),
    ('Target', 'Engineering roles, Japanese firms'),
]
TOOLS = [
    ('Design', 'Proteus, PICSimLab, MATLAB'),
    ('Embedded', 'Arduino, STM32, STM32CubeIDE'),
    ('IoT / Cloud', 'MQTT, ThingsBoard'),
]
CONTACT = [
    ('Email', 'sahurahulcoc@gmail.com'),
    ('LinkedIn', 'rahul-sahu-eee'),
    ('Status', 'Open to roles & collaborations'),
]

# --- your birth date, used only to compute the Uptime line ---
BIRTHDAY = datetime.date(2003, 12, 21)

THEMES = {
    'dark_mode': dict(
        bg='#0A1929', key='#FFB74D', value='#4FC3F7', dots='#3d5470',
        head='#e8f1fb', ascii='#7FA8C9', text='#c9d9e8',
    ),
    'light_mode': dict(
        bg='#EAF3FB', key='#B15E00', value='#0B5FA8', dots='#9fb4c8',
        head='#0A1929', ascii='#5C7A96', text='#12314a',
    ),
}

ASCII_X = 10
ASCII_FONT = 6
ASCII_LINE_H = 7
INFO_X = 360
INFO_FONT = 15
LINE_H = 20
TOP_Y_INFO = 30
TOP_Y_ASCII = 12


def build(theme_name):
    c = THEMES[theme_name]

    info_height = TOP_Y_INFO + (1 + len(MAIN) + 2 + len(TOOLS) + 2 + len(CONTACT)) * LINE_H
    ascii_height = TOP_Y_ASCII + len(ascii_lines) * ASCII_LINE_H
    height = max(info_height, ascii_height) + 20
    width = 1090

    svg = []
    svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
               f'font-family="Consolas, \'SFMono-Regular\', \'Courier New\', monospace">')
    svg.append('<style>')
    svg.append(f'.key {{fill:{c["key"]};}}')
    svg.append(f'.value {{fill:{c["value"]};}}')
    svg.append(f'.dots {{fill:{c["dots"]};}}')
    svg.append(f'.head {{fill:{c["head"]}; font-weight:bold;}}')
    svg.append(f'.ascii {{fill:{c["ascii"]};}}')
    svg.append('text, tspan {white-space:pre;}')
    svg.append('</style>')
    svg.append(f'<rect width="{width}" height="{height}" fill="{c["bg"]}" rx="15"/>')

    # --- left: ASCII portrait ---
    svg.append(f'<text x="{ASCII_X}" y="{TOP_Y_ASCII}" class="ascii" font-size="{ASCII_FONT}px">')
    for i, line in enumerate(ascii_lines):
        y = TOP_Y_ASCII + i * ASCII_LINE_H
        svg.append(f'<tspan x="{ASCII_X}" y="{y}">{esc(line)}</tspan>')
    svg.append('</text>')

    # --- right: info panel ---
    y = TOP_Y_INFO
    svg.append(f'<text x="{INFO_X}" y="{y}" font-size="{INFO_FONT}px" fill="{c["text"]}">')
    svg.append(f'<tspan x="{INFO_X}" y="{y}" class="head">rahul@eee</tspan>'
               f'<tspan class="dots"> -{"—"*38}-</tspan>')
    y += LINE_H
    for label, value in MAIN:
        if label == '__UPTIME__':
            prefix, dots, val = justify('Uptime', uptime_string(BIRTHDAY))
            svg.append(f'<tspan x="{INFO_X}" y="{y}" class="key">{esc(prefix)}</tspan>'
                       f'<tspan id="uptime_dots" class="dots">{esc(dots)}</tspan>'
                       f'<tspan id="uptime_value" class="value">{esc(val)}</tspan>')
        else:
            prefix, dots, val = justify(label, value)
            svg.append(f'<tspan x="{INFO_X}" y="{y}" class="key">{esc(prefix)}</tspan>'
                       f'<tspan class="dots">{esc(dots)}</tspan>'
                       f'<tspan class="value">{esc(val)}</tspan>')
        y += LINE_H

    y += LINE_H
    svg.append(f'<tspan x="{INFO_X}" y="{y}" class="head">- Toolchain</tspan>'
               f'<tspan class="dots"> -{"—"*36}-</tspan>')
    y += LINE_H
    for label, value in TOOLS:
        prefix, dots, val = justify(label, value)
        svg.append(f'<tspan x="{INFO_X}" y="{y}" class="key">{esc(prefix)}</tspan>'
                   f'<tspan class="dots">{esc(dots)}</tspan>'
                   f'<tspan class="value">{esc(val)}</tspan>')
        y += LINE_H

    y += LINE_H
    svg.append(f'<tspan x="{INFO_X}" y="{y}" class="head">- Contact</tspan>'
               f'<tspan class="dots"> -{"—"*38}-</tspan>')
    y += LINE_H
    for label, value in CONTACT:
        prefix, dots, val = justify(label, value)
        svg.append(f'<tspan x="{INFO_X}" y="{y}" class="key">{esc(prefix)}</tspan>'
                   f'<tspan class="dots">{esc(dots)}</tspan>'
                   f'<tspan class="value">{esc(val)}</tspan>')
        y += LINE_H

    svg.append('</text>')
    svg.append('</svg>')
    return '\n'.join(svg)


# Run this script from inside the scripts/ folder (e.g. "cd scripts && python build_card.py").
# It writes the finished cards straight into ../assets/, overwriting the old ones.
for theme in THEMES:
    out = build(theme)
    out_path = f'../assets/{theme}.svg'
    with open(out_path, 'w') as f:
        f.write(out)
    print(f'wrote {out_path}')
