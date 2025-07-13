#!/usr/bin/env python3.9

import oracledb
import pyarrow
import numpy as np
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def get_FRA_location(database_connection):
    
    fra_location=[]

    cursor = database_connection.cursor()
    for row in cursor.execute("select value from v$parameter where name = 'db_recovery_file_dest'"):                
        fra_location = list(row)

    return fra_location

def get_FRA_Size(database_connection):
    
    SQL="select value from v$parameter where name = 'db_recovery_file_dest_size'"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=SQL, arraysize=1000)
    df = pyarrow.Table.from_arrays(
    odf.column_arrays(), names='db_recovery_file_dest_size').to_pandas()

    return df

def get_FRA_Percent_Used(database_connection):

    SQL="select * from v$recovery_area_usage"

    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=SQL, arraysize=1000)
    df = pyarrow.Table.from_arrays(
    odf.column_arrays(), names=odf.column_names()).to_pandas()

    return df

def get_fra_information(user, pwd, host, port, database_name):
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    #Location, Size, Percent_Used_Space
    fra_information=[]

    fra_information=get_FRA_location(connection)
    fra_information.append(get_FRA_Size(connection))
    fra_information.append(get_FRA_Percent_Used(connection))

    df=get_FRA_Percent_Used(connection)

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