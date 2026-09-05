# scripts/update_snapshot.py
# ---------------------------------------------------------------------------
# Runs once a day via .github/workflows/update-snapshot.yml
#
# What it does, step by step:
#   1. Work out how long ago you were born ("22 years, 8 months, 15 days").
#   2. Open assets/dark_mode.svg and assets/light_mode.svg.
#   3. Find the two tagged elements inside them:
#        id="uptime_value"  -> the text itself
#        id="uptime_dots"   -> the leader dots before it (". Uptime: ..... ")
#   4. Overwrite both with today's numbers, re-padding the dots so the
#      value still lines up in the same column even when the day/month
#      counts change from 1 digit to 2 digits.
#   5. Save the files back. The GitHub Action then commits the change.
#
# Nothing else in the SVGs is touched -- Role, Institution, Toolchain, etc.
# stay exactly as you wrote them in build_card.py.
# ---------------------------------------------------------------------------
import datetime
from dateutil import relativedelta
from lxml import etree

# --- your birth date (change this only if it's ever wrong) ---
BIRTHDAY = datetime.date(2003, 12, 21)

# Must match the target_width used for every other line in build_card.py,
# so the "Uptime" row stays aligned with the rows above and below it.
DOT_TARGET_WIDTH = 17

SVG_FILES = ['assets/dark_mode.svg', 'assets/light_mode.svg']


def uptime_string(birthday):
    """Same wording style as before: '22 years, 8 months, 15 days'."""
    d = relativedelta.relativedelta(datetime.date.today(), birthday)

    def plural(n, word):
        return f"{n} {word}{'s' if n != 1 else ''}"

    return f"{plural(d.years, 'year')}, {plural(d.months, 'month')}, {plural(d.days, 'day')}"


def dots_for(label, value, total_width=DOT_TARGET_WIDTH):
    """Recreate the same dot-leader padding logic used in build_card.py."""
    prefix = f'. {label}:'
    dots_needed = max(2, total_width - len(prefix))
    return ' ' + ('.' * dots_needed) + ' '


def update_file(path, new_value, new_dots):
    tree = etree.parse(path)
    root = tree.getroot()

    value_el = root.find(".//*[@id='uptime_value']")
    dots_el = root.find(".//*[@id='uptime_dots']")

    if value_el is None or dots_el is None:
        raise RuntimeError(
            f"Could not find uptime_value / uptime_dots in {path}. "
            "Did the SVG get regenerated without those ids? "
            "Re-run scripts/build_card.py to restore them."
        )

    value_el.text = new_value
    dots_el.text = new_dots

    tree.write(path, encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    value = uptime_string(BIRTHDAY)
    dots = dots_for('Uptime', value)
    print('Today\'s uptime:', value)

    for path in SVG_FILES:
        update_file(path, value, dots)
        print('Updated', path)
