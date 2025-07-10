#!/usr/bin/env python3.9

from Fetch_CDB_PDB_Information.Fetch_CDB_PDB_States import gather_information_from_database as GIFD
from Fetch_CDB_PDB_Information.Fetch_Database_Home_And_SID import create_db_name_home_array as CDNHA
import Database_Connections.Create_Connection as DCCC 
import numpy as np




def get_FRA_location(database_connection):
    
    fra_location=[]

    with database_connection:
        with database_connection.cursor() as cursor:
            for row in cursor.execute("select vaule from v$parameter where name 'db_recovery_file_dest'"):                
                fra_location = list(row)

    fra_location=np.asarray(fra_location)

    return fra_location

def get_fra_information(user, pwd, host, port, database_name):
    connection = DCCC(user, pwd, host, port, database_name)
    
    #Location, Size, Percent_Used_Space
    fra_information=[]

    fra_information=np.append(get_FRA_location(connection))

    print(fra_information)


def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "name"



if __name__ == "__main__":
    main()