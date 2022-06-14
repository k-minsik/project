set sql_safe_updates=0;

create database IF NOT EXISTS mbt1;
use mbt1;
alter database mbt1 default character set utf8mb4;

set foreign_key_checks = 0;
drop table IF EXISTS User cascade; 
drop table IF EXISTS Center cascade;
drop table IF EXISTS Record cascade;  
drop table IF EXISTS Ranking cascade; 
set foreign_key_checks = 1;


create table Center (
CCODE INT NOT NULL,
Cname varchar(20) NOT NULL,
Caddress varchar(20) NOT NULL,
primary key(CCODE));


create table User (
UID varchar(20) NOT NULL,
UPW varchar(20) NOT NULL,
primary key(UID));
    

create table Record (
REvent varchar(10) NOT NULL,
RDate varchar(10) NOT NULL,
RWeight INT default 0,
Rreps INT default 0,
R1rm INT default 0,
UID varchar(10) NOT NULL,
CCODE INT NOT NULL,
primary key(REvent, RDate, UID),
foreign key (UID) references User(UID),
foreign key (CCODE) references Center(CCODE));

insert into Center
values(0000, 'NONE', '회원가입');
insert into Center
values(1111, 'GYM', '마포구 상수동');

insert into User
values('kms', '1234');
insert into User
values('asd', '1234');
insert into User
values('psy', '1234');

insert into Record
values('Squat', '22-05-01', 10, 1, 10, 'kms', 1111);
insert into Record
values('Squat', '22-05-02', 20, 2, 21, 'kms', 1111);
insert into Record
values('Squat', '22-05-03', 120, 6, 71, 'kms', 1111);
insert into Record
values('Squat', '22-05-04', 70, 7, 84, 'kms', 1111);
insert into Record
values('Squat', '22-05-05', 80, 8, 100, 'kms', 1111);

insert into Record
values('BenchPress', '22-05-01', 10, 1, 10, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-02', 20, 2, 21, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-03', 120, 3, 32, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-04', 40, 4, 44, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-05', 60, 6, 71, 'kms', 1111);

insert into Record
values('Deadlift', '22-05-01', 10, 1, 10, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-02', 20, 2, 21, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-03', 30, 3, 32, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-04', 40, 4, 44, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-05', 300, 5, 58, 'kms', 1111);

insert into Record
values('Squat', '22-05-05', 100, 5, 58, 'asd', 1111);
insert into Record
values('BenchPress', '22-05-05', 200, 5, 58, 'asd', 1111);
insert into Record
values('Deadlift', '22-05-05', 50, 5, 58, 'asd', 1111);

insert into Record
values('Squat', '22-05-05', 120, 5, 58, 'psy', 1111);
insert into Record
values('BenchPress', '22-05-05', 200, 5, 58, 'psy', 1111);
insert into Record
values('Deadlift', '22-05-05', 80, 5, 58, 'psy', 1111);



-- 1
select * from Center;
select * from User;
select * from Record;

select * from Record where REvent = 'Deadlift' and UID = 'kms' order by RDate desc LIMIT 7;
select * from Record where REvent = 'Squat' and UID = 'kms' order by RDate desc LIMIT 7;
select * from Record where REvent = 'BenchPress' and UID = 'kms' order by RDate desc LIMIT 7;


select UID, REvent, RWeight, dense_rank() over (order by RWeight desc) as ranking from Record;


select UID, MAX(RWeight)
from Record
where REvent = 'Squat'
group by UID;

select UID, SUM(RWeight) AS oneRM
from Record
group by UID; 




select * from User where UID = 'kms' and UPW = '1234';
select UID from User;


select MAX(RWeight) from Record where REvent = 'Squat' and UID = 'kms';
select * from Record where UID = 'qwe';