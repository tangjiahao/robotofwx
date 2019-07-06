
from wxpy import *
import wxpy
import requests

from datetime import datetime

import time

from urllib import request,parse
import ssl
import json
import pymysql
import requests
import time
import simplerobot
import chart2
import random
from fuzzywuzzy import fuzz
bot = Bot(cache_path=True)
# robot_group = bot.search("robotace1")[0]

# robot_group = bot.groups().search({'robotace'})[0]
menustate=-1#机器人工作的状态量
cyjlchar=''#成语接龙的下一个成语的开头字符
ask=""#上一个问的问题
dictofcache={}#这个字典用来模拟缓冲区，记录问过的问题和答案，这样问相同问题就不用访问数据库
stackofcache=[]#这个是用来存储聊天的问题，当相同问题达到了三次以后，问题和回答就会被存入dictofcache用来提高聊天速度
sensitiveword=[]#敏感词库
##建立数据库连接
conn = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='tangjing666',
    db='robotforchat',
    charset='utf8'
)


#成语数据有个空格消不掉
def serchforcyjl(firstchar):
    # 查询数据库数据


    # 获取游标
    cursor = conn.cursor()

    print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    firstchar=' '+firstchar
    sql = "SELECT cyname FROM cydq where cyname='%s'"%firstchar
    print(sql)
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    if(cursor.rowcount>0):
        print("回答正确")
        return True

    else:
        print("该成语不存在，回答错误")
        return False
    # print(cursor.rowcount)
    # for row in rr:
    #     print("成语： %s\n"%row)

#成语提示
def cyts():
    # 查询数据库数据
    global cyjlchar
    firstchar=cyjlchar
    # 获取游标
    cursor = conn.cursor()

    print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    firstchar=' '+firstchar+"%"
    sql = "SELECT cyname FROM cydq where cyname like '%s'"%firstchar
    print(sql)
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    result="提示\n"
    count=0
    flag=False
    if(cursor.rowcount>0):
        flag=True
        for i in rr:
            key=i[0].strip()
            result+=key+"\n"
            count+=1
            #最多只返回五条数据
            if count==5:
                break


    else:

        result+="该字开头的成语不存在，建议重新开始成语接龙"
    return flag,result

    # print(cursor.rowcount)
    # for row in rr:
    #     print("成语： %s\n"%row)

#查询成语释义，成语数据有个空格消不掉
def serchmean(cy):
    # 查询数据库数据


    # 获取游标
    cursor = conn.cursor()

    print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    cy=' '+cy
    sql = "SELECT cyname,mean FROM cydq where cyname ='%s'"%cy
    print(sql)
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    if cursor.rowcount>0:
        for row in rr:
            cyname,mean=row
            return cyname,mean
    else:
        return cyname,"本成语没有收录，查找失败"





#user表示发送的用户，content是内容，state表明它是群组还是好友
def sendblogmsg(user,content,state):
  #搜索自己的好友，注意中文字符前需要+u

      print(user,content)

      if (state==2):
          my_group = bot.groups().search(user)[0]
          my_group.send(content)  # 发送天气预报
      elif(state==1):
          my_friend = bot.friends().search(user)[0]
          my_friend.send(content)

#删除里面和num相同的元素
def deletesamenum(num):
    global stackofcache
    l=len(stackofcache)
    x=0
    while x<l:
        if stackofcache[x]==num:
            stackofcache.remove(num)
            x-=1
            l-=1
        x+=1

#判断是否为原则问题，这些包括涉及机器人本身根本问题的
def isprinciple(sentence):
   problem=["你叫什么名字","你怎么称呼","你是谁","你父亲叫什么名字","你的制作者叫什么名字","你父亲是谁","你制作者是谁"]
   #比较原则性问题
   for i in problem:
       if fuzz.ratio(i,sentence)>80:
           return True

   return False

