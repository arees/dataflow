create table companies (
  company_id integer primary key autoincrement,
  company_type integer not null,
  company_relative_id integer not null
)

create table isp (
  isp_id integer primary key autoincrement,
  short_name text not null,
  long_name text not null,
  region_id integer not null,
  datacoin_id integer not null,
  money_id integer not null,
  reputation integer not null,
  password_hash text not null,
  username text not null
)

create table tech_company (
  tech_company_id integer primary key autoincrement,
  short_name text not null,
  long_name text not null,
  region_id integer not null,
  datacoin_id integer not null,
  money_id integer not null,
  isp_id integer not null,
  reputation integer not null,
  password_hash text not null,
  username text not null
)

create table datacoin (
  datacoin_id integer primary key autoincrement,
  datacoin_value integer not null,
  trust integer not null
)

create table money (
  money_id integer primary key autoincrement,
  money_value integer not null
)

create table regions (
  region_id integer primary key autoincrement,
  infraestructure integer not null,
  population integer not null,
  internet_percentage integer not null,
  demand_percentage integer not null
)
