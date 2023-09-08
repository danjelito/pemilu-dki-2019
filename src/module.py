import matplotlib.pyplot as plt
import seaborn as sns


def create_donut(x, labels, title):
    fig1, ax1 = plt.subplots(figsize=(5, 5), dpi=100)

    ax1.pie(
        x=x,
        labels=labels,
        autopct="%.0f%%",
        shadow=False,
        startangle=90,
        textprops={"fontsize": 14},
        colors=["#483838", "#42855B", "#90B77D", "#D2D79F"],
    )

    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set_title(
        title,
        pad=25,
        loc="center",
        fontdict={
            "fontsize": 18,
            "fontweight": "bold",
            "verticalalignment": "baseline",
            # 'horizontalalignment': "right"
        },
    )

    # draw circle
    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)
    # Equal aspect ratio ensures that pie is drawn as a circle
    ax1.axis("equal")
    ax1.set_facecolor("white")
    plt.tight_layout()
    plt.show()