def getweather2(location):
    path="https://api.seniverse.com/v3/weather/now.json?key=Skb40T46PiBDM35V2&location=%s&language=zh-Hans&unit=c"
    path2="https://free-api.heweather.net/s6/weather?location=%s&key=a3269a0918a44a62ae97c314dd24f02a"
    url=path2%location
    res=requests.get(url)

    result=res.json()
    weather=""
    # print(result)

    if result['HeWeather6'][0]['status']=='ok':
        r1=result['HeWeather6'][0]
        # print(r1)
        s0=r1["basic"]["parent_city"]
        if s0!=location:
            s0=location+" 坐标城市:%s\n"%s0
        today=r1['now']
        s1='天气：%s\n'%today['cond_txt']

        s2="当前：%s℃  本日:%s~%s℃\n"%(today['tmp'],r1['daily_forecast'][0]['tmp_min'],r1['daily_forecast'][0]['tmp_max'])
        s3="风向：%s\n"%today['wind_dir']
        pm25=int(today['hum'])
        pollution=''
        if 0 <= pm25 < 35:

            pollution = '优'

        elif 35 <= pm25 < 75:

            pollution = '良'

        elif 75 <= pm25 < 115:

            pollution = '轻度污染'

        elif 115 <= pm25 < 150:

            pollution = '中度污染'

        elif 150 <= pm25 < 250:

            pollution = '重度污染'

        elif pm25 >= 250:

            pollution = '严重污染'
        s4="pm25:%s 空气质量:%s\n"%(pm25,pollution)
        lifetip=r1["lifestyle"]
        s5="紫外线:"
        s6="生活小贴士：\n"
        count=1
        for i in lifetip:
            if i['type'] not in ['sport','uv','comf','flu']:
                s6+=str(count)+':'+i['txt']+'\n'
                count+=1
            elif i['type']=='uv':
                s5+=i['txt']+'\n'
        weather=s0+s1+s2+s3+s4+s5+s6
        print(weather)
    else:
        print("没查到这个地区的天气信息，请检查地区名是否输入规范")
        weather="没查到这个地区的天气信息，请检查地区名是否输入规范"
    return weather

#获取音乐的链接
def geturlofmusic(hash,abid):
  path2 = 'http://www.kugou.com/yy/index.php?r=play/getdata&hash=%s&album_id=%s&_=1497972864535'
  path="https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191014887140948582345_1557824383110&hash=%s&album_id=%s&dfid=0zpwSa44LtGp0D89Gr371MJb&mid=51eafc9b0e5eaca4e106b905175401ec&platid=4&_=1557824383112"
  # 这个网址是获取音乐资源的网址，用到的hash和album_id是第一个网址获得值

  url2 = path% (hash, abid)
  res = requests.get(url2)
  s=res.text
  # print(s)
  temp=s[s.find('({')+1:s.find(');')]
  end=json.loads(temp)
  print(end)
  if(end['data']['play_url']):
      return end['data']['play_url']
  else:
      return None

#获取音乐的hash
def getmusic(music):
  path1= 'http://songsearch.kugou.com/song_search_v2?keyword=%spage=1&pagesize=3&userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0；'
  # 这个网址是为了获取下个网址需要的哈希值
  url1 = path1 % music
  response = requests.get(url1)
  result=response.json()
  # print(result)


  if(result["data"]['lists']):
      msg= result["data"]['lists'][0]
      # 尝试获取返回元素的第一个，资源有可能为空，因为第一个一般返回的是原唱，可能需要vip

      for key in result["data"]['lists']:
        print(key)
      name=msg['FileName']

      hash=msg['FileHash']
      abid=msg['AlbumID']
      mc=geturlofmusic(hash,abid)
      if(mc):
        mcurl=mc
        print("第一个："+mcurl)
        return mcurl,name
      else:
        #原唱歌手的资源没有，尝试第二个
        msg=result["data"]['lists'][1]
        hash = msg['FileHash']
        abid = msg['AlbumID']
        mc = geturlofmusic(hash, abid)
        if (mc):
          mcurl = mc
          print("第二个："+mcurl)
          return mcurl,name
        else:
          print("该音乐没有资源链接")
  else:
    print("找不到该音乐的hash")
