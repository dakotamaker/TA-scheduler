create table roles (
	role_id integer primary key,
	role_name varchar(20) unique not null
);

create table accounts (
	act_email varchar(50) primary key,
	act_fname varchar(50) not null,
	act_lname varchar(50) not null,
	act_password varchar(18),
	act_phone varchar(12) unique not null,
	role_id integer not null,
	foreign key(role_id) references roles(role_id)
);

create table courses (
	course_id integer primary key,
	course_name varchar(50) unique not null,
	instructor_email varchar(50),
	foreign key(instructor_email) references accounts(act_email)
);

create table labs (
	lab_id integer primary key,
	lab_name varchar(50) not null,
	course_id integer not null,
	ta_email varchar(50),
	foreign key(course_id) references courses(course_id),
	foreign key(ta_email) references accounts(act_email)
);
