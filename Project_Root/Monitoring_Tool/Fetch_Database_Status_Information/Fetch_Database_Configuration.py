#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def fetch_home_base(database_connection):
    
    home_base_directories_SQL="select directory_name, directory_path from all_directories where directory_name in ('ORACLE_BASE', 'ORACLE_HOME')"

    
    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=home_base_directories_SQL, arraysize=20)
    database_home_base= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()
    
    return database_home_base

def fetch_trace_dir_location(database_connection):
    trace_dir_path_SQL="select * from v$diag_info where NAME = 'Diag Trace'"

    cursor = database_connection.cursor()
    cursor.execute(trace_dir_path_SQL)

    trace_dir_path = str(cursor.fetchone())
    
    return trace_dir_path

def create_alert_log_path(database_connection, db_name, trace_dir):

    database_connection

def gather_configuration_information(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    database_home_base = fetch_home_base(connection)
    database_home_base = database_home_base.rename(columns={0: "PARAMETER", 1: "VALUE"})

    trace_dir = fetch_trace_dir_location(connection)

    alert_log = create_alert_log_path(connection, database_name, trace_dir)

    trace_dir = pd.DataFrame([{"PARAMETER" : trace_dir[1], "VALUE": trace_dir[2]}])

    database_configuration_information = pd.concat([database_home_base, trace_dir], ignore_index=True)

    connection.close()

    return database_configuration_information

###MAIN CODE FROM HERE
def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    configuration_information = gather_configuration_information(user, pwd, host, port, database_name)

    print(configuration_information)


if __name__ == "__main__":
    main() 