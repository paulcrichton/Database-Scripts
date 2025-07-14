#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def check_pdb_or_cdb(database_connection):
    
    container_database_states_SQL="select case sys_context('USERENV', 'CON_ID') when '1' then 'CDB' else 'PDB' end as cdb_or_pdb from dual"
    
    # Get an OracleDataFrame.
    # Adjust arraysize to tune the query fetch performance
    cursor = database_connection.cursor()
    cursor.execute(container_database_states_SQL)

    container_database_states = str(cursor.fetchone())
    
    
    return container_database_states

def cdb_or_pdb(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    cdb_or_pdb_db_value = check_pdb_or_cdb(connection)

    connection.close()

    print(cdb_or_pdb_db_value)

    if "CDB" in cdb_or_pdb_db_value:
        return "CDB"
    else:
        return "PDB"


###MAIN CODE FROM HERE
def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    cbd_or_pdb_bool = cdb_or_pdb(user, pwd, host, port, database_name)

    print(cbd_or_pdb_bool)

if __name__ == "__main__":
    main() 

