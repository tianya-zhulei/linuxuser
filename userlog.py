#!/bin/python
# coding:UTF-8
#coding:utf-8
import os
import socket
import sys
import time
sys.path.append('/home/zhulei/PycharmProjects/untitled/venv/lib/python2.7/site-packages') # 当前项目路径加入
import pymysql
while True:
   def userlog(username):
     db = pymysql.connect("122.152.205.63", "yanzhouhan", "Yanzhouhan123456!", "collection")
     cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
     createtime = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
     cursor.execute("SELECT * FROM account") # 使用 execute()  方法执行 SQL 查询
     data = cursor.fetchall() # 使用 fetchone() 方法获取单条数据.
     Login_Ip = os.popen("lastlog -u \'"+str(username)+"\' | awk 'NR ==2 {print $3}'").read()
     Login_Ip=Login_Ip.rstrip()
     Login_time=os.popen("lastlog -u \'"+str(username)+"\' |awk 'NR ==2 {print $5$6,$7}' ").read().rstrip()
     port =os.popen("lastlog -u \'"+str(username)+"\' |awk 'NR==2 {print $2}' ").read().rstrip()
     # Login_time=time.strptime(str.rstrip(Login_timea,"\n"),"%Y-%m-%D %H:%M")
     print username #用户名
     print port  #登录端口
     flage = True
    #获取IP地址my
     def my_ip():
        try:
                csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                csock.connect(('8.8.8.8', 80))
                (addr, port) = csock.getsockname()
                csock.close()
                return  addr
        except socket.error:
            return "127.0.0.1"
     if __name__ == "__main__":
        print my_ip()
     # if  port =="**从未登录过**\\n":
     if  port =='**从未登录过**':
         flage=False
     else:
        flage=True
    #插入userlogin表
     if flage==True:
        state="命令行"
        sql  = "INSERT INTO userlogin(loginname,createtime,port,logintime,ipaddress,state)" \
           " VALUES(\'"+str(username)+"\',\'"+str(createtime)+"\'," \
           "\'"+str(port)+"\',\'"+str(Login_time)+"\',\'"+str(Login_Ip)+"\',\'"+str(state)+"\') "
        print sql
        try:
       # 执行sql语句
            cursor.execute(sql)
       # 提交到数据库执行
            db.commit()
            print('获取当前信息成功')
        except Exception, e:
       # 如果发生错误则回滚
            print('获取当前信息失败')
            print e.message
            db.rollback()
        cursor.execute("SELECT * FROM userlogin") # 使用 execute()  方法执行 SQL 查询
        data=cursor.fetchall()
        print data
        time.sleep(0)
   break
