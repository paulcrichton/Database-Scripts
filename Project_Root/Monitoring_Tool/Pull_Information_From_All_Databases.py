#!/usr/bin/env python3.9

from Monitoring_Tool.Fetch_CDB_PDB_Information.Fetch_CDB_PDB_States import gather_information_from_database as GIFD
from Monitoring_Tool.Fetch_CDB_PDB_Information.Fetch_Database_Home_And_SID import create_db_name_home_array as CDNHA
from Monitoring_Tool.Fetch_FRA_Information.Fetch_FRA_Information import get_fra_information as GFI
import numpy as np
from datetime import datetime

def main():
    create_report_all()


def create_login_details(name):
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = name

    return user, pwd, host, port, database_name

def get_states(db_name):
    
        user, pwd, host, port, database_name=create_login_details(db_name)

        try: 
            cdb_states, pdb_states = GIFD(user, pwd, host, port, database_name)
            return cdb_states, pdb_states
        except:
            print("-----------------------------------------\n")
            print(f'database {db_name} could not be queried\n')
            print("-----------------------------------------\n")

            cdb_states = [['UNKNOWN','UNKNOWN']]
            pdb_states = [['UNKNOWN','UNKNOWN']]

            return cdb_states, pdb_states



def get_FRA(db_name):
        user, pwd, host, port, database_name=create_login_details(db_name)

        try: 
            fra_information = GFI(user, pwd, host, port, database_name)
            return fra_information
        except:
            print("-----------------------------------------\n")
            print(f'Unable to query FRA information for {db_name}\n')
            print("-----------------------------------------\n")

            fra_information = [['UNKNOWN','UNKNOWN']]

            return fra_information

def create_report_all():
    sysdate = datetime.today().isoformat()

    db_arr, oh_arr = CDNHA()

    for db_name in db_arr:

        cdb_states, pdb_states = get_states(db_name)

        print(f'Report for {db_name} started on {sysdate}')
        print(f'Container database {db_name} is {cdb_states[0][1]}')
        
        for pdb, state in pdb_states:
            print(f'Pluggable Database {pdb} is {state}')

        fra_information=get_FRA(db_name)

        print(fra_information)

        with open(f'{db_name}_{sysdate}.txt', "a") as f:
            f.write(f'Report for {db_name} started on {sysdate}')



if __name__ == "__main__":
    main()
