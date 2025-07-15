#!/usr/bin/env python3.9

import oracledb
import pyarrow
import pandas as pd
from Monitoring_Tool.Database_Connections import Create_Connection as DCCC

def check_pdb_or_cdb(database_connection):
    
    check_db_type_SQL="select case sys_context('USERENV', 'CON_ID') when '1' then 'CDB' else 'PDB' end as cdb_or_pdb from dual"

    cursor = database_connection.cursor()
    cursor.execute(check_db_type_SQL)

    database_type = str(cursor.fetchone())
    
    
    return database_type

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

