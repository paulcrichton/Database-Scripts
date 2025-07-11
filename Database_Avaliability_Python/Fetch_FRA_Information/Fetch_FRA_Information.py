#!/usr/bin/env python3.9

import oracledb
import numpy as np
from ..Database_Connections import Create_Connection as DCCC

def get_FRA_location(database_connection):
    
    fra_location=[]

    with database_connection:
        with database_connection.cursor() as cursor:
            for row in cursor.execute("select value from v$parameter where name = 'db_recovery_file_dest'"):                
                fra_location = list(row)

    fra_location=np.asarray(fra_location)

    return fra_location

def get_fra_information(user, pwd, host, port, database_name):
    connection = DCCC.create_connection(user, pwd, host, port, database_name)
    
    #Location, Size, Percent_Used_Space
    fra_information=[]

    fra_information=np.append(get_FRA_location(connection))

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