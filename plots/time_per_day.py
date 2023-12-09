import json
import os
import pathlib
import re
import sys
import urllib.request
from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.style.use("fivethirtyeight")


def leaderboard_times(year, day):
    # load data from cache (if it exists)
    cache_path = pathlib.Path("results.json")
    if os.path.isfile(cache_path):
        results = json.loads(cache_path.read_text())
        if year not in results.keys():
            results.update({year: {}})
    else:
        results = {year: {}}

    if day not in results[year].keys() or results[year][day]["part_1"] == []:
        # load data from website if needed
        print(f"loading data for year {year}, day {day}")
        try:
            with urllib.request.urlopen(
                f"https://adventofcode.com/{year}/leaderboard/day/{day}"
            ) as f:
                html = f.read().decode("utf-8")

            matches = re.findall(r"leaderboard-time\">Dec \d+  (\d+:\d+:\d+)", html)
            to_secs = lambda t: (
                datetime.strptime(t, "%H:%M:%S") - datetime(1900, 1, 1)
            ).seconds
            p_1 = [to_secs(t) for t in matches[100:]]
            p_2 = [to_secs(t) for t in matches[:100]]

        except urllib.error.HTTPError:
            print("  cannot find data, leaderboard may not exist yet")
            p_1, p_2 = [], []

        results[year].update({day: {"part_1": p_1, "part_2": p_2}})
        # update cache file
        cache_path.write_text(json.dumps(results, sort_keys=True, indent=4))

    return results[year][day]


def style_violin(violin, color):
    for pc in violin["bodies"]:
        pc.set_facecolor(color)
        pc.set_edgecolor(color)
        pc.set_alpha(0.5)

    for pc in (violin["cbars"], violin["cmins"], violin["cmaxes"]):
        pc.set_edgecolor(color)
        pc.set_linewidth(3)


def plot_year(year):
    results_p1 = []
    results_p2 = []
    day_range = range(1, 25 + 1)
    for day in day_range:
        res = leaderboard_times(str(year), str(day))
        if res["part_1"] == []:
            continue
        results_p1.append([r / 60 for r in res["part_1"]])  # convert to minutes
        results_p2.append([r / 60 for r in res["part_2"]])

    c1 = "xkcd:navy green"
    c2 = "goldenrod"
    c3 = "xkcd:drab green"
    c4 = "xkcd:cherry"
    c5 = "xkcd:wine red"

    mpl.rcParams["grid.color"] = c3
    mpl.rcParams["axes.edgecolor"] = c1
    mpl.rcParams["text.color"] = c2
    mpl.rcParams["axes.labelcolor"] = c2
    mpl.rcParams["xtick.color"] = c2
    mpl.rcParams["ytick.color"] = c2
    mpl.rcParams["font.family"] = "cursive"
    mpl.rcParams["font.weight"] = "bold"
    mpl.rcParams["font.size"] = 20

    fig, ax = plt.subplots(constrained_layout=True, figsize=(16, 8))
    fig.suptitle(f"Advent of Code leaderboards {year}", fontsize=32)
    fig.set_facecolor(c1)

    pos_v1 = [p + 0.9 for p in range(len(results_p1))]  # slight offsets for violins
    pos_v2 = [p + 1.1 for p in range(len(results_p1))]

    v1 = ax.violinplot(results_p1, positions=pos_v1, showextrema=True)
    v2 = ax.violinplot(results_p2, positions=pos_v2, showextrema=True)
    style_violin(v1, c4)
    style_violin(v2, c5)
    ax.set_facecolor(c1)
    ax.set_xlabel("day")
    ax.set_ylabel("time [min]")
    ax.set_xticks(day_range)
    ax.set_yticks([x * 5 for x in range(int(ax.get_ybound()[1] // 5 + 1))])

    figname = f"leaderboards_{year}.png"
    fig.savefig(figname, facecolor=fig.get_facecolor())
    print(f"figure saved as {figname}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("provide year as argument:\n\tpython time_per_day.py 2023")
        raise SystemExit

    plot_year(sys.argv[-1])
