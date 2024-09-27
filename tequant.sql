-- use defaultdb;
CREATE TABLE Blog (
	blog_link  varchar(200) primary key,
    Title VARCHAR(254) NOT NULL,
    Body MEDIUMTEXT CHARSET UTF16 NOT NULL,
    category VARCHAR(255) NOT NULL,
    author VARCHAR(255) NOT NULL,
    publish_date DATE NOT NULL
);
insert into Blog values ('tips-for-the-tesh-tipwef-vwfv2342-d', 'Title For the Furst Blog in TeQuant', 'Body l-78.558,52.367v-7.121l81.331-54.216l81.331,54.216v7.121L224.106,278.965z M262.215,123.865v16.799c0,2.761,2.239,5,5,5h0.465
                            ', 'Tech', 'Faith Dan-Elebiga' , '2024-09-25');

SELECT 
    *
FROM
    Blog;
-- drop table Blog
    
   CREATE TABLE Admins (
    FIRST_NAME VARCHAR(100) NOT NULL,
    LAST_NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(254) NOT NULL PRIMARY KEY,
    PASSWORD_ VARCHAR(254) NOT NULL
);

insert into Admins values ('Nikson', 'Kejeh', 'nikson.kejeh@tequant.ng', '12r3f2t32tgbv3qfcvnbteugt834t');


create table Videos(
Title varchar (100) not null,
Link varchar(254) not null primary key,
upload_date DATE NOT NULL
);

insert into Videos values('JavaScript Basics',  'https://www.youtube.com/embed/W6NZfCO5SIk', '2021-12-09');
    select * from Videos;
    
create table Students( 
	STUDENT_ID VARCHAR (100) NOT NULL PRIMARY KEY,
    FIRST_NAME VARCHAR(100) NOT NULL,
    LAST_NAME VARCHAR(100) NOT NULL,
    EMAIL VARCHAR(254) NOT NULL ,
    PASSWORD_ VARCHAR(254) NOT NULL,
    Date_Registered date not null
);

insert into Students values('CS/24/011/', 'Johnny', 'Doer', 'johnnydoer@gmail.com', '12456756i5u4352rgbgcbxh63g224gui67n', '2022-12-23');
select * from Students
