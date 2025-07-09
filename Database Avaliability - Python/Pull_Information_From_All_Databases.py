#!/usr/bin/env python3.9

from Fetch_CDB_PDB_Information.Fetch_CDB_PDB_States import gather_information_from_database as GIFD
from Fetch_CDB_PDB_Information.Fetch_Database_Home_And_SID import create_db_name_home_array as CDNHA
import numpy as py

def main():
    
    cdb_states, pdb_states = get_states()

    print(cdb_states, pdb_states)
    
def create_login_details(name):
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = name

    return user, pwd, host, port, database_name

def get_states():
    db_arr, oh_arr = CDNHA()
    
    for db_name in db_arr:
        user, pwd, host, port, database_name=create_login_details(db_name)

        try: 
            cdb_states, pdb_states = GIFD(user, pwd, host, port, database_name)
        except:
            print("-----------------------------------------\n")
            print("database", db_name, "could not be queried")
            print("-----------------------------------------\n")
        
            next
    
    return cdb_states, pdb_states

if __name__ == "__main__":
    main()