set echo off; 
set feedback off; 
set heading off; 
spool &1
select NAME from v$pdbs;
spool off;
exit;
