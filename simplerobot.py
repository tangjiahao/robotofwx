from urllib import request,parse
import ssl
import json
import pymysql
import requests
import time
import re
import chart2


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
def serchdata(firstchar):
    # 查询数据库数据


    # 获取游标
    cursor = conn.cursor()

    print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    firstchar=' '+firstchar+'%'
    sql = "SELECT cyname FROM cydq where cyname like '%s'"%firstchar
    # print(sql)
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    if(cursor.rowcount>0):
        print("回答正确")
    else:
        print("该成语不存在，回答错误")
    print(cursor.rowcount)
    for row in rr:
        print("成语： %s\n"%row)

def serchonecybyround():
    sql="select cyname from cydq order by rand( ) limit 1";
    cursor = conn.cursor()
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中,这里只有一条
    key=''
    for row in rr:
        key=row[0].strip()#取出并去空格
        # print(len(key))
        return key
def serchsensitiveword():
    sql = "select badword from sensitiveword ";
    cursor = conn.cursor()
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中,这里只有一条
    wordlist=[]
    for row in rr:
        wordlist.append(row[0])
        # print(len(key))
    return wordlist

def serchonestorybyround():
    sql="select storymsg from story order by rand( ) limit 1";
    cursor = conn.cursor()
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中,这里只有一条
    key=''
    for row in rr:
        key=row[0]
        # for i in range(key):
        #     key[0]=
        # # print(len(key))
        return key

def serchonestorybyname(cy):
    # 查询数据库数据


    # 获取游标
    cursor = conn.cursor()

    print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    cy='%'+cy+"%"
    sql = "SELECT storymsg FROM story where storymsg like '%s'"%cy
    print(sql)
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    if cursor.rowcount>0:
        for row in rr:
            storymsg=row[0]
            return storymsg
    else:
        return "该哲理小故事没有找到，并没有收录，尽请期待作者更新"
#插入数据到成语大全表
def insertdata(sql0,*parm):#前二位第一位为数据库语句，第二位为插入的参数
    # 建立数据库连接

    # 获取游标

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
#读取文件把成语文件写入数据库
def readfile():
    f = open("acemake.txt", "r")  # 设置文件对象
    str = f.read()  # 将txt文件的所有内容读入到字符串str中
    s=str.split("\n")
    dic={}
    for line in s:
        key=line[0:line.find("拼音")]
        key.strip()
        value=line[line.find("释义：")+3:-1]
        dic[key]=value
    sql = "INSERT INTO cydq(cyname,mean) values(%s,%s)"

    for s in dic:
        print("key:",s,"value:",dic[s])
        insertdata(sql,s,dic[s])


    print(len(dic))
    f.close()  # 将文件关闭

