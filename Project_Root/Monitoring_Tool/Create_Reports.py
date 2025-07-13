#!/usr/bin/env python3.9

from Monitoring_Tool.Fetch_CDB_PDB_Information.Fetch_CDB_PDB_States import gather_information_from_database as GIFD
from Monitoring_Tool.Fetch_CDB_PDB_Information.Fetch_Database_Home_And_SID import create_db_name_home_array as CDNHA
from Monitoring_Tool.Fetch_FRA_Information.Fetch_FRA_Information import create_FRA_report as CFR
import numpy as np
import sys
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

            cdb_states = ['UNKNOWN']
            pdb_states = ['UNKNOWN']

            return cdb_states, pdb_states



def get_FRA(db_name):
        user, pwd, host, port, database_name=create_login_details(db_name)

        try: 
            fra_configuration, fra_usage_breakdown, fra_percent_used= CFR(user, pwd, host, port, database_name)
            return fra_configuration, fra_usage_breakdown, fra_percent_used
        except:
            print("-----------------------------------------\n")
            print(f'Unable to query FRA information for {db_name}\n')
            print("-----------------------------------------\n")

            fra_configuration = [['UNKNOWN','UNKNOWN']]
            fra_usage_breakdown=[['UNKNOWN']]
            fra_percent_used=[['UNKNOWN']]
        

            return fra_configuration, fra_usage_breakdown, fra_percent_used

def create_report_all():
    sysdate = datetime.today().isoformat()
    o = sys.stdout
    report_names=[]

    db_arr, oh_arr = CDNHA()

    for index, db_name in enumerate(db_arr):

               
        with open(f'{db_name}_{sysdate}.txt', "a") as f:
            report_names.append(f.name())

            f.write(f'Report for {db_name} started on {sysdate}')
            sys.stdout = f

            cdb_states, pdb_states = get_states(db_name)

            if 'UNKNOWN' in cdb_states:
                print(f'Database {db_arr} is unreachable\n')
                print("-----------------------------------------\n")
                print(f'End of report for {db_name} at {sysdate}')
                print("-----------------------------------------\n\n\n\n")
            
                continue 

            print(f'Report for {db_name} started at {sysdate}\n\n')
            print("-----------------------------------------\n")
            print(f'Database Configuration Information')
            print("-----------------------------------------\n")

            print(f'Database Home: {oh_arr[index]}')

            print(f'Container database {db_name} is {cdb_states[0][1]}')
            
            for pdb, state in pdb_states:
                print(f'Pluggable Database {pdb} is {state}')

            fra_configuration, fra_usage_breakdown, fra_percent_used=get_FRA(db_name)
            print("\n\n\n")
            print("-----------------------------------------\n")
            print(f'Fast Recovery Configuration\n\n')
            print("-----------------------------------------\n")
            print(fra_configuration, "\n\n", fra_usage_breakdown, "\n\n", fra_percent_used)

    sys.stdout = o

    print(report_names)
    for file_name in report_names:
        file = open("file_name")
        print(file.read())



if __name__ == "__main__":
    main()
