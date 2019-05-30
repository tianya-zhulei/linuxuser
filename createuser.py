#coding=utf-8
#!/usr/bin/python
import time
import os
import sys
sys.path.append('/home/zhulei/PycharmProjects/untitled/venv/lib/python2.7/site-packages') # 当前项目路径加入
import pymysql
print(sys.path)
import spacetest
import userlog
userpassword =111111 #初始化密码111111
while True:
  db = pymysql.connect("122.152.205.63", "yanzhouhan", "Yanzhouhan123456!", "collection")
  cursor = db.cursor()  # 使用 cursor() 方法创建一个游标对象 cursor
# 连接数据库遍历获取人名

  cursor.execute("select spell from student order by id desc")
  spells = cursor.fetchall() #用户名
  for (spella,) in spells:

    cursor.execute("select number from student where spell =%s",spella)
    (number,) = cursor.fetchone()

    username=spella+str(number)#用户名等于姓名加学号，防止重复
    print username

# 连接数据库获取组名
    cursor.execute("select classID from student where spell=%s",spella)
    (classID,)=cursor.fetchone()
    print classID

    cursor.execute("select classspell from class where id = %s",classID)
    (classspell,) = cursor.fetchone() #组名
    print classspell
# 获取系统时间
    createdate = time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))
    directory='/home/'+username
    print directory
    try:
     print "用户名:",username
     print "密码:",userpassword
     print createdate
    except Exception, e:  #异常报错
     print e.message
#状态1
    state=0#状态，0表示还未分配帐号
# 插入account表
    sql = "INSERT INTO account(logname,password,groupa,directory,state,createtime)" \
           " VALUES(\'"+str(username)+"\',\'"+str(userpassword)+"\'," \
           "\'"+str(classspell)+"\',\'"+str(directory)+"\',"+str(state)+"," \
             "\'"+str(createdate)+"\') "
    #print sql
    try:
# 执行sql语句
      cursor.execute(sql)
   # 提交到数据库执行
      db.commit()
      print('插入数据库成功')
    except Exception, e:
   # 如果发生错误则回滚
      print('插入数据库失败')
      print e.message
      db.rollback()
      cursor.execute("SELECT * FROM account") # 使用 execute()  方法执行 SQL 查询
      data = cursor.fetchall() # 使用 fetchone() 方法获取单条数据.
      #print data   #打印数据
# 创建linux用户
    #判断数据库用户状态
  cursor.execute("select logname from account order by id ")
  lognames=cursor.fetchall()
  for (logname,) in lognames:
    cursor.execute("select state from account where logname=%s ",logname)
    (state,)=cursor.fetchone()  #查询用户状态
    cursor.execute("select groupa from account where logname =%s",logname)
    (groupa,)=cursor.fetchone()
    while state ==0: #状态等于0时新建linux用户
             print('创建linux用户...')
             print logname
             os.system('groupadd %(groupa)s' % {'groupa' : groupa}) #新建组
             os.system('useradd  -d /home/%(name)s  -g %(group)s -m %(logname)s' % {'name': logname,'group':groupa,'logname':logname})
             os.system('echo %(name)s:%(pwd)s |chpasswd' %
                           {'name': logname, 'pwd': userpassword})   #设置密码

             os.system('echo "您好,您的账号为：" %(name)s ",密码为:" %(pwd)s' % {'name': logname, 'pwd': userpassword})
             # 状态1表示已分配linux帐号
             cursor.execute("UPDATE account SET st"
                            "ate=1 WHERE logname = %s", logname)
             db.commit()
             #给指定用户配额
             os.system('sudo mount /dev/sdb /home/%(username)s'% {'username':logname})
             os.system('sudo mount -o remount,usrquota,grpquota /home/%(username)s' % {'username':logname})
             #执行配额检查
             os.system("quotacheck -avug")
             os.popen("sudo quotaon -vug /home/\'"+logname+"\'",'w',1)
             os.system('setquota -u %(username)s 1000 2000 5 8 /home/%(username)s'% {'username':logname})
             os.system('chown %(username)s /home/%(name)s' % {'username': logname, 'name': logname})  # 设置该路径权限
             #os.system("umount -l /home/%(username)s "%{'username':logname})
             break
    while state==3:
            #状态等于3时准备删除用户
            #先取消配额
            os.system('umount -l /home/%(username)s' % {'username': logname})
            # 2.删除用户
            os.system('userdel -rf %(username)s' % {'username': logname})
            print('删除账号成功')
            # 获取系统时间
            deldate = time.strftime('%Y.%m.%d %H:%M', time.localtime(time.time()))  # 删除用户时的时间
            print deldate
            #修改state为4表示已经删除帐号
            state=4
            cursor.execute("update account set state =4 where logname= %s ", logname) #状态为4时表示已经删除成功
            cursor.execute("update account set userspace = NULL where logname= %s ",logname) #设置用户配额为NULL
            cursor.execute("update account set used = NULL where logname= %s ",logname) #设置用户已使用空间为NULL
            db.commit()
            break
    while state in {1}:
        spacetest.userspace(logname)
        userlog.userlog(logname)
        break
    while state==2:
        spacetest.spacechange(logname)
        spacetest.warnquota(logname)
        break
  time.sleep(10)
  db.close()# 关闭数据库连接


