# -*- coding:utf-8 -*-
import MySQLdb
import time

class Data:
    split_key=''
    code = ''
    role_id=''
    permission_id=''

    def __init__(self, c, s, r, p):
        self.code = c
        self.split_key = s
        self.role_id = r
        self.permission_id = p

    def toString(self):
        return str(self.split_key) + "_" + str(self.role_id) + "_" + str(self.code)[:5]
try:
    conn = MySQLdb.Connect(host="10.10.7.44", user="root", passwd="password",db="study-projectcenter",
                           charset="utf8")
    cur = conn.cursor()
    ISOTIMEFORMAT = '%Y%m%d_%H%M%S'
    cur_time=time.strftime(ISOTIMEFORMAT, time.localtime())
    file = open('/temp/UpdatePermission_DML_'+cur_time+'.txt','w')

    selectSQLFor1 = "SELECT t1.id FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                    "WHERE t.permission_id = t1.id AND t1.role_type = 1 " \
                    "AND (t1.code LIKE '350%101009' OR t1.code LIKE '350%101008')" \
                    "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor2 = "SELECT t1.id FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                    "WHERE t.permission_id = t1.id AND t1.role_type = 2 " \
                    "AND (t1.code LIKE '350%001010' OR t1.code LIKE '350%001013')" \
                    "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor3 = "SELECT t1.id FROM el_sa_role_permission_ref t,el_sa_permission t1 " \
                    "WHERE t.permission_id = t1.id AND t1.role_type = 3 " \
                    "AND (t1.code LIKE '350%301003' OR t1.code LIKE '350%301004')" \
                    "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor4_py = "SELECT t1.code,t.split_key,t.role_id,t.permission_id " \
                       "FROM el_sa_role_permission_ref t,el_sa_permission t1 " \
                       "WHERE t.permission_id = t1.id AND t1.role_type = 4 AND t1.code LIKE '350%201010'" \
                       "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor4_sh = "SELECT t1.code,t.split_key,t.role_id,t.permission_id " \
                       "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                       "WHERE t.permission_id = t1.id AND t1.role_type = 4 AND t1.code LIKE '350%201013'" \
                       "AND t1.split_key NOT LIKE '-%';"

    ## 查询permission所有查看批阅、查看审核
    selectSQLFor1_per = "SELECT t1.id FROM el_sa_permission t1 " \
                        "WHERE t1.role_type = 1 " \
                        "AND (t1.code LIKE '350%101009' OR t1.code LIKE '350%101008')" \
                        "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor2_per = "SELECT t1.id FROM el_sa_permission t1 " \
                        "WHERE t1.role_type = 2 " \
                        "AND (t1.code LIKE '350%001010' OR t1.code LIKE '350%001013')" \
                        "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor3_per = "SELECT t1.id FROM el_sa_permission t1 " \
                        "WHERE t1.role_type = 3 " \
                        "AND (t1.code LIKE '350%301003' OR t1.code LIKE '350%301004')" \
                        "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor4_py_per = "SELECT t1.id FROM el_sa_permission t1 " \
                           "WHERE t1.role_type = 4 AND t1.code LIKE '350%201010'" \
                           "AND t1.split_key NOT LIKE '-%';"

    selectSQLFor4_sh_per = "SELECT t1.id FROM el_sa_permission t1 " \
                           "WHERE t1.role_type = 4 AND t1.code LIKE '350%201013'" \
                           "AND t1.split_key NOT LIKE '-%';"

    cur.execute(selectSQLFor1)
    queryData_1 = cur.fetchall()

    cur.execute(selectSQLFor2)
    queryData_2 = cur.fetchall()

    cur.execute(selectSQLFor3)
    queryData_3 = cur.fetchall()

    # 辅导老师不可同等对待
    cur.execute(selectSQLFor4_py)
    queryData_4_py = cur.fetchall()

    cur.execute(selectSQLFor4_sh)
    queryData_4_sh = cur.fetchall()

    def update_permission(id):
        update_sql = 'UPDATE el_sa_permission SET split_key = -split_key WHERE id= %s' % id
        cur.execute(update_sql)
        conn.commit()
        file.write(update_sql + "\n")

    def update_permission_4_name(id):
        update_sql = 'UPDATE el_sa_permission SET name=\'%s\' WHERE id= %s' % ('批阅/审核',id)
        cur.execute(update_sql)
        conn.commit()
        file.write(update_sql + "\n")

    def update_permission_ref(id):
        update_sql = "UPDATE el_sa_role_permission_ref SET split_key = -split_key WHERE permission_id= %s" % id
        cur.execute(update_sql)
        conn.commit()
        file.write(update_sql + "\n")

    # 得到审核不存在批阅里的permission_id
    def get_permisson_4(permission_id, role_id, split_key):
        #查询该id的菜单id和code
        str1 = "SELECT menu_id,code FROM el_sa_permission WHERE id = %s" % permission_id
        cur.execute(str1)
        queryData_getStr1 = cur.fetchall()

        # 改变code最后一位为批阅的code,查询出同列表得批阅id
        str2 = "SELECT id FROM el_sa_permission WHERE menu_id=%s " \
              "and code=%s" %(queryData_getStr1[0][0], queryData_getStr1[0][1][:-1]+"0")
        cur.execute(str2)
        queryData_getStr2 = cur.fetchall()

        # 根据得到的批阅id 查询 ref表中是否有数据，没有的话插入，有的话跳过
        str3 = "SELECT * FROM el_sa_role_permission_ref " \
               "WHERE role_id=%s AND permission_id=%s" % (role_id,queryData_getStr2[0][0])
        cur.execute(str3)
        queryData_getStr3 = cur.fetchall()

        if len(queryData_getStr3)==0:
            str4 = "INSERT INTO el_sa_role_permission_ref (split_key,role_id,permission_id,sort) " \
                   "VALUES(%s,%s,%s,0)" % (split_key,role_id,queryData_getStr2[0][0])
            try:
                cur.execute(str4)
                conn.commit()
                file.write(str4 + "\n")
            except MySQLdb.Error, e:
                print"Mysql Error %d: %s" % (e.args[0], e.args[1])

    for id in queryData_1:
        update_permission(id[0])
        update_permission_ref(id[0])

    for id in queryData_2:
        update_permission(id[0])
        update_permission_ref(id[0])

    for id in queryData_3:
        update_permission(id[0])
        update_permission_ref(id[0])

    queryData_4_py_list=[]
    queryData_4_sh_list=[]
    for py in queryData_4_py:
        queryData_4_py_list.append(str(py[1])+"_"+str(py[2])+"_"+str(py[0][:-6]))
        update_permission_4_name(py[3])

    for sh in queryData_4_sh:
        queryData_4_sh_list.append(Data(sh[0], sh[1], sh[2], sh[3]))

    for sh in queryData_4_sh_list:
        if sh.toString() not in queryData_4_py_list:
            get_permisson_4(sh.permission_id, sh.role_id, sh.split_key)
        update_permission(sh.permission_id)
        update_permission_ref(sh.permission_id)


    ## 查询permission所有查看批阅、查看审核
    cur.execute(selectSQLFor1_per)
    queryData_1_per = cur.fetchall()

    cur.execute(selectSQLFor2_per)
    queryData_2_per = cur.fetchall()

    cur.execute(selectSQLFor3_per)
    queryData_3_per = cur.fetchall()

    cur.execute(selectSQLFor4_py_per)
    queryData_4_py_per = cur.fetchall()

    cur.execute(selectSQLFor4_sh_per)
    queryData_4_sh_per = cur.fetchall()

    ## 处理所有查看批阅与查看审核
    ## 删除123查看批阅、查看审核，删除4的审核，修改4的批阅为批阅/审核
    for id in queryData_1_per:
        update_permission(id[0])

    for id in queryData_2_per:
        update_permission(id[0])

    for id in queryData_3_per:
        update_permission(id[0])

    for id in queryData_4_py_per:
        update_permission_4_name(id[0])

    for id in queryData_4_sh_per:
        update_permission(id[0])

    cur.close()
    conn.close()
    file.close()
except MySQLdb.Error, e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])
