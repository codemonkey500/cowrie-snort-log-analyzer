#!/usr/bin/env python3

"""
This script only consists of constants to use in this project.
"""

COWRIE_LOGS_FILE_PATH = "data/cowrie/*"
COWRIE_LOGS_FILE_NAME = "cowrie.json"

SNORT_LOGS_FILE_PATH = "data/snort/snort-alert.log"
SNORT_LOGS_FILE_NAME = "snort-alert.log"

HOST = "localhost"
USER = ""  # Add you db username here
PASSWORD = ""  # Add your db password here
DATABASE = ""  # Add your db name here
COWRIE_TABLE = ""  # Add name of cowrie table here
SNORT_TABLE = ""  # Add name of snort table here

START_DATE = "2021-06-02"
END_DATE = "2021-06-25"

COWRIE_COLUMNS = ["index", "eventid", "message", "sensor", "timestamp", "src_ip", "session", "username", "fingerprint",
                  "key",
                  "type", "password", "filename", "outfile", "input",
                  "is_new", "positives", "total", "src_port", "dst_ip", "dst_port", "version",
                  "duration", "size", "duplicate", "name",
                  "value", "country"]

SNORT_COLUMNS = ["index", "timestamp", "src_ip", "src_port", "dst_ip", "dst_port", "country", "full_country_name"]
