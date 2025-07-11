#!/usr/bin/env python3.9

import re
import os

def create_db_name_home_array():
    """
    Fetch database names and Oracle home paths from oratab file
    """
    # Default oratab file path
    ot = '/etc/oratab'
    
    # Check if oratab file exists
    if not os.path.exists(ot):
        print(f"Error: Oratab file {ot} not found.")
        return None, None
    
    # Read the oratab file
    try:
        with open(ot, 'r') as f:
            lines = f.readlines()
    except IOError:
        print(f"Error: Unable to read {ot}")
        return None, None
    
    # Initialize arrays to store database names and Oracle homes
    db_arr = []
    oh_arr = []
    
    # Process each line in the oratab file
    for line in lines:
        # Skip comments and empty lines
        if line.strip() and not line.startswith('#') and not line.startswith('*'):
            # Split the line by ':'
            parts = line.strip().split(':')
            
            # Check if the line matches the expected format
            if len(parts) >= 3 and parts[2] in ['Y', 'N']:
                db_arr.append(parts[0])
                oh_arr.append(parts[1])
    
    return db_arr, oh_arr

def main():
    # Call the function
    db_arr, oh_arr = create_db_name_home_array()

        # Display output (first elements)
    if db_arr:
        print(db_arr[0])
    if oh_arr:
        print(oh_arr[0])

if __name__ == "__main__":
    main()