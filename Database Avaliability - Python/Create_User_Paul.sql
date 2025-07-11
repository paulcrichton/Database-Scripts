###Create User Paul


create user c##paul identified by paul account unlock;
grant sysdba to c##paul container=all;
GRANT CONNECT TO c##paul container=all;
GRANT  CONNECT, RESOURCE, DBA TO c##paul container=all;
GRANT CREATE SESSION TO c##paul container=all;
GRANT UNLIMITED TABLESPACE TO c##paul container=all;
