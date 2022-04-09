set sql_safe_updates=0;

create database IF NOT EXISTS mbt1;
use mbt1;
alter database mbt1 default character set utf8mb4;

set foreign_key_checks = 0;   -- 외래키 체크하지 않는 것으로 설정
drop table IF EXISTS User cascade;   -- 기존 고객 테이블 제거  
drop table IF EXISTS Center cascade;   -- 기존 대리점 테이블 제거  
drop table IF EXISTS Record cascade;   -- 기존 직원 테이블 제거  
drop table IF EXISTS Ranking cascade;   -- 기존 렌탈제품 테이블 제거  
set foreign_key_checks = 1;   -- 외래키 체크하는 것으로 설정


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
primary key(RDate),
foreign key (UID) references User(UID),
foreign key (CCODE) references User(CCODE));


insert into Center
values(1111, 'GYM', '마포구 상수동');

insert into User
values('kms', '1234', 'kms', 1111);

insert into Record
values('squat', '22-04-03', 100, 10, 140, 'kms', 1111);

update Record
set RDate = '22-04-02', RWeight = 0, R1rm = 0
where REvent = 'squat' and UID = 'kms' and CCODE = 1111;

delete from Record
where RDate = '22-04-09';

-- 1
select * from Center;
select * from User;
select * from Record;