#!/usr/bin/env python3.9

import oracledb
import numpy as np

def create_connection(username, user_password, hostname, port_number, service_name):
    sysdba=oracledb.AuthMode.SYSDBA

    cs = f'{hostname}:{port_number}/{service_name}'

    connection = oracledb.connect(user=username, password=user_password, dsn=cs,
                    stmtcachesize=30, mode=sysdba)
    
    return connection

def fetch_pdb_states(database_connection):
    pluggable_database_states=[]

    with database_connection:
        with database_connection.cursor() as cursor:
            for row in cursor.execute("select name, open_mode from v$PDBS"):
                
                pluggable_database_states.append(list(row))

    pluggable_database_states=np.asarray(pluggable_database_states)

    return pluggable_database_states

def fetch_cdb_states(database_connection):
    container_database_state=[]

    with database_connection:
        with database_connection.cursor() as cursor:
            for row in cursor.execute("select name, open_mode from v$database"):                
                container_database_state.append(list(row))

    container_database_state=np.asarray(container_database_state)

    return container_database_state

def gather_information_from_database(user, pwd, host, port, database_name):
    
    connection = create_connection(user, pwd, host, port, database_name)

    cdb_states = fetch_cdb_states(connection)

    connection = create_connection(user, pwd, host, port, database_name)

    pdb_states = fetch_pdb_states(connection)

    return cdb_states, pdb_states

###MAIN CODE FROM HERE
def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "IFSPCDB"

    gather_information_from_database(user, pwd, host, port, database_name)

if __name__ == "__main__":
    main() 


