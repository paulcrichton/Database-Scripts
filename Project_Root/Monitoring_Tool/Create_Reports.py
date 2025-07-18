#!/usr/bin/env python3.9

# ──────────────────────────────────────────────
# Standard Library Imports
# ──────────────────────────────────────────────
import sys                                 # For system-specific parameters and functions
from datetime import datetime              # For timestamping and logging
import pandas as pd                        # For data manipulation and reporting

# ──────────────────────────────────────────────
# Monitoring Tool - Database Configuration Information
# ──────────────────────────────────────────────
from Monitoring_Tool.Fetch_Database_Status_Information.Fetch_Database_Configuration import (
    gather_configuration_information as GCI,                    # Logical configuration details
    gather_physical_configuration_information as GPCI          # Physical setup details
)

# ──────────────────────────────────────────────
# Monitoring Tool - Database State Information
# ──────────────────────────────────────────────
from Monitoring_Tool.Fetch_Database_Status_Information.Fetch_Database_State import (
    gather_cdb_state as GCS,                                   # Container DB state
    gather_pdb_state as GPS                                    # Pluggable DB state
)

# ──────────────────────────────────────────────
# Monitoring Tool - Pluggable Databases (PDB) and Container Databases (CDB)
# ──────────────────────────────────────────────
from Monitoring_Tool.Fetch_Database_Status_Information.Fetch_CDB_PDB_States import (
    gather_information_from_pluggable_databases as GIPD        # Gather info from all PDBs in a CDB
)

# ──────────────────────────────────────────────
# Monitoring Tool - Database Names and Environment
# ──────────────────────────────────────────────
from Monitoring_Tool.Fetch_Database_Status_Information.Fetch_PDB_Names import (
    create_pluggable_names_report as CPNR                      # Generate report of PDB names
)
from Monitoring_Tool.Fetch_Database_Status_Information.Fetch_Database_Home_And_SID import (
    create_db_name_home_array as CDNHA                         # Get DB name, ORACLE_HOME, and SID
)

# ──────────────────────────────────────────────
# Monitoring Tool - Storage & Space Usage
# ──────────────────────────────────────────────
from Monitoring_Tool.Fetch_FRA_Information.Fetch_FRA_Information import (
    create_FRA_report as CFR                                   # Generate FRA usage report
)
from Monitoring_Tool.Fetch_Tablespace_Information.Fetch_Tablespace_Information import (
    create_tablespace_report as CTR                            # Generate tablespace usage report
)

# ──────────────────────────────────────────────
# Monitoring Tool - DB Type Detection
# ──────────────────────────────────────────────
from Monitoring_Tool.Database_Connections.CDB_or_PDB import (
    cdb_or_pdb as COP                                          # Determine if database is CDB or PDB
)

def main():
    create_report_all()

def create_login_details(name):
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = name

    return user, pwd, host, port, database_name

def get_database_state(db_name, is_pdb):
    
    user, pwd, host, port, database_name=create_login_details(db_name)

    try: 
        if is_pdb!='PDB':
            cdb_state = GCS(user, pwd, host, port, database_name)
            return cdb_state
        else:
            pdb_state = GPS(user, pwd, host, port, database_name)
            return pdb_state
            
    except:
        print("-----------------------------------------\n")
        print(f'database {db_name} could not be queried\n')
        print("-----------------------------------------\n")

        cdb_state = "UNKNOWN"

        return cdb_state
    
def get_pluggable_names(container_name):

    user, pwd, host, port, database_name=create_login_details(container_name)

    try: 
        pdb_states = CPNR(user, pwd, host, port, database_name)
        return pdb_states
    except:
        print("-----------------------------------------\n")
        print(f'database {container_name} could not be queried for pluggable names\n')
        print("-----------------------------------------\n")

        pdb_states = "UNKNOWN"

        return pdb_states

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
        
def get_tablespace(db_name):
        user, pwd, host, port, database_name=create_login_details(db_name)

        try: 
            tablespace_metrics=CTR(user, pwd, host, port, database_name)
            return tablespace_metrics
        except:
            print("-----------------------------------------\n")
            print(f'Unable to query Tablespace information for {db_name}\n')
            print("-----------------------------------------\n")

            tablespace_metrics="UNKNOWN"
        

            return tablespace_metrics
        