def choosedoth(str,user,state):
    global menustate,cyjlchar,ask,dictofcache,stackofcache,sensitiveword

    # print("进入了选择函数")
    if("~糖糖" in str):
        # print("捕获到了正确的句子")
        s=str.split()
        if(len(s)==3):
            if s[1]=="天气预报":
                print("查询%s天气信息"%s[2])
                msg=getweather2(s[2])
                print(msg)
                sendblogmsg(user,msg,state)

            elif s[1]=="点歌":
                print("进入点歌")

                url,name=getmusic(s[2])

                s=name+":\n"+url
                sendblogmsg(user,s,state)
            elif s[1]=="成语词典":
                print("查成语")

                cyname,mean=serchmean(s[2])

                s=cyname+":\n"+mean
                sendblogmsg(user,s,state)
            elif s[1]=="讲故事":
                print("查询特定故事%s"%s[2])
                msg=simplerobot.serchonestorybyname(s[2])
                print(msg)
                sendblogmsg(user,msg,state)




            else:
                print("功能格式输入错误1")
                sendblogmsg(user, "功能格式使用错误，请检查", state)
                return
        elif(len(s)==2):
            if s[1]=="使用说明":
                s1="大家好，我是微信机器人糖糖，请多指教！下面是我的技能说明：\n"
                s1+="1:智能聊天  请输入~糖糖 陪我聊天\n"
                s1+="2:天气预报  请输入~糖糖 天气预报 城市（可精确到区）\n"
                s1+="3:快捷点歌  请输入~糖糖 点歌 歌名\n"
                s1+="4:成语接龙  请输入~糖糖 成语接龙\n"
                s1+="5:成语词典  请输入~糖糖 成语词典 成语名\n"
                s1+="6:讲故事  请输入~糖糖 讲故事\n"
                # print(s1)
                sendblogmsg(user,s1,state)
            elif s[1]=="tj666":
                s="触发金手指说明：\n"
                s+="1在聊天模式下：输入 ~（空格)重新教 原问题 新回答 可以修改原问题的答案\n"
                s+="2在成语接龙模式下：输入 ~(空格)成语提示 可以获得成语接龙提示\n"
                s+="3讲故事功能可以讲特定故事：输入~糖糖 讲故事 故事名即可\n"
                sendblogmsg(user,s,state)
            elif s[1]=="成语接龙":
                print("进入成语接龙")
                if menustate==4:
                    sendblogmsg(user,"已经处于成语接龙模式了亲，不要重复无意义指令喔",state)
                    return
                s=simplerobot.serchonecybyround()

                cyjlchar=s[-1]#记住上个成语的最后一个字符
                flag,ts=cyts()
                #如果随机给出的成语无法进行下一个接龙，就重新给个成语
                while(not flag):
                    s=simplerobot.serchonestorybyround()
                    cyjlchar=s[-1]
                    flag,ts=cyts()
                menustate = 4  # 这个全局变量让机器人知道进入了成语接龙模式
                sx = "已进入成语接龙模式，随机给出一个成语：" + s + "\n"
                sx += "请继续接龙,输入 ~ (中间有个空格)接龙的成语 即可\n 想结束成语接龙，输入 ~ (中间有个空格)结束接龙 即可"

                sendblogmsg(user,sx,state)
            elif s[1]=="讲故事":
                print("进入讲故事")
                s=simplerobot.serchonestorybyround()
                sendblogmsg(user,s,state)
            elif s[1]=="陪我聊天":
                if menustate==1:
                    sendblogmsg(user,"已经处于聊天模式了亲，不要重复无意义指令喔",state)
                    return
                print("进入智能聊天")
                s=simplerobot.serchsensitiveword()
                sensitiveword=s[:]#复制内容
                s="你好，性感糖糖，在线陪聊！\n 已进入智能聊天模式，可以用~(空格) 聊天内容 跟我聊天\n"
                s+="糖糖会自我学习喔，如果我不会，你可以用 ~ 教你 教导内容 指导我\n 想结束智能聊天，输入 ~ (中间有个空格)结束聊天 即可"
                sendblogmsg(user,s,state)
                menustate=1

            else:
                print("句子错误")
                sendblogmsg(user, "功能格式使用错误，请检查", state)
                return
    elif ("~" in str and menustate>0):
        s=str.split()

        if(len(s)>=2):
            # print("进入了成语接龙的判定")
            errmsg = "错误的句子格式，未识别"
            if menustate==4 and cyjlchar!='':
                if cyjlchar==s[1][0] and serchforcyjl(s[1]):
                    cyjlchar=s[1][-1]
                    result="成语接龙回答正确,QVQ!请再接再厉\n请以下一个成语:"+s[1]+" 的最后一个字符："+cyjlchar+"  继续接龙"
                    sendblogmsg(user,result,state)
                elif s[1]=="结束接龙":
                    menustate = -1
                    cyjlchar = ''
                    sendblogmsg(user, "成语接龙已结束", state)
                elif s[1]=='成语提示':
                    flag,ts=cyts()
                    sendblogmsg(user,ts,state)
                else:
                    result="成语接龙回答错误qwq,有请下一个朋友回答："
                    sendblogmsg(user, result, state)
            elif menustate==1 and s[1]=="教你":
                print("进入教学模式")
                answer=s[2]
                que1,que2=chart2.sentencedeletemark(ask)#去掉问题的标点符号
                if isprinciple(que1):
                    sendblogmsg(user,"教导的问题为原则性问题，答案不可更改",state)
                    return
                for word in sensitiveword:
                    if word in answer:
                        sendblogmsg(user, "教导的内容包含敏感词汇："+word+"，糖糖拒绝学习", state)
                        return
                chart2.insertdata(que1,answer)
                s="糖糖学会了，谢谢您嘞！"
                sendblogmsg(user,s,state)
                dictofcache.pop(ask)
            elif menustate==1 and s[1]=="重新教":
                print("重新教学模式")
                if(len(s)==4):
                    problem=s[2]
                    answer=s[3]
                    if isprinciple(s[2]):
                        sendblogmsg(user, "教导的问题为原则性问题，答案不可更改", state)
                        return
                    for word in sensitiveword:
                        if word in answer:
                            sendblogmsg(user, "教导的内容包含敏感词汇：" + word + "，糖糖拒绝学习", state)
                            return
                    if(chart2.updatedata(s[3],s[2])):
                        sendblogmsg(user,"关于 %s 糖糖已经重新更正了答案"%s[2],state)
                        dictofcache.pop(ask)
                        print("缓存中的回答已经移除")
                    else:
                        sendblogmsg(user, "关于 %s 没有找到原问题，答案更新失败" % s[2], state)
            elif menustate==1 and s[1]!="教你" and s[1]!="结束聊天":
                print("进入聊天模式")
                ask = s[1]
                #如果问题问过且有答案，直接使用缓存的答案，不查找数据库
                if ask in dictofcache.keys():

                    answer="这句话说过多次亲，"+dictofcache[ask]
                    sendblogmsg(user,answer,state)
                    return
                result=chart2.chatwithrobot(s[1])

                print(result)
                if(result):
                    #如果有答案的问题，将这个问题加入问题栈里
                    stackofcache.append(ask)
                    answer=result
                    if stackofcache.count(ask)>=3:
                        dictofcache[ask] = result  # 这个问题问了多次，缓存不存在答案，且数据库能找到答案加入到缓存中
                        deletesamenum(ask)#把问过多次的问题从问题栈删除，节省内存

                    sendblogmsg(user,answer,state)
                else:
                    answer="糖糖不知道呢，教我qwq！"
                    sendblogmsg(user,answer,state)
            elif menustate==1 and s[1]=="结束聊天":
                menustate = -1
                ask=''
                dictofcache={}
                sendblogmsg(user, "陪聊结束", state)





    else:
        print("没捕获到")

