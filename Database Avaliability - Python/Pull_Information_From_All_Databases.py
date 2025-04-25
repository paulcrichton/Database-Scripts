#!/usr/bin/env python3.9

from Fetch_CDB_PDB_Information.Fetch_CDB_PDB_States import gather_information_from_database as GIFD

def main():
    user= "c##paul"
    pwd = "paul"
    host = "prodba-db"
    port = 1521
    database_name = "IFSPCDB"
    GIFD(user, pwd, host, port, database_name)


if __name__ == "__main__":
    main()