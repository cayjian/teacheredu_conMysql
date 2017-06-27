# -*- coding:utf-8 -*-
import MySQLdb
import time

try:
    conn = MySQLdb.Connect(host="10.10.246.50", user="root", passwd="password", db="study-projectcenter",
                           charset="utf8")
    cur = conn.cursor()
    ISOTIMEFORMAT = '%Y%m%d_%H%M%S'
    cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    file1 = open('D://checkUserTaskGrade_DML_' + cur_time + '.txt', 'w')
    file2 = open('D://checkUserTask2Grade_DML_' + cur_time + '.txt', 'w')
    file3 = open('D://checkUserTask3Grade_DML_' + cur_time + '.txt', 'w')
    sql_select_config_mark ="SELECT split_key,name FROM el_pc_config WHERE type='6' AND value='mark'" \
                            "AND split_key NOT LIKE '-%';"
    sql_select_config_audit = "SELECT split_key,name FROM el_pc_config WHERE type='6' AND value='audit'" \
                              "AND split_key NOT LIKE '-%';"

    cur.execute(sql_select_config_mark)
    queryData_config_mark = cur.fetchall()
    cur.execute(sql_select_config_audit)
    queryData_config_audit = cur.fetchall()

    def checkGrade(sk,property):
        grade="1=1"
        if property=='mark':
            grade="(grade='agree' OR grade='disagree')"
        elif property=='audit':
            grade = "(grade='verygood' OR grade='good' OR grade='pass' OR grade='nopass')"

        sql_select_usertask_grade="SELECT id,split_key,status,audit,grade,checktime " \
                                  " FROM el_pc_usertask WHERE split_key="+sk+" AND "+grade
        cur.execute(sql_select_usertask_grade)
        queryData_select_usertask_grade = cur.fetchall()
        if len(queryData_select_usertask_grade) > 0 :
            for usertask in queryData_select_usertask_grade:
                file1.write(
                    str(usertask[0]) + "_" + str(usertask[1]) + "_" + str(usertask[2]) + "_" + str(usertask[3]) + "_" +
                    str(usertask[4]) + "_" + str(usertask[5]) + "\n")

        sql_select_usertask1_grade = "SELECT id,split_key,status,audit,grade,checktime " \
                                     " FROM el_pc_usertask1 WHERE split_key=" + sk + " AND " + grade
        cur.execute(sql_select_usertask1_grade)
        queryData_select_usertask1_grade = cur.fetchall()
        if len(queryData_select_usertask1_grade) > 0:
            for usertask in queryData_select_usertask1_grade:
                file2.write(
                    str(usertask[0]) + "_" + str(usertask[1]) + "_" + str(usertask[2]) + "_" + str(usertask[3]) + "_" +
                    str(usertask[4]) + "_" + str(usertask[5]) + "\n")

        sql_select_usertask2_grade = "SELECT id,split_key,status,audit,grade,checktime " \
                                     " FROM el_pc_usertask2 WHERE split_key=" + sk + " AND " + grade
        cur.execute(sql_select_usertask2_grade)
        queryData_select_usertask2_grade = cur.fetchall()
        if len(queryData_select_usertask2_grade) > 0:
            for usertask in queryData_select_usertask2_grade:
                file3.write(
                    str(usertask[0]) + "_" + str(usertask[1]) + "_" + str(usertask[2]) + "_" + str(usertask[3]) + "_" +
                    str(usertask[4]) + "_" + str(usertask[5]) + "\n")

    splitkey_list_mark = []
    splitkey_list_audit = []
    file1.write("id,split_key,status,audit,grade,checktime" + "\n")
    file2.write("id,split_key,status,audit,grade,checktime" + "\n")
    file3.write("id,split_key,status,audit,grade,checktime" + "\n")
    file1.write("+++++++++++++++++++++++++批阅开始了+++++++++++++++++++++++++++++++++++++"+"\n")
    file2.write("+++++++++++++++++++++++++批阅开始了+++++++++++++++++++++++++++++++++++++"+"\n")
    file3.write("+++++++++++++++++++++++++批阅开始了+++++++++++++++++++++++++++++++++++++"+"\n")
    for data in queryData_config_mark:
        sk_mark = data[1][:3] +str(data[0])[5:] +data[1][3:5]
        checkGrade(sk_mark,'mark')

    file1.write("+++++++++++++++++++++++++批阅结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    file2.write("+++++++++++++++++++++++++批阅结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    file3.write("+++++++++++++++++++++++++批阅结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    print "mark OK"

    file1.write("+++++++++++++++++++++++++审核开始了+++++++++++++++++++++++++++++++++++++" + "\n")
    file2.write("+++++++++++++++++++++++++审核开始了+++++++++++++++++++++++++++++++++++++" + "\n")
    file3.write("+++++++++++++++++++++++++审核开始了+++++++++++++++++++++++++++++++++++++" + "\n")
    for data in queryData_config_audit:
        sk_audit = data[1][:3] + str(data[0])[5:] + data[1][3:5]
        checkGrade(sk_audit, 'audit')

    print "audit OK"
    file1.write("+++++++++++++++++++++++++审核结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    file2.write("+++++++++++++++++++++++++审核结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    file3.write("+++++++++++++++++++++++++审核结束了+++++++++++++++++++++++++++++++++++++" + "\n")

    print "ALL OK"
    file1.write("+++++++++++++++++++++++++所有都结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    file2.write("+++++++++++++++++++++++++所有都结束了+++++++++++++++++++++++++++++++++++++" + "\n")
    file3.write("+++++++++++++++++++++++++所有都结束了+++++++++++++++++++++++++++++++++++++" + "\n")

except MySQLdb.Error,e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])
