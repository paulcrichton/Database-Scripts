#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
import numpy as np
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC



def get_tablespace_usage_metrics(database_connection):

    tablespace_useage_SQL="select * from dba_tablespace_usage_metrics order by 4"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=tablespace_useage_SQL, arraysize=20)
    tablespace_useage_SQL = pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    return tablespace_useage_SQL



def create_tablespace_report(user, pwd, host, port, database_name):
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    #Location, Size, Percent_Used_Space
    tablespace_usage_metrics=get_tablespace_usage_metrics(connection)

    connection.close()

    return tablespace_usage_metrics


def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    tablespace_usage_metrics=create_tablespace_report(user, pwd, host, port, database_name)

    print(tablespace_usage_metrics)

if __name__ == "__main__":
    main()