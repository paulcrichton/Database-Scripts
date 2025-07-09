#!/usr/bin/env python3.9

from Fetch_CDB_PDB_Information.Fetch_CDB_PDB_States import gather_information_from_database as GIFD
import numpy as py

def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "IFSLCDB"




    
    cdb_states, pdb_states = GIFD(user, pwd, host, port, database_name)

    print(cdb_states, pdb_states)
    

if __name__ == "__main__":
    main()