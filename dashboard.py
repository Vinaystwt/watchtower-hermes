import curses
import time
import os
import requests

SKILLS_DIR = "skills"
LOG_FILE = "memory/learning_curve.log"


def read_skills():
    if not os.path.exists(SKILLS_DIR):
        return []
    return sorted(os.listdir(SKILLS_DIR))


def read_learning_curve():
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE) as f:
        return [line.strip() for line in f.readlines()]


def fetch_metrics():
    try:
        r = requests.get("http://localhost:5001/health", timeout=2)
        return r.json()
    except:
        return {"memory_percent": 0, "cpu_percent": 0}


def draw_bar(value, width=20):
    filled = int((value / 100) * width)
    return "█" * filled + "░" * (width - filled)


def dashboard(stdscr):

    curses.curs_set(0)

    while True:

        stdscr.clear()

        height, width = stdscr.getmaxyx()

        panel_width = width // 3

        skills = read_skills()
        logs = read_learning_curve()
        metrics = fetch_metrics()

        # LEFT PANEL — SKILLS
        stdscr.addstr(0, 0, "SKILL LIBRARY", curses.A_BOLD)

        for i, skill in enumerate(skills):

            marker = ""
            if i == len(skills) - 1:
                marker = " ← NEW"

            stdscr.addstr(i + 2, 0, f"{skill}{marker}")

        stdscr.addstr(len(skills) + 4, 0, f"{len(skills)} self-authored skills")

        # MIDDLE PANEL — LEARNING CURVE
        mid_x = panel_width

        stdscr.addstr(0, mid_x, "LEARNING CURVE", curses.A_BOLD)

        for i, line in enumerate(logs[-10:]):
            stdscr.addstr(i + 2, mid_x, line)

        # Safe ratio calculation
        if len(logs) >= 2:

            try:

                first = float(logs[0].split("|")[2].replace("s", "").strip())
                second = float(logs[1].split("|")[2].replace("s", "").strip())

                if second > 0:
                    ratio = round(first / second)

                    stdscr.addstr(
                        height - 2,
                        mid_x,
                        f"★ {ratio}× faster after learning",
                    )

            except:
                pass

        # RIGHT PANEL — LIVE METRICS
        right_x = panel_width * 2

        stdscr.addstr(0, right_x, "LIVE METRICS", curses.A_BOLD)

        mem = metrics.get("memory_percent", 0)
        cpu = metrics.get("cpu_percent", 0)

        mem_bar = draw_bar(mem)
        cpu_bar = draw_bar(cpu)

        stdscr.addstr(2, right_x, f"Memory {mem}%")
        stdscr.addstr(3, right_x, mem_bar)

        stdscr.addstr(5, right_x, f"CPU {cpu}%")
        stdscr.addstr(6, right_x, cpu_bar)

        stdscr.addstr(height - 1, 0, "Press Q to quit")

        stdscr.refresh()

        stdscr.timeout(3000)

        key = stdscr.getch()

        if key == ord("q") or key == ord("Q"):
            break


def main():
    curses.wrapper(dashboard)


if __name__ == "__main__":
    main()