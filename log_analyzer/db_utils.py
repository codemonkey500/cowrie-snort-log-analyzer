#!/usr/bin/env python3

"""
This script contains all methods which operate with the MySQL database.
"""

import logging
import os
import pandas as pd
from sqlalchemy import create_engine
import constants
import cryptography


def get_data_from_db(table):
    """
    This method will fetch data from the database into a dataframe.
    :param table: name of the wanted table
    :return: dataframe
    """
    df = pd.read_sql_query("SELECT * FROM " + table, get_db_connection())
    return df


def get_db_connection():
    """
    This method is used to establish a database connection.
    :return: database connection object
    """
    con = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}".format(user=constants.USER,
                                                                         pw=constants.PASSWORD,
                                                                         host=constants.HOST,
                                                                         db=constants.DATABASE))
    return con


def push_data_to_db(df, table, if_exists="append"):
    """
    This method is used to push a dataframe to the database.
    :param if_exists: Change default value to replace in order to overwrite
    :param df: dataframe which should be push to database
    :param table: name of the table to be created
    """
    connection = get_db_connection()
    df.to_sql(table, con=connection, if_exists=if_exists, chunksize=1000, index=False)
    logging.info("\t" + "Success: " + "\t" + "Data is no available in your database!")


def get_count_ssh_from_countries():
    """
    This method is used get the amount of SSH conncetions frome each country.
    Notice: This also includes SSH connections that did not go through the login process.
    :return: dataframe
    """
    connection = get_db_connection()

    result = pd.read_sql_query("""
                                SELECT COUNT(*) AS count, full_country_name
                                FROM logs.snort
                                GROUP BY full_country_name
                                ORDER BY count DESC;
                                """, connection)

    print_dataframe(result)
    print("\n" + "Total SSH connections: " + str(result["count"].sum()))
    save_df_as_file(result, "attack_countries.txt")

    return result


def get_ssh_connections_per_day():
    """
    This method is used to get the amount of SSH conncetions for each day.
    Notice: This also includes SSH connections that did not go through the login process.
    :return: dataframe
    """
    connection = get_db_connection()

    result = pd.read_sql_query("""
                                SELECT DATE_FORMAT(DATE(timestamp), "%%Y-%%m-%%d") AS timestamp, COUNT(*) AS count
                                FROM logs.snort
                                GROUP BY DATE_FORMAT(DATE(timestamp), "%%Y-%%m-%%d");""", connection)

    print_dataframe(result)
    save_df_as_file(result, "attacks_per_day.txt")

    return result


def save_df_as_file(df, name):
    """
    This method is used to save a dataframe as a file.
    :param df: dataframe to store as a file
    :param name: name of the generated file
    """
    df.to_csv(os.path.join(os.path.dirname(__file__), "data/db_query_files/" + name), index=False)
    logging.info("\t" + "\"" + name + "\"" + " stored in data/db_query_files")


def print_dataframe(df):
    """
    This method is used to print a dataframe.
    :param df: dataframe to print
    """
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df)
