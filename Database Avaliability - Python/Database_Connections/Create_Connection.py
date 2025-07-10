#!/usr/bin/env python3.9

import oracledb
import numpy as np

def create_connection(username, user_password, hostname, port_number, service_name):
    sysdba=oracledb.AuthMode.SYSDBA

    cs = f'{hostname}:{port_number}/{service_name}'

    connection = oracledb.connect(user=username, password=user_password, dsn=cs,
                    stmtcachesize=30, mode=sysdba)
    
    return connection


def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "IFSPCDB"

    connection = create_connection(user, pwd, host, port, database_name)

if __name__ == "__main__":
    main() 