# -*- coding:utf-8 -*-
import MySQLdb
try:
    conn = MySQLdb.Connect(host="192.168.0.230",user="root",passwd="password",db="study-projectcenter",charset="utf8")
    ##cur = conn.cursor()
    cur = conn.cursor(cursorclass=MySQLdb.cursors.DictCursor) ## 注意这里：cursorclass = MySQLdb.cursors.DictCursor
    sql="select * from el_pc_config LIMIT 1"
    cur.execute(sql)
    querydata = cur.fetchall()
    print querydata[0].get("id")

    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])
