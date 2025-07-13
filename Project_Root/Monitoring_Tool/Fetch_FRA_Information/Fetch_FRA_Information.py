#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
import numpy as np
import logging 
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def get_parameter(database_connection, parameter):
    SQL = """select value from v$parameter where name=:parameter"""

    parameter_value=[]

    cursor = database_connection.cursor()
    for row in cursor.execute(SQL, [parameter]):            
        parameter_value = row

    return parameter_value

def get_FRA_configuration(connection):

    configuration=[]

    FRA_configuration_parameters=["db_recovery_file_dest", "db_recovery_file_dest_size"]

    for parameter in FRA_configuration_parameters:
        configuration.append(get_parameter(connection, parameter))
    
    configuration=dict(zip(FRA_configuration_parameters, configuration))

    configuration=pd.DataFrame(configuration)

    return configuration

def get_FRA_usage_metrics(database_connection):

    percent_used_SQL="SELECT ROUND((SPACE_USED - SPACE_RECLAIMABLE)/SPACE_LIMIT * 100, 1) AS PERCENT_FULL FROM V$RECOVERY_FILE_DEST"
    usage_breakdown_SQL="select * from v$recovery_area_usage"


    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=usage_breakdown_SQL, arraysize=20)
    usage_breakdown_df = pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    odf = None

    odf = database_connection.fetch_df_all(statement=percent_used_SQL, arraysize=20)
    percent_used_df = pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()
    
    return usage_breakdown_df, percent_used_df

def create_FRA_report(user, pwd, host, port, database_name):
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    #Location, Size, Percent_Used_Space
    fra_configuration=get_FRA_configuration(connection)

    fra_usage_breakdown, fra_percent_used=get_FRA_usage_metrics(connection)

    print(fra_usage_breakdown, fra_percent_used)

    connection.close()

    return fra_configuration


def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    fra_information=get_fra_information(user, pwd, host, port, database_name)

    print(fra_information)


if __name__ == "__main__":
    main()