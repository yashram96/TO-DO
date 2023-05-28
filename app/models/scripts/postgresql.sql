 CREATE USER yashram WITH PASSWORD <password>;
 CREATE DATABASE practice WITH OWNER yashram; 
 CREATE SCHEMA to_do AUTHORIZATION yashram; 
 
DROP TABLE IF EXISTS to_do.timezones CASCADE ;
 CREATE TABLE to_do.timezones ( 
         id serial NOT NULL PRIMARY KEY,
         timezone_name varchar unique not null,
         created_at timestamp without time zone default now(),
         updated_at timestamp without time zone  default now()
     );

DROP TABLE IF EXISTS to_do.users CASCADE;
 CREATE TABLE to_do.users ( 
         id serial NOT NULL PRIMARY KEY,
         username varchar unique NOT NULL ,
         email varchar unique NOT NULL,
         password varchar NOT NULL,
         firstname varchar NOT NULL,
         role varchar NOT NULL,
         is_active BOOLEAN NOT NULL default TRUE,
         created_at timestamp without time zone  default now(),
         updated_at timestamp without time zone  default now()
     );

DROP TABLE IF EXISTS to_do.user_preferences CASCADE;
 CREATE TABLE to_do.user_preferences ( 
         id serial NOT NULL PRIMARY KEY,
         user_id int not null references to_do.users(id),
         TimeZone_Id int not null references to_do.timezones(id),
         created_at timestamp without time zone  default now(),
         updated_at timestamp without time zone  default now()
     );