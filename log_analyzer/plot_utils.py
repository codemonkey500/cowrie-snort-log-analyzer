#!/usr/bin/env python3

"""
This script contains all the methods which are able to plot data.
"""

from matplotlib import pyplot as plt
import matplotlib.dates as mdates
import db_utils
from datetime import datetime
import pandas as pd
import constants


def plot_attack_countries():
    """
    This method is used to plot the top 5 countries on the x-axis and the amount of attacks on the y-axis.
    """
    df = db_utils.get_count_ssh_from_countries()

    df = df.head(5)

    ax = df.plot.bar(x="full_country_name", y="count", rot=0)
    ax.get_legend().remove()
    ax.yaxis.grid()

    plt.xlabel("Nationalstaaten")
    plt.ylabel("Zugriffe auf Honeypot")
    plt.show()


def plot_timeseries_of_attacks():
    """
    This method is used to plot a timeseries on the x-axis and the amount of attacks on the y-axis.
    The output should visualize the amount of attacks on each day druing the logging process.
    """
    df = db_utils.get_ssh_connections_per_day()

    months = mdates.MonthLocator()  # every month
    days = mdates.DayLocator()
    formatter = mdates.DateFormatter("%Y-%m-%d")

    fig, ax = plt.subplots()

    ax.plot([datetime.strptime(d, "%Y-%m-%d").date() for d in df["timestamp"]], df["count"], color="black")

    # format the ticks
    # ax.xaxis.set_major_locator(months)
    ax.xaxis.set_major_locator(days)
    ax.xaxis.set_major_formatter(formatter)
    ax.set_xlim([pd.to_datetime(constants.START_DATE), pd.to_datetime(constants.END_DATE)])

    ax.grid(True)

    # rotates and right aligns the x labels
    fig.autofmt_xdate()
    plt.xlabel("Datum")
    plt.ylabel("Anzahl der SSH Verbindungen")
    # fig.suptitle("Optional", fontsize=16)
    plt.show()