#这是监听好友信息的注册函数
@bot.register(bot.friends(),except_self=False)
def print_messages(msg):
    # print(msg)
    print("微信好友监听")
    print(msg.text)
    # print(msg.type)
    print(msg.chat.remark_name)

    print("微信好友")
    choosedoth(msg.text,msg.chat.remark_name,1)

group=["robotace1","小老弟1"]
# 这是监听微信群的注册函数
@bot.register(Group,except_self=False)
def ace2(msg1):
    print("进入了微信群监听")
    print(msg1)
    # print(msg1.text)
    # print(msg1.sender.name)
    #
    # print(msg1.type)
    line=str(msg1)
    #这里获得微信群的群名称
    group_name=line[0:line.find(' ')]
    print(group_name)
    if group_name not in group:
        print("该群聊不需要监管")
    else:
        choosedoth(msg1.text,group_name, 2)
# # 这是监听微信群的注册函数
# @bot.register(robot_group,except_self=False)
# def ace1(msg1):
#     global robot_group
#     print("进入了微信群监听")
#     print(msg1.text)
#     # print(msg1.type)
#     print(robot_group.name)
#     # print(msg1.sender)
#     # print(msg1.chat.owner.name)
#     # print(msg1.member.name)
#     # robot_group.send("hello")
#
#     # s=robot_group.name
#     print("微信群")
#
#     choosedoth(msg1.text,robot_group.name,2)


if __name__ == '__main__':
    # msg=send_weather("广州番禺")
    # sendblogmsg('acemake',msg)
    # 机器人账号自身
    myself = bot.self
    # robot_group.send("hello word")
    # 向文件传输助手发送消息
    # bot.file_helper.send('Hello from wxpy!')
    bot.join()
    # isprinciple("adog")




