use no1;

create table 학과정보 (
	학과코드 char(4) primary key not null,
    명칭 varchar(20) not null,
    constraint chk_학과코드 check (학과코드 like 'c___')		-- MySQL 5.X 이하 버전에서는 동작하지 않을 수 있음
);

show columns from 학과정보;

insert into 학과정보(학과코드, 명칭)
values
('c001', '정보통신과'),
('c002', 'AI개발과'),
('c003', '클라우드보안과'),
('c004', '모바일개발과');

select * from 학과정보;