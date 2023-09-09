import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import opinionated


def label_point(x, y, val, ax):
    a = pd.concat({"x": x, "y": y, "val": val}, axis=1)
    for i, point in a.iterrows():
        ax.text(
            point["x"],
            point["y"],
            str(point["val"]),
            alpha=0.75,
            ha="center",
            va="center",
        )


def create_donut(x, labels, title=None, subtitle=None):
    fig1 = plt.figure(figsize=(12, 8))
    ax1 = fig1.add_axes((0.02, 0.325, 0.5, 0.5))

    ax1.pie(
        x=x,
        labels=labels,
        autopct="%.1f%%",
        pctdistance=0.72,
        shadow=False,
        startangle=90,
        textprops={"fontsize": 14},
    )

    ax1.axis("equal")
    if title is not None and subtitle is not None:
        opinionated.set_title_and_suptitle(title, subtitle)

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.50, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    ax1.axis("equal")
    ax1.set_facecolor("white")

    plt.show()
