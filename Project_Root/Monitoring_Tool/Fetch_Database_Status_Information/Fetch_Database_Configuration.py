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

    trace_dir_path = cursor.fetchone()
    
    return trace_dir_path

def create_alert_log_path(database_connection, db_name, trace_dir):

    alert_log_path=trace_dir + f'alert_{db_name}.log'

    return alert_log_path

def fetch_memory_configuration(database_connection):

    home_base_directories_SQL="SELECT NAME, (VALUE/1024/1024) AS VALUE FROM V$PARAMETER WHERE NAME IN ('pga_aggregate_limit','pga_aggregate_target','sga_max_size','sga_min_size','sga_target','memory_max_target','memory_target')"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=home_base_directories_SQL, arraysize=20)
    database_memory_parameters= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()



    return database_memory_parameters
    

def gather_configuration_information(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    database_home_base = fetch_home_base(connection)
    database_home_base = database_home_base.rename(columns={'DIRECTORY_NAME': "PARAMETER", "DIRECTORY_PATH": "VALUE"})

    trace_dir = fetch_trace_dir_location(connection)

    alert_log = create_alert_log_path(connection, database_name, trace_dir[2])

    trace_dir = pd.DataFrame([{"PARAMETER" : trace_dir[1].upper(), "VALUE": trace_dir[2]}])

    alert_log = pd.DataFrame([{"PARAMETER" : "ALERT LOG", "VALUE": alert_log}])

    memory_parameters=fetch_memory_configuration(connection)

    print(memory_parameters)

    database_configuration_information = pd.concat([database_home_base, trace_dir, alert_log], ignore_index=True)


    connection.close()

    return database_configuration_information

###MAIN CODE FROM HERE
def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    ##Set Pandas Display Options
    pd.set_option("expand_frame_repr", True)
    pd.set_option("max_colwidth", None)

    configuration_information = gather_configuration_information(user, pwd, host, port, database_name)

    print(configuration_information)


if __name__ == "__main__":
    main() 