def pluggable_check(db_name):
    user, pwd, host, port, database_name=create_login_details(db_name)

    try: 
        is_pdb=COP(user, pwd, host, port, database_name)
        return is_pdb
    except:
        print("-----------------------------------------\n")
        print(f'Unable to check if pluggable database for {db_name}\n')
        print("-----------------------------------------\n")
        
        is_pdb="UNKNOWN"

        return is_pdb
    
def gather_database_configuration_information(db_name):
    user, pwd, host, port, database_name=create_login_details(db_name)

    try: 
        configuration_information=GCI(user, pwd, host, port, database_name)
        return configuration_information
    except:
        print("-----------------------------------------\n")
        print(f'Unable to check database {db_name} for configuraiton information\n')
        print("-----------------------------------------\n")
        
        configuration_information="UNKNOWN"

        return configuration_information
    
def gather_physical_structure_information(db_name):
    user, pwd, host, port, database_name=create_login_details(db_name)

    try: 
        physical_structure=GPCI(user, pwd, host, port, database_name)
        return physical_structure
    except:
        print("-----------------------------------------\n")
        print(f'Unable to check database {db_name} for physical structure information\n')
        print("-----------------------------------------\n")
        
        physical_structure="UNKNOWN"

        return physical_structure

        
def create_database_report(db_name):
    sysdate = datetime.today().isoformat()
    #o = sys.stdout
    report_names=[]

    with open(f'{db_name}_{sysdate}.txt', "a") as f:
        report_names=f.name
        #sys.stdout = f

        is_pdb=pluggable_check(db_name)

        print(is_pdb)

        if "CDB" in is_pdb:
            cdb_state = get_database_state(db_name, is_pdb)

            if 'UNKNOWN' in cdb_state:
                print(f'Report for {db_name} started at {sysdate}\n\n')
                print(f'Database {db_name} is unreachable\n')
                print("-----------------------------------------\n")
                print(f'End of report for {db_name} at {sysdate}')
                print("-----------------------------------------\n\n\n\n")

            print(f'Report for {db_name} started at {sysdate}\n\n')

            print(f'Container database {db_name} is {cdb_state}')

        elif "PDB" in is_pdb:
            pdb_state = get_database_state(db_name, is_pdb)
            print(f'Report for {db_name} started at {sysdate}\n\n')
            print(f'pluggable database {db_name} is {pdb_state}')

        elif is_pdb == "UNKNOWN":
            print(f'Report for {db_name} started at {sysdate}\n\n')
            print(f'Database {db_name} is unreachable\n')
            print("-----------------------------------------\n")
            print(f'End of report for {db_name} at {sysdate}')
            print("-----------------------------------------\n\n\n\n")


        database_configuration_parameters=gather_database_configuration_information(db_name)
        print("-----------------------------------------\n")
        print(f'Database Configuration\n\n')
        print("-----------------------------------------\n")
        print(database_configuration_parameters,"\n\n")

        database_file_parameters=gather_physical_structure_information(db_name)
        print("-----------------------------------------\n")
        print(f'Physical Configuration Configuration\n\n')
        print("-----------------------------------------\n")
        print(database_file_parameters,"\n\n")
        
        fra_configuration, fra_usage_breakdown, fra_percent_used=get_FRA(db_name)
        print("\n\n\n")
        print("-----------------------------------------\n")
        print(f'Fast Recovery Configuration\n\n')
        print("-----------------------------------------\n")
        print(fra_configuration, "\n\n", fra_usage_breakdown, "\n\n", fra_percent_used)




    #sys.stdout = o

    # print(report_names)
    # for file_name in report_names:
    #     file = open(file_name)
    #     print(file.read())


def create_report_all():

    sysdate = datetime.today().isoformat()
    oratab_sid_arr, oh_arr = CDNHA()

    for index, container_name in enumerate(oratab_sid_arr):
        create_database_report(container_name)

        pdb_names=get_pluggable_names(container_name)
        if "UNKNOWN" not in pdb_names:
            for pdb_name in pdb_names.NAME:
                create_database_report(pdb_name)


if __name__ == "__main__":
    main()
