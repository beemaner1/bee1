drop table if exists ludi;
create table ludi (
  id integer primary key autoincrement,
  password text not null,
  log text not null
);