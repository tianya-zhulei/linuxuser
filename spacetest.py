#coding=utf-8
#!/usr/bin/python
#!/usr/bin/python
import os
import sys
import time
import thread
sys.path.append('/home/zhulei/PycharmProjects/untitled/venv/lib/python2.7/site-packages') # 当前项目路径加入
import pymysql
def userspace(username):
    db = pymysql.connect("122.152.205.63", "yanzhouhan", "Yanzhouhan123456!", "collection")
    cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
    cursor.execute("select state from account where logname=%s",username)
    print username
    os.system("quotaon -avug")
    linea=os.popen("sudo quota -uvs \'"+username+"\' |sed '1d' |awk ' NR ==2 {print $2 }'").readlines()
    #读取命令|删除第一行|读取第二行第二列
    print linea
    used= linea[0].rstrip()
    lineb=os.popen("sudo quota -uvs \'"+username+"\' |sed '1d' |awk ' NR ==2 {print $3 }'").readlines()
    userspace =lineb[0].rstrip()
    print used
    print userspace
    if int(filter(str.isdigit,userspace)) <=int(filter(str.isdigit,used)):
        state_a=2
    else:
        state_a=1
    print state_a
    cursor.execute("update account set state =%s where logname=%s",[state_a,username])
    cursor.execute("update account set userspace=%s,used=%s where logname =%s",[userspace,used,username])
    db.commit()
    print ("查询用户配额成功")

def spacechange(username):
    db=pymysql.connect("122.152.205.63", "yanzhouhan", "Yanzhouhan123456!", "collection")
    cursor=db.cursor()
    #读取数据库中用户空间
    cursor.execute("select userspace from account where logname=%s",username)
    (userspace,)=cursor.fetchone()
    userspacea=userspace[:-1]
    print userspacea
    userspaceb=int(userspacea)
    print userspaceb
    # 执行配额检查
    os.system("quotacheck -avug")
    #os.system('mount /dev/sdb  /home/%(username)s'% {'username':username})
    os.system('setquota -u %(username)s %(userspace)d %(userspace)d  5 8 /home/%(username)s'% {'username':username,'userspace':userspaceb})
    #os.system('umount -l /home/%(username)s'%{'username':username})
    cursor.execute("update account set state =1 where logname= %s ", username)  # 修改配额后将状态置为1
    print("****修改用户配额成功****")
    time.sleep(5)
def warnquota(username):
    os.system('echo %(username)s quota is full |mail -s "userquota warning" 1035028274@qq.com' %{'username':username})
    print("发送邮件提醒成功")
    time.sleep(20)




