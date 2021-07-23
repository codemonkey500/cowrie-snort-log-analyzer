#!/usr/bin/env python3

import logging
import pandas as pd
import constants
import os
import sys
from datetime import datetime
import log_analyzer
import pycountry
import db_utils
import numpy as np

logging.basicConfig(level=logging.INFO)


class SnortLogs:
    """
    A class to represent snort log data.

    It is primarily used to create a dataframe which can be uploaded to a MySQL database.
    """

    def __init__(self):
        """
        The class constructor creates a dataframe.
        Snort log file must be stored in its dedicated directory (data/snort/).
        """
        self.__lines_of_file = []
        try:
            file_path = os.path.join(os.path.dirname(__file__), constants.SNORT_LOGS_FILE_PATH)
            with open(file_path, "r", encoding="utf-8") as f:
                self.__lines_of_file = f.readlines()
            logging.info("\t" + "Found: " + "\"" + os.path.basename(file_path) + "\"")
            self.create_data_frame()
            self.add_ip_location()  # add ip locations
            self.add_full_country_name()  # add full country name
        except OSError as e:
            logging.error("\n" + "\"" + constants.SNORT_LOGS_FILE_NAME + "\"" +
                          " must be stored in the data/snort directory of the current project! File not found!")
            sys.exit(e)

    def create_data_frame(self):
        """
        This method is used to create a datafram from a log file.
        """
        index = 1
        log_every_n = 50
        upload_every_n = 3000
        df = pd.DataFrame()

        for line in self.__lines_of_file:
            d = {}
            split = line.split(" ")
            split = list(filter(None, split))  # Remove blanks from list
            for column in constants.SNORT_COLUMNS:
                if column == "index":
                    d[column] = index
                    index += 1
                elif column == "timestamp":
                    current_date = datetime.now()
                    current_year = current_date.strftime("%Y")
                    datetime_object = datetime.strptime(split[0], "%b")
                    month_number = datetime_object.month
                    if month_number < 10:
                        month_number = str(month_number).zfill(1)
                    timestamp = current_year + "-" + str(month_number) + "-" + split[1] + " " + split[2]
                    timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                    timestamp = datetime.strftime(timestamp, "%Y-%m-%d %H:%M:%S")
                    d[column] = timestamp
                elif column == "src_ip":
                    ip_port = split[10]
                    ip_port_split = ip_port.split(":")
                    d[column] = ip_port_split[0]
                    d["src_port"] = ip_port_split[1]
                elif column == "dst_ip":
                    ip_port = split[12].rstrip()
                    ip_port_split = ip_port.split(":")
                    d[column] = ip_port_split[0]
                    d["dst_port"] = ip_port_split[1]

            df_single_line = pd.DataFrame(d, index=[0])
            df = df.append(df_single_line, ignore_index=True)

            if index > 0:
                if (index % log_every_n) == 0:
                    logging.info("\t" + "Progress update: " + str(index) + " lines have been read")

            if (index % upload_every_n) == 0:
                db_utils.push_data_to_db(df, constants.SNORT_TABLE)
                df = pd.DataFrame()

        db_utils.push_data_to_db(df, constants.SNORT_TABLE)

    @staticmethod
    def add_ip_location():
        """
        This method is used to add the ip address location to the dataframe.
        """
        log_every_n = 50
        df = db_utils.get_data_from_db(constants.SNORT_TABLE)
        df["country"] = ""
        for index, row in df.iterrows():
            if index > 0:
                if (index % log_every_n) == 0:
                    logging.info("\t" + "Progress update: " + str(index) + " lines got ip location data")
            ip = df.iloc[index]["src_ip"]
            response = log_analyzer.create_geo_data(ip)
            df.at[index, "country"] = str(response.country_short)
        db_utils.push_data_to_db(df, constants.SNORT_TABLE, "replace")

    @staticmethod
    def add_full_country_name():
        """
        This method is used to add the full country name to the dataframe.
        """
        log_every_n = 50
        df = db_utils.get_data_from_db(constants.SNORT_TABLE)
        df["full_country_name"] = ""

        for index, row in df.iterrows():
            country = pycountry.countries.get(alpha_2=df.at[index, "country"])
            if country is not None:
                df.at[index, "full_country_name"] = country.name
            else:
                df.at[index, "full_country_name"] = np.nan
            if index > 0:
                if (index % log_every_n) == 0:
                    logging.info("\t" + "Progress update: " + str(index) + " lines got full country name")
        db_utils.push_data_to_db(df, constants.SNORT_TABLE, "replace")
