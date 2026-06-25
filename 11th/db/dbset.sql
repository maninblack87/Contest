create table if not exists 학생정보 (
    학번 text primary key,
    이름 text not null,
    이메일 text not null,
    학과 text not null,
    상태 text not null,
    foreign key (학과) references 학과정보(학과코드)
);

create table if not exists 학과정보 (
    학과코드 text primary key,
    명칭 text not null
);

create table if not exists 업무사용자 (
    사번 text primary key,
    이름 text not null,
    권한 text not null,
    암호 text not null
);

insert or ignore into 학생정보 (학번, 이름, 이메일, 학과, 상태) values 
('22001','문소리','s22001@kead.ac.kr','c001','졸업'),
('22002','김원중','s22002@kead.ac.kr','c003','졸업'),
('22003','김은하','s22003@kead.ac.kr','c002','휴학'),
('23001','홍동길','s23001@kead.ac.kr','c004','재학'),
('23002','박만정','s23002@kead.ac.kr','c002','휴학'),
('23003','오세양','s23003@kead.ac.kr','c004','재학'),
('23004','유일이','s23004@kead.ac.kr','c001','재학'),
('24001','차장영','s24001@kead.ac.kr','c003','재학'),
('24002','홍길동','s24002@kead.ac.kr','c002','퇴학'),
('24003','최명수','s24003@kead.ac.kr','c004','재학'),
('24004','강감찬','s24004@kead.ac.kr','c001','재학');

insert or ignore into 학과정보 (학과코드, 명칭) values 
('c001', '정보통신과'),
('c002', 'AI개발과'),
('c003', '클라우드보안과'),
('c004', '모바일개발과');

insert or ignore into 업무사용자 (사번, 이름, 권한, 암호) values
('05110401','정한용','user','05110401'),
('08100101','마한경','admin','08100101'),
('12022401','주민제','admin','12022401'),
('22081001','양한솔','user','22081001');
