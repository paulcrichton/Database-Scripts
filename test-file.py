
pdb_states= [['PDB$SEED' 'READ ONLY']['IFSLPDB' 'READ WRITE']]

num_pdbs = len(pdb_states)/2

np.asarray(pdb_states)
pdb_states.reshape((num_pdbs, 2))
        
for pdb, state in pdb_states:
    print(f'Pluggable Database {pdb} is {state}')