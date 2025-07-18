use no1;

CREATE TABLE 학생정보 (
    학번 char(5) PRIMARY KEY NOT NULL,    
    이름 VARCHAR(20) not null,           
    이메일 VARCHAR(100) not null,         
    학과 char(4) not null,            
    상태 enum('재학', '졸업', '휴학', '퇴학') not null
);

insert into 학생정보(학번, 이름, 이메일, 학과, 상태)
values 
('22001', '문소리', 's22001@kead.ac.kr', 'c001', '졸업'),
('22002', '김원중', 's22002@kead.ac.kr', 'c003', '졸업'),
('22003', '김은하', 's22003@kead.ac.kr', 'c002', '휴학'),
('23001', '홍동길', 's23001@kead.ac.kr', 'c004', '재학'),
('23002', '박만정', 's23002@kead.ac.kr', 'c002', '휴학'),
('23003', '오세양', 's23003@kead.ac.kr', 'c004', '재학'),
('23004', '유일이', 's23004@kead.ac.kr', 'c001', '재학'),
('24001', '차장영', 's24001@kead.ac.kr', 'c003', '재학'),
('24002', '홍길동', 's24002@kead.ac.kr', 'c002', '퇴학'),
('24003', '최명수', 's24003@kead.ac.kr', 'c004', '재학'),
('24004', '강감찬', 's24004@kead.ac.kr', 'c001', '재학');

select * from 학생정보;