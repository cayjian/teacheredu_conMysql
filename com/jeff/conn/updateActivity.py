# -*- coding:utf-8 -*-
import MySQLdb
try:
    conn_proj = MySQLdb.Connect(host="192.168.0.230", user="root", passwd="password", db="study-projectcenter",
                                charset="utf8")
    cur_proj = conn_proj.cursor()

    sql_dict_1="SELECT act.id,act.rely_id ,dict.split_key, dicttype.sort, dict.usr_dict_id1,dict.usr_dict_code1 " \
               "FROM `study-swap`.`el_pc_activity` act " \
               "INNER JOIN `study-projectcenter`.`el_pc_class_dict` dict " \
               "ON act.rely_id = dict.class_id " \
               "INNER JOIN `study-dict`.`el_sa_dict` dict1 " \
               "ON dict.usr_dict_id1=dict1.id " \
               "INNER JOIN `study-dict`.`el_sa_dicttype` dicttype " \
               "ON dict1.dicttype_id=dicttype.id " \
               "WHERE dicttype.name_key='area' AND act.rely_type='class' GROUP BY act.id;"

    sql_dict_2="SELECT act.id,act.rely_id ,dict.split_key, dicttype.sort, dict.usr_dict_id2,dict.usr_dict_code2 " \
               "FROM `study-swap`.`el_pc_activity` act " \
               "INNER JOIN `study-projectcenter`.`el_pc_class_dict` dict " \
               "ON act.rely_id = dict.class_id " \
               "INNER JOIN `study-dict`.`el_sa_dict` dict1 " \
               "ON dict.usr_dict_id2=dict1.id " \
               "INNER JOIN `study-dict`.`el_sa_dicttype` dicttype " \
               "ON dict1.dicttype_id=dicttype.id " \
               "WHERE dicttype.name_key='area' AND act.rely_type='class' GROUP BY act.id;"

    cur_proj.execute(sql_dict_1)
    result_dict_1 = cur_proj.fetchall()

    cur_proj.execute(sql_dict_2)
    result_dict_2 = cur_proj.fetchall()

    file = open('d://output_empty.txt', 'w')

    def update(result ,input_file):
        if (result[0] is None) or (result[1] is None) or (result[2] is None) \
            or (result[3] is None) or (result[4] is None) or (result[5] is None):
            input_file.write(str(result) +"\n")
        else:
            sql_update = "UPDATE `study-swap`.`el_pc_activity` SET usr_dict_id%s=%s ,usr_dict_code%s=%s " \
                  "WHERE id=%d" % (result[3], result[4], result[3], result[5], result[0])
            cur_proj.execute(sql_update)
            #print sql

    for res in result_dict_1:
        update(res,file)
    conn_proj.commit()

    for res in result_dict_2:
        update(res, file)
    conn_proj.commit()

    file.close()
    cur_proj.close()
    conn_proj.close()

except MySQLdb.Error,e:
    print"Mysql Error %d: %s" % (e.args[0], e.args[1])
