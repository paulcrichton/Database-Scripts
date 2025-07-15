#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def fetch_pdb_state(database_connection):
    
    pdb_state_SQL="select open_mode from v$PDBS"

    cursor = database_connection.cursor()
    cursor.execute(pdb_state_SQL)

    pdb_state = str(cursor.fetchone())
    
    return pdb_state


def fetch_cdb_state(database_connection):
    
    cdb_state_SQL="select open_mode from v$database"

    cursor = database_connection.cursor()
    cursor.execute(cdb_state_SQL)

    cdb_state = str(cursor.fetchone())
    
    return cdb_state

def gather_pdb_state(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    pdb_state = fetch_pdb_state(connection)

    connection.close()

    return pdb_state

def gather_cdb_state(user, pwd, host, port, database_name):
    
    connection = DCCC.create_connection(user, pwd, host, port, database_name)

    cdb_state = fetch_cdb_state(connection)

    connection.close()

    return cdb_state

###MAIN CODE FROM HERE
def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "ifslcdb"

    pdb_state = gather_pdb_state(user, pwd, host, port, database_name)
    cdb_state = gather_cdb_state(user, pwd, host, port, database_name)

    print(cdb_state, "\n\n", pdb_state)

if __name__ == "__main__":
    main() 
