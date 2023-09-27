create table tripupdate_db
(
    id int auto_increment,
    data json null,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    constraint tripupdate_db_pk primary key (id)
);

create table vehicle_db
(
    trip_id text not null,
    route_Id text not null,
    stop_sequence int not null,
    stop_id text not null,
    vehicle_id text not null,
    status text not null,
    updated_at datetime null,
);