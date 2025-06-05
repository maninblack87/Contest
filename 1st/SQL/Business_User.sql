use no1;

create table 업무사용자 (
	사번 char(8) primary key not null,
    이름 varchar(10) not null,
    권한 enum('admin', 'user') not null,
    암호 varchar(20) not null,
    constraint chk_사번 check (사번 regexp '^[0-9]{8}$')	-- Check 제약조건이 8.0.16미만 부터는 무시될 수 있음
);

show columns from 업무사용자;

insert into 업무사용자(사번, 이름, 권한, 암호)
values
('05110401', '정한용', 'user', '05110401'),
('08100101', '마한경', 'admin', '08100101'),
('12022401', '주민제', 'admin', '12022401'),
('22081001', '양한솔', 'user', '22081001');

select * from 업무사용자;
