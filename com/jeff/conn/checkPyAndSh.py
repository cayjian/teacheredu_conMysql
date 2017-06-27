# -*- coding:utf-8 -*-
import MySQLdb
import time
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
try:
    conn = MySQLdb.Connect(host="192.168.0.230",user="root",passwd="password",db="study-projectcenter",charset="utf8")
    cur = conn.cursor()
    ISOTIMEFORMAT = '%Y%m%d_%H%M%S'
    cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    writer=csv.writer(open('/data/checkPyAndSh_'+cur_time+'.csv','wb'))
    writer.writerow(['项目id', '项目名称', '识别码', '工具名称', '工具码'])
    piYueSQL_1 = "SELECT t1.code,t.split_key,t.role_id,t.permission_id,t1.name " \
                 "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                 "WHERE t.permission_id = t1.id AND t1.role_type = 1 AND t1.code LIKE '350%101009';"

    shenHeSQL_1=  "SELECT t1.code,t.split_key,t.role_id,t.permission_id,t1.name " \
                 "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                 "WHERE t.permission_id = t1.id AND t1.role_type = 1 AND t1.code LIKE '350%101008';"

    piYueSQL_4 =  "SELECT t1.code,t.split_key,t.role_id,t.permission_id,t1.name " \
                 "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                 "WHERE t.permission_id = t1.id AND t1.role_type = 4 AND t1.code LIKE '350%201010';"

    shenHeSQL_4 =  "SELECT t1.code,t.split_key,t.role_id,t.permission_id,t1.name " \
                 "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                 "WHERE t.permission_id = t1.id AND t1.role_type = 4 AND t1.code LIKE '350%201013';"

    # 规则：如果1或4角色批阅审核都勾选了， 筛出；如果1或4之间勾选不一致，筛出
    cur.execute(piYueSQL_1)
    queryData_piYue_1 = cur.fetchall()
    cur.execute(shenHeSQL_1)
    queryData_shenHe_1 = cur.fetchall()

    cur.execute(piYueSQL_4)
    queryData_piYue_4 = cur.fetchall()
    cur.execute(shenHeSQL_4)
    queryData_shenHe_4 = cur.fetchall()

    piYue_1_list=[]
    for py_1 in queryData_piYue_1:
        piYue_1_list.append(str(py_1[0][:5])+"_"+str(py_1[1]))
    # print piYue_1_list

    shenHe_1_list = []
    for sh_1 in queryData_shenHe_1:
        shenHe_1_list.append(str(sh_1[0][:5]) + "_" + str(sh_1[1]))
    # print shenHe_1_list
    # 取批阅1和审核1的交集，即为都勾选的
    jiaoji_list_1=list(set(piYue_1_list).intersection(set(shenHe_1_list)))
    # print jiaoji_list_1

    piYue_4_list=[]
    for py_4 in queryData_piYue_4:
        piYue_4_list.append(str(py_4[0][:5])+"_"+str(py_4[1]))

    shenHe_4_list = []
    for sh_4 in queryData_shenHe_4:
        shenHe_4_list.append(str(sh_4[0][:5]) + "_" + str(sh_4[1]))

    # 取批阅4和审核4的交集，即为都勾选的
    jiaoji_list_4 = list(set(piYue_4_list).intersection(set(shenHe_4_list)))
    # print jiaoji_list_4
    # 1与4的并集，即为两个角色各自双勾的
    neibubutong_list= list(set(jiaoji_list_4).union(set(jiaoji_list_1)))

    # 取批阅1和审核4的交集
    jiaocha_1=list(set(piYue_1_list).intersection(set(shenHe_4_list)))
    # 取批阅4和审核1的交集
    jiaocha_4 =list(set(shenHe_1_list).intersection(set(piYue_4_list)))
    # 取差别的交集，即为勾选不一致的
    waibubutong_list= list(set(jiaocha_1).union(set(jiaocha_4)))
    #取双勾选和勾选不一致的并集，即为所有勾选错误的
    result_list = list(set(waibubutong_list).union(set(neibubutong_list)))

    def select_pid(split_key, code):
        select_sql = "SELECT p.id,p.name,t.split_key,t.platform_title,t.code " \
                     "FROM el_pc_project_tool t LEFT JOIN el_pc_project p ON t.split_key=p.split_key " \
                     "WHERE t.split_key=%s AND t.code=%s" % (split_key, code)

        cur.execute(select_sql)
        querydata = cur.fetchall()
        for query in querydata:
            writer.writerow([query[0],query[1],query[2],query[3],query[4]])

    for i in result_list:
        select_pid(str(i[6:]),str(i[0:5]))

    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])

