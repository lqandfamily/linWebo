initSqlList = [
    "drop table if exists hot_spot",
    "drop table if exists spider_date",
    "drop table if exists t_user",
    """create table hot_spot
    (
        id         int auto_increment primary key,
        _rank      int,
        affair     char(100),
        views      int,
        crawl_date timestamp,
        date_id    int
    ) default charset=utf8;
    """,
    """
    create table spider_date
    (
        date_id         int auto_increment primary key,
        crawl_date timestamp
    ) default charset=utf8;
    """,
    """
    create table t_user
    (
        id int auto_increment primary key ,
        username varchar(40),
        password varchar(200)
    ) default charset=utf8;
    """
]
