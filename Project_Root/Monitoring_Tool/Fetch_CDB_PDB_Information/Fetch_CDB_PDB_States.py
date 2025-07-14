#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def fetch_pdb_states(database_connection):

    pluggable_database_states_SQL="select name, open_mode from v$PDBS"
    
    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=pluggable_database_states_SQL, arraysize=20)
    pluggable_database_states= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()
    
    return pluggable_database_states

def fetch_cdb_states(database_connection):
    
    container_database_states_SQL="select name, open_mode from v$PDBS"
    
    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    odf = database_connection.fetch_df_all(statement=container_database_states_SQL, arraysize=20)
    container_database_states= pyarrow.Table.from_arrays(odf.column_arrays(), names=odf.column_names()).to_pandas()
    
    return container_database_states

def gather_information_from_database(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    cdb_states = fetch_cdb_states(connection)
    pdb_states = fetch_pdb_states(connection)

    connection.close()

    return cdb_states, pdb_states

###MAIN CODE FROM HERE
def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    cdb_states, pdb_states = gather_information_from_database(user, pwd, host, port, database_name)

    print(cdb_states, pdb_states)

if __name__ == "__main__":
    main() 