#读故事文件写入数据库
def readfile2():
    s='''
    6．寻死的失恋青年
　　一位青年因为失恋，痛苦万分地坐在与恋人初遇的河边，准备投河自尽。恰逢大哲学家柏拉图走过来，问他是怎么回事。
　　“我失恋了。”青年目光呆滞地说道，“我爱她，把她当成我自己的生命来看待，没有了她，我一分钟都活不下去。反正没有了爱情我活着也是具行尸走肉，还不如死了好。”
　　“你们处了多久？”柏拉图问。
　　“两年，在这两年里，我无时无刻不……”青年喃喃着。
　　柏拉图打断了他的话:“那你能告诉我两年前，在还没有遇到她的时候你是怎么过的吗？”
　　青年的眼里有了一丝光彩：“那时候，我是个自由自在、无忧无虑的青年。每天我都会活力四射地生活、工作。领导和同事们都很喜欢我。我还好几次被评为优秀员工呢，光奖状都得到好几张。那时候，我还有过关于爱情的甜蜜幻想，那种幻想真美啊！可惜从今往后再也不会有了。”
　　“不，你当然可以有。”柏拉图大声说，“你看，命运是如此地爱你。它把你又送回了两年前，让你依然可以自由自在、无忧无虑地生活，并可以继续拥有自己美好的梦想，不是吗？”
　　想一想果真如此，青年便放弃了寻死的念头。
　　生命总会有一定程度的反复，当我们因为今天的失去而回复从前的生活时，让心情、想法也回到从前，不啻为幸福的一大秘诀。
　　7．盲僧
　　由于家里穷，养不起只吃饭不干活的人，天生双目失明的他被迫出家了。
　　经过多年苦学，他已经深通佛经。20岁时，他被师父老方丈定为了行脚僧，命他从此云游四海，解脱人间苦难。然后，老方丈送了他一个纸包和一根探路杖：“这纸包里是我寻求来的一个民间秘方。它能让你的双眼复明。但是，在打开这个纸包之前，你必须先做到一件事——因为探路敲断10根探路杖。”他答应了师父，然后便上路了。
　　一年又一年，他谨遵师命传播着佛经，度化着苦难的亡灵，不知经历了多少风雨，走过了多少里路。他的心中一直存着一个希望：敲断十根探路杖，让自己的眼睛重见光明。可是没想到那看起来不粗的探路杖用起来却异常结实，一直到第六个年头，师父送的那根杖子才终于断了。
　　就这样，等到这位盲僧真的敲断了10根探路杖时，他已经是八十多岁的白发老人了。但是当他欣喜若狂地把纸包递给一个药店的老板时，老板却告诉他：纸上一个字都没有。
　　盲僧顿时呆住了，但是几秒钟之后，他便双手合十，满脸感激了：“师父，谢谢你以这种方式让我一直活在希望里，我觉得不枉此生了。”
　　每个人生命的终极归宿都是坟墓，尽管如此，我们仍应尽量让活着的日子精彩有色。一直活在希望中，你就能感觉不虚此行。
　　8．极限
　　某登山俱乐部组织了一次攀登珠穆朗玛峰的活动，许多登山爱好者纷纷报名参加。在一个风和日丽的日子，他们开始了这趟极富险趣的挑战。
　　在最初的1000米，大家皆兴致勃勃，谁都不甘落后。
　　第二个1000米，一小部分人开始气喘吁吁，体力明显不支。
　　到了第三个1000米，已经有好几个人自动放弃了挑战。
　　坚持到第六个1000米时，原来四五十人的大队伍只剩下不到10个人了。看样子，这几个人都是决心坚持到最后了。但是在到达6400米的高度时，一个人突然停了下来，他指着自己的心脏对其他人说：“我不行了，你们上去吧。”说完，他便找了个比较安全的山洞钻了进去。
　　后来，所有爬到山顶的人均对这个人表示遗憾：就差那么一点点了，何不咬咬牙登上去呢？老了回忆起来，也算是完成了珠穆朗玛之旅了。
　　“不，”他微笑着摇摇头，表情很自然，“我原来是个登山运动员，我晓得我自己的极限，6400米是我生命的最高峰，所以我并没有什么遗憾。如果再往上登的话，除非我不要命。”
　　这句话顿时让所有人对他肃然起敬，为了他对挑战极限的明智理解，更为了他对生命的爱惜和尊重。
　　任何事情都存在突破口，但并非任何人都能跨越它，抵达更高的层次。量力而行，恰到好处，才是令人叹服的明智之举与最高境界。
    '''
    s1="""
   6.寻死的失恋青年
　　一位青年因为失恋，痛苦万分地坐在与恋人初遇的河边，准备投河自尽。恰逢大哲学家柏拉图走过来，问他是怎么回事。
　　“我失恋了。”青年目光呆滞地说道，“我爱她，把她当成我自己的生命来看待，没有了她，我一分钟都活不下去。反正没有了爱情我活着也是具行尸走肉，还不如死了好。”
　　“你们处了多久？”柏拉图问。
　　“两年，在这两年里，我无时无刻不……”青年喃喃着。
    2.四六级阿里
    上述地块
    3.少打了个
    十大垃圾管理开始大驾光临
    """
    f = open("story.txt", "r")  # 设置文件对象
    str = f.read()  # 将txt文件的所有内容读入到字符串str中
    sql = "INSERT INTO story(storymsg) values(%s)"
    count=0
    result=re.split('(\d{1,2}\．)',str)
    #保留了匹配项分割，做完之后发现用不带（）的不保留匹配项分割简单的多，都没有后续的判断语句
    for i in result:
        # print(i)
        # print("-----")
        #去掉7.这样的元素
        if re.match('(\d{1,2}\．)',i)==None:
            print("分割："+i)
            count+=1
            insertdata(sql,i)

    f.close()  # 将文件关闭
    print(count)

#读取小黄鸡聊天文件写入问答数据
def readfile3():
    f = open("xhj.txt", "r")  # 设置文件对象
    str = f.read()  # 将txt文件的所有内容读入到字符串str中
    s = str.split("E")
    dic = {}
    templist=[]
    for line in s:
        # print(line)
        s0=line.split("\n")
        if len(s0)==4:
            templist.append(s0)

    for line in templist:
        Q=line[1][line[1].find("M")+1:]
        A=line[2][line[2].find("M")+1:]
        dic[Q]=A

    for q in dic:
        # print(q+":"+dic[q])
        chart2.insertdata(q,dic[q])
if __name__ == '__main__':
    # serchdata()
    # readfile()
    # serchdata('左')
    # print("    sgaace    agsa   ".strip())
    # print(serchonecybyround())
    # readfile2()
    # print(serchonestorybyround())
    # readfile3()
    print(serchonestorybyname("谁更成功"))
    # readfile2()