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

    home_base_directories_SQL="SELECT NAME, (VALUE/1024/1024/1024 || 'G') AS VALUE FROM V$PARAMETER WHERE NAME IN ('pga_aggregate_limit','pga_aggregate_target','sga_max_size','sga_min_size','sga_target','memory_max_target','memory_target')"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=home_base_directories_SQL, arraysize=20)
    database_memory_parameters= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    return database_memory_parameters

def fetch_full_file_locations(database_connection):
    full_file_paths_all_SQL="with rws as (SELECT 'CONTROL FILE' AS PARAMETER, VALUE AS PATH FROM V$PARAMETER WHERE NAME='control_files') SELECT 'CONTROL FILE' AS PARAMETER, regexp_substr (PATH, '[^,]+', 1, level) value from  rws connect by level <= length ( PATH	) - length ( replace ( PATH, ',' ) ) + 1 UNION SELECT 'DATAFILE PATH' AS PARAMETER, NAME AS PATH FROM V$DATAFILE UNION SELECT 'LOGFILE PATH' AS PARAMETER, MEMBER AS PATH FROM V$LOGFILE UNION SELECT 'TEMPFILE PATH' AS PARAMETER,NAME AS PATH FROM V$TEMPFILE;"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=full_file_paths_all_SQL, arraysize=20)
    full_file_paths_all= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    full_file_paths_all['PARAMETER']=full_file_paths_all['PARAMETER'].mask(full_file_paths_all['PARAMETER'].duplicated(),"")

    return full_file_paths_all

def fetch_file_locations(database_connection):

    database_file_parameters_SQL="SELECT NAME, VALUE FROM V$PARAMETER WHERE NAME IN ('db_create_file_dest','control_files','db_recovery_file_dest')"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=database_file_parameters_SQL, arraysize=20)
    database_file_parameters= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    actual_database_file_paths_SQL="SELECT DISTINCT 'DATAFILE PATH' AS PARAMETER, REGEXP_SUBSTR(NAME, '.*\/') AS VALUE from v$datafile UNION SELECT DISTINCT 'TEMPFILE PATH' AS PARAMETER, REGEXP_SUBSTR(NAME, '.*\/') AS VALUE from v$tempfile UNION SELECT DISTINCT 'LOGFILE PATH' AS PARAMETER, REGEXP_SUBSTR(MEMBER, '.*\/') AS VALUE from v$logfile"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=actual_database_file_paths_SQL, arraysize=20)
    actual_file_paths= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    actual_file_paths['PARAMETER']=actual_file_paths['PARAMETER'].mask(actual_file_paths['PARAMETER'].duplicated(),"")

    return database_file_parameters, actual_file_paths

def gather_physical_configuration_information(user, pwd, host, port, database_name):

    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    database_file_parameters, actual_file_paths=fetch_file_locations(connection)

    connection.close()

    return database_file_parameters

def gather_configuration_information(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    database_home_base = fetch_home_base(connection)
    database_home_base = database_home_base.rename(columns={'DIRECTORY_NAME': "PARAMETER", "DIRECTORY_PATH": "VALUE"})

    trace_dir = fetch_trace_dir_location(connection)

    alert_log = create_alert_log_path(connection, database_name, trace_dir[2])

    memory_parameters=fetch_memory_configuration(connection)
    memory_parameters = memory_parameters.rename(columns={'NAME': "PARAMETER"})

    trace_dir = pd.DataFrame([{"PARAMETER" : trace_dir[1].upper(), "VALUE": trace_dir[2]}])

    alert_log = pd.DataFrame([{"PARAMETER" : "ALERT LOG", "VALUE": alert_log}])

    database_configuration_information = pd.concat([database_home_base, trace_dir, alert_log, memory_parameters], ignore_index=True)

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