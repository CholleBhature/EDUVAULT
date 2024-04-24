CREATE DATABASE IF NOT EXISTS eduvault;

USE eduvault;


-- Table to store user accounts (students and faculty)
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(10) PRIMARY KEY,
    pass VARCHAR(20) NOT NULL,
    desgn ENUM('stu', 'fct') NOT NULL
);

-- Table to store student details
CREATE TABLE IF NOT EXISTS stu_details (
    uid VARCHAR(10) PRIMARY KEY,
    f_name VARCHAR(50) NOT NULL,
    l_name VARCHAR(50) NOT NULL,
    sec VARCHAR(10),
    gender ENUM('M', 'F', 'O') NOT NULL,
    cont_num BIGINT NOT NULL,
    mail VARCHAR(70),
    address VARCHAR(150)
);

-- Table to store parent details
CREATE TABLE IF NOT EXISTS parent_dtl (
    uid VARCHAR(10) PRIMARY KEY,
    father_name VARCHAR(50) NOT NULL,
    mother_name VARCHAR(50) NOT NULL,
    f_cont BIGINT NOT NULL,
    m_cont BIGINT NOT NULL,
    f_mail VARCHAR(70),
    m_mail VARCHAR(70),
    FOREIGN KEY (uid) REFERENCES stu_details(uid)
);

-- Table to store subject-wise attendance
CREATE TABLE IF NOT EXISTS sub_att (
    uid VARCHAR(10) PRIMARY KEY,
    sub1 DECIMAL(5,2),
    sub2 DECIMAL(5,2),
    sub3 DECIMAL(5,2),
    sub4 DECIMAL(5,2),
    sub5 DECIMAL(5,2),
    FOREIGN KEY (uid) REFERENCES stu_details(uid)
);

-- Table to store leave applications
CREATE TABLE IF NOT EXISTS leav_app (
    uid VARCHAR(10),
    dat DATE,
    reason VARCHAR(100),
    remark VARCHAR(10) default 'pending',
    PRIMARY KEY (uid, dat),
    FOREIGN KEY (uid) REFERENCES stu_details(uid)
);

-- Table to store Unfair Means Cases (UMC) details
CREATE TABLE IF NOT EXISTS umc_dtl (
    uid VARCHAR(10) PRIMARY KEY,
    sub VARCHAR(10),
    FOREIGN KEY (uid) REFERENCES stu_details(uid)
);

-- Table to store exam schedules
CREATE TABLE IF NOT EXISTS date_sht (
    branch VARCHAR(10) PRIMARY KEY,
    exm1 VARCHAR(10),
    exm2 VARCHAR(10),
    exm3 VARCHAR(10),
    exm4 VARCHAR(10),
    exm5 VARCHAR(10)
);

-- Table to store branches and associated subjects
CREATE TABLE IF NOT EXISTS branches (
    br_nm VARCHAR(10) PRIMARY KEY,
    sub1 VARCHAR(20),
    sub2 VARCHAR(20),
    sub3 VARCHAR(20),
    sub4 VARCHAR(20),
    sub5 VARCHAR(20)
);

-- Table to store assignments
CREATE TABLE IF NOT EXISTS assign (
    br_nm VARCHAR(10) PRIMARY KEY,
    sub1 VARCHAR(20),
    sub2 VARCHAR(20),
    sub3 VARCHAR(20),
    sub4 VARCHAR(20),
    sub5 VARCHAR(20)
);

-- Table to store notice board messages
CREATE TABLE IF NOT EXISTS notice_board (
    id INT AUTO_INCREMENT PRIMARY KEY,
    message TEXT NOT NULL
);

-- Table to store semester-wise marks for students
-- Example: marks_sem1, marks_sem2, etc.
CREATE TABLE IF NOT EXISTS marks_sem (
    uid VARCHAR(10),
    sem INT,
    sub1 DECIMAL(5,2),
    sub2 DECIMAL(5,2),
    sub3 DECIMAL(5,2),
    sub4 DECIMAL(5,2),
    sub5 DECIMAL(5,2),
    PRIMARY KEY (uid, sem),
    FOREIGN KEY (uid) REFERENCES stu_details(uid)
);

ALTER TABLE stu_details
ADD COLUMN branch VARCHAR(10);

-- ALTER TABLE leav_app ADD COLUMN status VARCHAR(20) DEFAULT 'pending';
ALTER TABLE leav_app MODIFY COLUMN dat VARCHAR(15);
ALTER TABLE leav_app modify column ;



