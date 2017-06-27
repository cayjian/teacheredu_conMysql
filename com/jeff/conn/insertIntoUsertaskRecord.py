# -*- coding:utf-8 -*-
import MySQLdb

try:
    conn = MySQLdb.Connect(host="192.168.0.230",user="root",passwd="password",db="study-projectcenter",charset="utf8")
    cur = conn.cursor()

    #查询ut表所有不合格记录
    sql_ut="select * from el_pc_usertask WHERE (grade='nopass' OR grade='disagree') AND split_key NOT LIKE '-%';"
    cur.execute(sql_ut)
    query_ut = cur.fetchall()
    values=[]
    for data in query_ut:
        values.append(data)
    #print values[0]
    #插入record表
    sql_utr_insert="INSERT INTO el_pc_usertask_record (usertask_id, split_key, task_id, user_id, username, " \
               "t_user_id, class_id, context, attachments, status, correct, audit, recommend_id, recommend_date, " \
               "is_recommend, remark, addtime, checktime, grade, view_num, comment_num, sys_dict_id1, " \
               "sys_dict_id2, sys_dict_id3, sys_dict_id4, sys_dict_id5, sys_dict_id6, sys_dict_id7, sys_dict_id8, " \
               "sys_dict_id9, sys_dict_id10, usr_dict_id1, usr_dict_id2, usr_dict_id3, usr_dict_id4, usr_dict_id5, " \
               "usr_dict_id6, usr_dict_id7, usr_dict_id8, usr_dict_id9, usr_dict_id10, sys_dict_code1, " \
               "sys_dict_code2, sys_dict_code3, sys_dict_code4, sys_dict_code5, sys_dict_code6, sys_dict_code7, " \
               "sys_dict_code8, sys_dict_code9, sys_dict_code10, usr_dict_code1, usr_dict_code2, usr_dict_code3, " \
               "usr_dict_code4, usr_dict_code5, usr_dict_code6, usr_dict_code7, usr_dict_code8, usr_dict_code9, " \
               "usr_dict_code10, markComment, m_user_id, stage_id, dict_id_level1, dict_id_level2, dict_id_level3, " \
               "dict_id_level4, is_draft ,updatetime, deletetime) " \
               "VALUES (%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s,%s,%s,%s," \
                   "%s,%s,%s,%s)"

    #cur.executemany(sql_utr_insert,values)
    #conn.commit()

    #获取刚插入的
    sql_utr_select="SELECT doc.id, doc.split_key,doc.usertask_id, doc.filetype, " \
                   "doc.name, doc.url, doc.create_date, doc.note, re.id " \
                   "FROM el_to_usertask_doc doc " \
                   "INNER JOIN el_pc_usertask_record re " \
                   "ON doc.split_key = re.split_key " \
                   "AND doc.usertask_id = re.usertask_id"

    cur.execute(sql_utr_select)
    query_utr_select = cur.fetchall()



    def insertIntoUTDoc(split_key, usertask_id, filetype, name, url, create_date, note):
        sql_utdoc_insert = "INSERT INTO el_to_usertask_doc " \
                           "(split_key, usertask_id, filetype, name, url, create_date, note) " \
                           "VALUES (%s,%s,%s,%s,%s,%s,%s)" \
                           %(split_key, usertask_id, filetype, name, url, create_date, note)
        cur.execute(sql_utdoc_insert)
        conn.commit()


    for data in query_utr_select:
        print data[8],data[1],data[2],data[3],data[4],data[5],data[6],data[7]








    cur.close()
    conn.close()
except MySQLdb.Error,e:
    print"Mysql Error %s: %s" % (e.args[0], e.args[1])
