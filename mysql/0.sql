use mysql;
select host, user from user;
grant all privileges on *.* to root@'%' identified by 'Mx560205';
-- 这一条命令一定要有：
flush privileges;