-- adding data to tables

INSERT INTO users (id, pass, desgn) VALUES
('10507', '1123', 'stu'),
('10206','1122','stu'),
('10076','1122','stu'),
('10722','1133','stu'),
('11002', 'pass11', 'fct');


INSERT INTO users (id, pass, desgn) VALUES ('10722','1133','stu');


INSERT INTO stu_details (uid, f_name, l_name, sec, gender, cont_num, mail, address) VALUES
('10507', 'Siddharth', 'Sharma', '607-A', 'M', 1234567890, 'siddharth@gmail.com', 'jai ho'),
('10206', 'Tanu', 'Satija', '601-A', 'F', 9876543210, 'tanu@email.com', 'addressssss'),
('10076', 'Anshika', 'Goel', '601-A', 'F', 9876543210, 'anshika@email.com', 'addressssss');

INSERT INTO parent_dtl (uid, father_name, mother_name, f_cont, m_cont, f_mail, m_mail) VALUES
('10507', 'John Doe Sr.', 'Jane Doe', 9876543210, 1234567890, 'john.doe.sr@example.com', 'jane.doe@example.com'),
('10206', 'Jack Smith', 'Jill Smith', 1234567890, 9876543210, 'jack.smith@example.com', 'jill.smith@example.com'),
('10076', 'Jack Smith', 'Jill Smith', 1234567890, 9876543210, 'jack.smith@example.com', 'jill.smith@example.com');

INSERT INTO sub_att (uid, sub1, sub2, sub3, sub4, sub5) VALUES
('10507', 95.5, 87.2, 91.8, 78.5, 88.9),
('10206', 88.3, 90.5, 84.7, 92.1, 89.6),
('10076', 88.3, 90.5, 84.7, 92.1, 89.6);


INSERT INTO leav_app (uid, dat, reason, remark) VALUES
('10206', '2023-01-05', 'Fever', 'Approved'),
('10076', '2023-02-10', 'Family function', 'Pending');


INSERT INTO umc_dtl (uid, sub) VALUES
('10507', 'Maths'),
('10206', 'Physics');


INSERT INTO date_sht (branch, exm1, exm2, exm3, exm4, exm5) VALUES
('CS', '2023-05-10', '2023-05-15', '2023-05-20', '2023-05-25', '2023-05-30'),
('EE', '2023-05-12', '2023-05-17', '2023-05-22', '2023-05-27', '2023-06-01');


INSERT INTO branches (br_nm, sub1, sub2, sub3, sub4, sub5) VALUES
('CS', 'Maths', 'Physics', 'Programming', 'Database', 'Networking'),
('EE', 'Electricity', 'Electronics', 'Circuits', 'Signals', 'Machines');


INSERT INTO assign (br_nm, sub1, sub2, sub3, sub4, sub5) VALUES
('CS', 'Assignment1', 'Assignment2', 'Assignment3', 'Assignment4', 'Assignment5'),
('EE', 'Project1', 'Project2', 'Project3', 'Project4', 'Project5');


INSERT INTO notice_board (message) VALUES
('Meeting scheduled for next Monday.'),
('Semester exams will begin from May 10th. Prepare well.');


INSERT INTO marks_sem (uid, sem, sub1, sub2, sub3, sub4, sub5) VALUES
('10507', 1, 85.5, 78.2, 91.8, 82.5, 88.9),
('10206', 1, 88.3, 90.5, 84.7, 92.1, 89.6),
('10076', 1, 86.3, 84.5, 88.7, 92.1, 89.6);


-- updating the data 

UPDATE stu_details
SET branch = 'CS'
WHERE uid IN ('10507', '10206', '10076');




delete from users where id='10722';


SELECT * FROM stu_details;




/*
-- display data 

SELECT * FROM users;


SELECT * FROM stu_details;

SELECT * FROM parent_dtl;

SELECT * FROM sub_att;

SELECT * FROM leav_app;

SELECT * FROM umc_dtl;

SELECT * FROM date_sht;

SELECT * FROM branches;

SELECT * FROM assign;

SELECT * FROM notice_board;

SELECT * FROM marks_sem;


-- drop tables 

drop table branches;
drop table leav_app;





desc stu_details;
desc leav_app;
desc umc_dtl;
desc branches;

*/
