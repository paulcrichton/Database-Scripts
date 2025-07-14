
import oracledb
import pyarrow
import pandas as pd
import numpy as np
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def get_pluggable_names(database_connection):

    pluggable_names_SQL="select name from v$PDBS"
    
    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=pluggable_names_SQL, arraysize=20)
    pluggable_names= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()
    
    return pluggable_names

def create_pluggable_names_report(user, pwd, host, port, database_name):
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    #Location, Size, Percent_Used_Space
    pluggable_names=get_pluggable_names(connection)

    connection.close()

    return pluggable_names

def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    pluggable_names=create_pluggable_names_report(user, pwd, host, port, database_name)

    print(pluggable_names)

if __name__ == "__main__":
    main()