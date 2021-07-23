#!/usr/bin/env python3

"""
log_analyzer (MAIN)

This script allows the user to analyse cowrie and snort log data.
It should be run from console with different arguments.
Use the argument "--help" to see all the options.
"""
import argparse
import os
import sys
import IP2Location
import constants
import cowrie_logs
import db_utils
import plot_utils
import snort_logs


def create_geo_data(addr):
    """
    This method can be used to create geo data for a given ip address.
    :param addr: IP address (IPV4, IPV6)
    :return: IP2Location object
    """
    database = IP2Location.IP2Location(os.path.join(os.path.dirname(__file__), "data/IP2LOCATION.BIN"), "SHARED_MEMORY")
    res = database.get_all(addr)
    return res


if __name__ == '__main__':
    """
    This main method offers a CLI for optimal use on console.
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", help="Upload Cowrie-Logs to database", action="store_true")
    parser.add_argument("-b", help="Upload SNORT-Logs to database", action="store_true")
    parser.add_argument("-c", help="Plot: x=country, y=attack_count", action="store_true")
    parser.add_argument("-d", help="Plot x=datetime, y=SSH connections", action="store_true")
    parser.add_argument("-e", help="Get total SSH connections from each country", action="store_true")
    parser.add_argument("-f", help="Get total SSH connections per day", action="store_true")

    args = parser.parse_args()

    if args.a:
        cowrie = cowrie_logs.CowrieLogs()
    elif args.b:
        snort = snort_logs.SnortLogs()
    elif args.c:
        plot_utils.plot_attack_countries()
    elif args.d:
        plot_utils.plot_timeseries_of_attacks()
    elif args.e:
        db_utils.get_count_ssh_from_countries()
    elif args.f:
        db_utils.get_ssh_connections_per_day()
    else:
        parser.print_help(sys.stderr)
