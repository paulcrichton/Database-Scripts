col name format a25
col open_mode format a25
spool &1.txt
select name, open_mode from v$database;
exit;
