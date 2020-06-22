# -*- coding:utf-8 -*-

import os
import time
import pymysql
# import numpy.core.multiarray
from  common.config import  *
import jpype
import psycopg2

class InceptorConnect(object):

    def mysqlConnect(self):
        db = pymysql.connect(
            user="root",
            host='47.98.60.130',
            passwd="cndsdis123",
            # host='localhost',
            # host='10.4.255.129',
            # passwd="ccc331",
            # passwd="Ideal@123",
            db='hugeleaflabs_video',
            charset="utf8",
            cursorclass=pymysql.cursors.DictCursor
        )
        return db


    def postgconnect(self):
        pgconn=psycopg2.connect(database=database, user=user, password=password, host=host,port=port)
        return pgconn

    def get_all_data(self, db, sql):
        cursor = db.cursor()
        cursor.execute(sql)
        repetition = cursor.fetchall()
        return repetition

        ##将值写入文件
        # data = str(time.time())
        # fp = open("result" + data, "w")
        # loan_count = 0
        # for loanNumber in repetition:
        #     loan_count += 1
        #     fp.write(str(loanNumber) + "\n")
        # fp.close()


    def hiveConnect(self):
        jvmPath = jpype.getDefaultJVMPath()
        jpype.startJVM(jvmPath,
                       "-Djava.class.pathD:\soft\连接数据库工具/inceptor-sdk-transwarp-6.1.0-SNAPSHOT.jar")
                       #"-Djava.class.path=/opt/pythonworkspace/entgroupCrawler/inceptor-sdk-transwarp-6.1.0-SNAPSHOT.jar")
        # jpype.startJVM(jvmPath,
        #                "-Djava.class.path="+ os.getcwd()+"/inceptor-sdk-transwarp-6.1.0-SNAPSHOT.jar")
        HanLP = jpype.JClass('org.apache.hive.jdbc.HiveDriver')
        conn = jpype.java.sql.DriverManager.getConnection(
             "jdbc:hive2://192.168.99.101:10000/default")
            #"jdbc:hive2://114.80.110.4:10000/hisw_fast")
        return conn




    def getData(self, conn, sql):
        stmt = conn.createStatement()
        rs = stmt.executeQuery(sql)
        metaData = rs.getMetaData()
        columnCount = metaData.getColumnCount()
        result = []
        while rs.next():
            # index = rs.getString(1)
            jsonObj = {}
            for i in range(1, int(columnCount) + 1):
                columnName = metaData.getColumnLabel(i)
                value = rs.getString(columnName)
                jsonObj[columnName] = value
            result.append(jsonObj)
        return result

    def insertData(self, conn, sql):
        stmt = conn.createStatement()
        # stmt = conn.execute(sql)
        stmt.execute(sql)

    def close(self, conn):
        conn.close()
        jpype.shutdownJVM()

    def mysql_close(self, conn):
        consor = conn.cursor()
        consor.connection.commit()
        consor.close()
        conn.close()


if __name__ == '__main__':
    # db = InceptorConnect().mysqlConnect()
    # mysql = "SELECT * FROM t_video_weibo_topic "
    # loc = InceptorConnect().get_all_data(db=db, sql=mysql)
    # print(loc)
    # InceptorConnect().mysql_close(db)
    f = open("C:\\Users\\uAdmin\Desktop\\t_movie_staff_201908161431.sql", "r", encoding='utf-8')
    # 查看多少行
    # print(len(f.read().split("\n")))
    conn = InceptorConnect().hiveConnect()
    for i in f:
        sql = i.strip()
        # result = InceptorConnect().getData(conn=conn, sql=sql)
        # print(result)
        InceptorConnect().insertData(conn=conn, sql=sql)
    InceptorConnect().close(conn)

    # sql = "INSERT INTO t_video_weibo_topic VALUES ('193','177251','#时间都知道#','4544000','1400000000');"
    # # sql = "load data local inpath 'd:\\workspace\\hugeleaflabsVideoCrawler\\result1564024073' overwrite into table t_video_weibo_topic;"
    # conn = InceptorConnect().hiveConnect()
    # # result = InceptorConnect().getData(conn=conn, sql=sql)
    # # print(result)
    # InceptorConnect().insertData(conn=conn, sql=sql)
    # InceptorConnect().close(conn)
