#!/usr/bin/env python
import psycopg2

DBname = "news"

def prob1():
    db = psycopg2.connect(database=DBname)
    c = db.cursor()
    c.execute("SELECT articles.title, COUNT(*) AS num"
              "FROM articles JOIN log"
              "ON log.path = '/article/' || articles.slug"
              "GROUP BY articles.title"
              "ORDER BY NUM DESC"
              "LIMIT 3;")
    c.fetchall()
    db.close()


def prob2():
    db = psycopg2.connect(database=DBname)
    c = db.cursor()
    c.execute("SELECT authors.name, COUNT(*) AS num"
              "FROM authors, articles, log"
              "WHERE authors.id=articles.author"
              "and log.path = '/article/' || articles.slug"
              "GROUP BY authors.name"
              "ORDER BY NUM DESC;")
    c.fetchall()
    db.close()


def prob3():
    db = psycopg2.connect(database=DBname)
    c = db.cursor()
    c.execute("CREATE VIEW ok_browse AS"
              "SELECT date_trunc('day',time) AS day, COUNT(status) AS num"
              "FROM log"
              "where status = '200 OK'"
              "GROUP BY day"
              "ORDER BY day;"

              "CREATE VIEW error_browse AS"
              "SELECT date_trunc('day',time) AS day, COUNT(status) AS num"
              "FROM log"
              "where status = '404 NOT FOUND'"
              "GROUP BY day"
              "ORDER BY day;"

              "SELECT ok_browse.day, float4(error_browse.num)/"
              "(float4(error_browse.num)+float4(ok_browse.num)) AS rate"
              "FROM ok_browse, error_browse"
              "where float4(error_browse.num)"
              "/(float4(error_browse.num)+float4(ok_browse.num))>0.01"
              "and ok_browse.day=error_browse.day;")
    c.fetchall()
    db.close()
