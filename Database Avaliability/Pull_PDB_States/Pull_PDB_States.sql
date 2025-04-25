set echo off; 
set feedback off; 
set heading off; 
set termout off
set markup csv on
spool &1
select NAME, OPEN_MODE from v$pdbs;
spool off;
exit;
