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
Uname varchar(10) NOT NULL,
CCODE INT NOT NULL,
primary key(UID),
foreign key (CCODE) references Center(CCODE));
    

create table Record (
REvent varchar(10) NOT NULL,
RDate varchar(10) NOT NULL,
RWeight INT default 0,
Rreps INT default 0,
R1rm INT default 0,
UID varchar(10) NOT NULL,
CCODE INT NOT NULL,
primary key(REvent, RDate),
foreign key (UID) references User(UID),
foreign key (CCODE) references User(CCODE));


insert into Center
values(1111, 'GYM', '마포구 상수동');

insert into User
values('kms', '1234', 'kms', 1111);

insert into Record
values('Squat', '22-05-02', 10, 1, 10, 'kms', 1111);
insert into Record
values('Squat', '22-05-05', 20, 2, 21, 'kms', 1111);
insert into Record
values('Squat', '22-05-13', 30, 3, 32, 'kms', 1111);
insert into Record
values('Squat', '22-05-21', 40, 4, 44, 'kms', 1111);
insert into Record
values('Squat', '22-05-26', 50, 5, 58, 'kms', 1111);
insert into Record
values('Squat', '22-05-18', 60, 6, 71, 'kms', 1111);
insert into Record
values('Squat', '22-05-07', 70, 7, 84, 'kms', 1111);
insert into Record
values('Squat', '22-05-15', 80, 8, 100, 'kms', 1111);

insert into Record
values('BenchPress', '22-05-02', 10, 1, 10, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-28', 20, 2, 21, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-09', 30, 3, 32, 'kms', 1111);
insert into Record
values('BenchPress', '22-05-17', 40, 4, 44, 'kms', 1111);

insert into Record
values('Deadlift', '22-05-03', 10, 1, 10, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-14', 20, 2, 21, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-21', 30, 3, 32, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-10', 40, 4, 44, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-16', 50, 5, 58, 'kms', 1111);
insert into Record
values('Deadlift', '22-05-07', 60, 6, 71, 'kms', 1111);

-- 1
select * from Center;
select * from User;
select * from Record;