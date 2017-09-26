import psycopg2

DBname="news"

def prob1():
    db=psycopg2.connect(database=DBname)
    c=db.cursor()
    c.execute(
    "select  articles.title, count(*) as num
    from articles  join log
    on    log.path = '/article/' || articles.slug
    group by articles.title
    order by num desc
    limit 3;")
    return c.fetchall()
    db.close()

def prob2():
    db=psycopg2.connect(database=DBname)
    c=db.cursor()
    c.execute(
    "select authors.name, count(*) as num
    from authors, articles, log
    where authors.id=articles.author
    and log.path = '/article/' || articles.slug
    group by authors.name
    order by num desc;")
    return c.fetchall()
    db.close()

def prob3():
    db=psycopg2.connect(database=DBname)
    c=db.cursor()
    c.execute(
    "create view ok_browse as
    select date_trunc('day',time) as day, count(status) as num
    from log
    where status = '200 OK'
    group by day
    order by day;

    create view error_browse as
    select date_trunc('day',time) as day, count(status) as num
    from log
    where status = '404 NOT FOUND'
    group by day
    order by day;

    select ok_browse.day, float4(error_browse.num)/(float4(error_browse.num)+float4(ok_browse.num)) as rate
    from ok_browse, error_browse
    where float4(error_browse.num)/(float4(error_browse.num)+float4(ok_browse.num))>0.01
    and ok_browse.day=error_browse.day;")
    return c.fetchall()
    db.close()
