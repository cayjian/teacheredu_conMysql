# -*- coding:utf-8 -*-
import MySQLdb
import time

try:
    conn = MySQLdb.Connect(host="10.10.7.44", user="root", passwd="password", db="study-projectcenter",
                           charset="utf8")
    cur = conn.cursor()
    ISOTIMEFORMAT = '%Y%m%d_%H%M%S'
    cur_time = time.strftime(ISOTIMEFORMAT, time.localtime())
    file = open('/temp/InsertConfig_DML_' + cur_time + '.txt', 'w')

    piYueSQL = "SELECT RIGHT(t.split_key,6),LEFT(t1.code,5) " \
               "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
               "WHERE t.permission_id = t1.id AND t1.role_type = 1 AND t1.code LIKE '350%101009'"\
               "AND t1.split_key NOT LIKE '-%';"
    cur.execute(piYueSQL)
    piYue_queryData = cur.fetchall()
    piYueSplitKeyList = []
    for py in piYue_queryData:
        piYueSplitKeyList.append(py[1][:3] + py[0] + py[1][-2:])

    shenHeSQL = "SELECT RIGHT(t.split_key,6),LEFT(t1.code,5) " \
                "FROM el_sa_role_permission_ref t, el_sa_permission t1 " \
                "WHERE t.permission_id = t1.id AND t1.role_type = 1 AND t1.code LIKE '350%101008'"\
                "AND t1.split_key NOT LIKE '-%';"
    cur.execute(shenHeSQL)
    shenHe_queryData = cur.fetchall()
    shenHeSplitKeyList = []
    for sh in shenHe_queryData:
        shenHeSplitKeyList.append(sh[1][:3] + sh[0] + sh[1][-2:])

    # 批阅List和审核List取交集，交集部分应该为批阅
    jiaojiList = list(set(shenHeSplitKeyList).intersection(set(piYueSplitKeyList)))
    # 审核List中有，而交集List中没有的差集，相当于删除了与批阅List重复的部分
    chajiList = list(set(shenHeSplitKeyList).difference(set(jiaojiList)))

    # 获取pid,split_key对应关系字典
    projAllSQL = "SELECT id,split_key FROM el_pc_project"
    cur.execute(projAllSQL)
    projAll_queryData = cur.fetchall()
    projAll_dict = {}
    for proj in projAll_queryData:
        projAll_dict[long(proj[0])] = proj[1]

    # 批阅
    for py in piYueSplitKeyList:
        pid = long(py[5:-2])
        ptcode = str(py[:3] + py[-2:]) + "workTool_property"
        split_key = projAll_dict.get(long(py[5:-2]))
        if split_key is None:
            continue

        pyInsertStr = "INSERT INTO el_pc_config(split_key,project_id,type,name,value) " \
                      "VALUES(%s,%s,'6','%s','mark')" % (split_key, pid, ptcode)
        cur.execute(pyInsertStr)
        conn.commit()
        file.write(pyInsertStr + "\n")
    # 审核
    for sh in chajiList:
        pid = long(sh[5:-2])
        ptcode = str(sh[:3] + sh[-2:]) + "workTool_property"
        split_key = projAll_dict.get(long(sh[5:-2]))
        if split_key is None:
            continue

        shInsertStr = "INSERT INTO el_pc_config(split_key,project_id,type,name,value) " \
                      "VALUES(%s,%s,'6','%s','audit')" % (split_key, pid, ptcode)
        cur.execute(shInsertStr)
        conn.commit()
        file.write(shInsertStr + "\n")

    cur.close()
    conn.close()
    file.close()
except MySQLdb.Error, e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])
