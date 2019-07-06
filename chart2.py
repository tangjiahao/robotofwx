# -*- coding=utf-8 -*-
import requests
import itchat
import random
import jieba
import random
from urllib import request,parse
import ssl
import json
import pymysql
import requests
import time
import re
from wxpy import *
import copy
from fuzzywuzzy import fuzz
KEY = '2de1c72204a048679add5cb3b19c525b'


# 建立数据库连接
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='tangjing666',
    db='robotforchat',
    charset='utf8'
)

#成语数据有个空格消不掉
def serchanswer(sql):
    # 查询数据库数据
    print(sql)

    # 获取游标
    cursor = conn.cursor()

    # print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"


    # print(sql)
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    listace = []
    if(cursor.rowcount>0):
        # print("找到回答")

        for row in rr:
            # print("回答： %s\n" % row[0])
            listace.append(row[0])

    else:
        print("没找到回答")
    # print(cursor.rowcount)
    return listace

#插入数据到聊天库
def insertdata(*parm):#传入参数为可变参数，分别为问题和答案
    # 建立数据库连接

    # 获取游标
    sql0="insert into chatrobot(ask,answer) values(%s,%s)"
    cursor = conn.cursor()
    # print(cursor.rowcount)

    # 2数据库中插入数据
    # sql_insert = "INSERT INTO aircompany() values(%s,%s)"
    # 执行语句
    try:
        cursor.execute(sql0,parm)
        # 事务提交，否则数据库得不到更新
        conn.commit()
        print("插入成功")
    except Exception:
        print("插入失败")
        conn.rollback()
def updatedata(*parm):
    sql0 = "update chatrobot set answer='%s' where ask='%s'"%parm
    cursor = conn.cursor()
    # print(cursor.rowcount)

    # 2数据库中插入数据
    # sql_insert = "INSERT INTO aircompany() values(%s,%s)"
    # 执行语句
    try:
        cursor.execute(sql0)
        # 事务提交，否则数据库得不到更新
        conn.commit()
        print("更新成功")
        return True
    except Exception:
        print("更新失败")
        conn.rollback()
        return False
def chatwithall():

    # 扫码登陆
    bot = Bot()

    # 初始化图灵机器人 (API key 申请: http://tuling123.com)
    tuling = Tuling(api_key=KEY)


    # 自动回复所有文字消息
    @bot.register(msg_types=TEXT)
    def auto_reply_all(msg):
        tuling.do_reply(msg)



    # 开始运行
    bot.join()
#判断一个单词是否为中文单词或者英文单词
def isAllZh(s):
    if s.isalpha():
        return True
    for c in s:
        if not('\u4e00' <= c <= '\u9fa5'):
            return False
    return True


#把句子的符号去掉,返回一个不带符号的句子和它的关键词列表
def sentencedeletemark(str):
    str=jieba.lcut(str)
    newstr=[]
    s=""
    for i in str:
        if isAllZh(i):
            s+=i
            newstr.append(i)
    return s,newstr
def searchmatch(str):
    sql="select answer from chatrobot where ask='%s'"%str
    return serchanswer(sql)

def searchmohumatch(str):
    sql = "select answer from chatrobot where ask like '%s'" % str
    # print(sql)
    return serchanswer(sql)

#把关键词左右加上*，如我/喜欢/你，改为*我*喜欢*你*
def wordaddstr(listace):
    if listace:
        s=""
        for i in listace:
            i='%'+i
            s+=i
        s+='%'
        return s
    else:
        print("空字符串，无法转化")

def combineword(list,maxlen,lenofstr,lenoflist):

    lx=[]
    count=0
    for i in list:
        if len(i)==maxlen:
            lx.append(i)
            count+=len(i)
    #如果这个列表的单词数小于等于一且单词数同时小于分析的句子列表的单词数的一半和列表元素总长度小于分析的句子长度的一半,就不返回
    if len(lx)<=1 and len(lx)<lenoflist and count<lenofstr:
       return []
    return lx
#找到一个list中的最长元素
def findmaxlenofnum(listace):
    max=0
    for i in listace:
        if len(i)>max:
            max=len(i)
    return max

def combinesql(list):
    sqllist=[]
    sqlx=wordaddstr(list)
    sqllist.append(sqlx)

    #如果去掉一个列表元素的sql语句,它的占比达到了65%以上,那就再试试组合分词的sql语句
    if((len(list)-1)/len(list)>=0.65):
        for i in range(len(list)):

            temp = list[:]#这个相当于复制内容，但两个列表的内容独立
            temp.pop(i)#根据下标删除元素，考虑到列表中有可能有相同的元素
            sqly=wordaddstr(temp)
            sqllist.append(sqly)
    return sqllist
def chatwithrobot(str):
    newstr,newlist=sentencedeletemark(str)
    lenofstr=int(len(newstr)/2)
    lenoflist=int(len(newlist)/2)
    s1=searchmatch(newstr)
    if(len(s1)>0):
        return random.sample(s1,1)[0]
    else:


        s2=wordaddstr(newlist)
        list2=searchmohumatch(s2)
        if list2:
            return random.sample(list2, 1)[0]
        #直接分词模糊查询查不到，最大单词的长度是大于1才进行分词分析，组合关键词开始模糊查询,不然很容易词不达意
        elif len(list2)==0 and (findmaxlenofnum(newlist))>1:
            maxlen=findmaxlenofnum(newlist)
            temp=int(copy.deepcopy(maxlen)/2)
            flag=0#默认没找到的标志量
            while(maxlen>=temp and flag==0 and maxlen!=1):
                lx=combineword(newlist,maxlen,lenofstr,lenoflist)
                if(len(lx)>0):
                   sqllist=combinesql(lx)
                   for sql in sqllist:
                       res=searchmohumatch(sql)
                       if len(res)>0:
                           flag=1
                           list2=res[:]
                           break

                       else:
                           continue
                   if flag==0:
                        maxlen-=1
                else:
                    maxlen-=1
                    continue
            if flag==1:
                return random.sample(list2, 1)[0]
            else:
                return None






# tuling = Tuling(api_key=KEY)
if __name__ == '__main__':

    str="你的master是谁？"
    # print(int(5/2))
    # print(5/2)

    # s=2
    # c=copy.deepcopy(s)
    # s=5
    # print(s)
    # print(c)
    # print(jieba.lcut(str))
    # print(chatwithrobot(str))
    print(2/3)
