#!/usr/bin/env python3

import logging

import pandas
import pandas as pd
import numpy as np
import constants
import os
import sys
from datetime import datetime
import glob
import log_analyzer
import db_utils

logging.basicConfig(level=logging.INFO)


class CowrieLogs:
    """
    A class to represent cowrie log data.

    It is primarily used to create a dataframe which can be uploaded to a MySQL database.
    """

    def __init__(self):
        """
        The class constructor creates a dataframe.
        Cowrie log files must be stored in its dedicated directory (data/cowrie/).
        The method will read in all the files stored in this particular directory.
        """

        self.__index = 1
        try:
            path = os.path.join(os.path.dirname(__file__), constants.COWRIE_LOGS_FILE_PATH)
            paths = sorted(glob.glob(path))
            if len(paths) == 0:
                raise OSError
            for file_path in paths:
                with open(file_path) as f:
                    logging.info("\t" + "Found: " + "\"" + os.path.basename(file_path) + "\"")
                    lines_of_file = f.readlines()
                    self.create_data_frame(lines_of_file)
        except OSError as e:
            logging.error(
                "Files must be stored in the data/cowrie directory of the current project! Files not found!")
            sys.exit(e)

    def get_index(self):
        return self.__index

    def raise_index(self):
        self.__index += 1

    def create_data_frame(self, lines):
        """
        This method is used to create a dataframe from a list of lines which were read in from a log file.
        :param lines: List of lines from a log file.
        """
        df = pd.DataFrame()
        log_every_n = 50
        upload_every_n = 3000
        lines_of_file = 1
        for line in lines:
            d = {}
            for segment in line.split(",\""):
                if ":" not in segment:
                    continue
                split = segment.split(":", 1)
                key = split[0].split("\"")
                if len(key) == 3:  # Special behavior for first segment
                    key = key[1]
                else:
                    key = key[0]
                if key not in constants.COWRIE_COLUMNS:
                    continue
                if "\"" in split[1]:  # Remove double quotes
                    value = split[1].split("\"")
                    value = value[1]
                else:
                    value = split[1]
                d[key] = value
            geo_data = log_analyzer.create_geo_data(d.get("src_ip"))
            for column in constants.COWRIE_COLUMNS:  # Add index column as primary key
                if column not in d:
                    if column == "index":
                        d[column] = self.get_index()
                        self.raise_index()
                    elif column == "country":
                        if geo_data is not None:
                            d[column] = str(geo_data.country_short)
                        else:
                            d[column] = np.nan
                    else:
                        d[column] = np.nan  # Fill missing column values
            timestamp = d.get("timestamp")  # Format timestamp
            date_time_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
            timestamp = date_time_object.strftime("%Y-%m-%d %H:%M:%S")
            d["timestamp"] = timestamp
            df_single_line = pd.DataFrame(d, index=[0])
            df_single_line = df_single_line.reindex(columns=constants.COWRIE_COLUMNS)
            df = df.append(df_single_line)

            if (lines_of_file % log_every_n) == 0:
                logging.info("\t" + "Progress update: " + str(lines_of_file) + " lines have been read")
            lines_of_file += 1

            if (lines_of_file % upload_every_n) == 0:
                db_utils.push_data_to_db(df, constants.COWRIE_TABLE)
                df = pd.DataFrame()

        db_utils.push_data_to_db(df, constants.COWRIE_TABLE)
