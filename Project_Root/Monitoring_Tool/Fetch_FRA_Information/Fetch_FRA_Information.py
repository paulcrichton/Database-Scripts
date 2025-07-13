#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
import numpy as np
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def get_parameter(database_connection, parameter):
    SQL = """select value from v$parameter where name=:parameter"""

    cursor = database_connection.cursor()
    for row in cursor.execute(SQL, [parameter]):            
        parameter_value = list(row)

    return parameter_value

def get_FRA_configuration(connection):

    configuration=[]
    FRA_configuration_parameters=[["db_recovery_file_dest"], ["db_recover_file_dest_size"]]

    for parameter in FRA_configuration_parameters:
        configuration.append(get_parameter(connection, parameter))
    
    pd.DataFrame(data=configuration, columns=FRA_configuration_parameters)

    return configuration

def get_FRA_Percent_Used(database_connection):

    SQL="select * from v$recovery_area_usage"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=SQL, arraysize=1000)
    df = pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()

    return df

def get_fra_information(user, pwd, host, port, database_name):
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    #Location, Size, Percent_Used_Space
    fra_information=[]
    fra_information=get_FRA_configuration(connection)
    metrics_df=get_FRA_Percent_Used(connection)

    connection.close()

    return fra_information


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