from urllib import request,parse
import ssl
import json
import pymysql
import requests
import time
airportnostr="""
北京首都国际机场 PEK 北京 
上海浦东国际机场 PVG 上海 
广州白云国际机场 CAN 广东广州 
上海虹桥国际机场 SHA 上海 
深圳宝安国际机场 SZX 广东深圳 
成都双流国际机场 CTU 四川成都 
昆明巫家坝国际机场 KMG 云南昆明 
海口美兰机场 HAK 海南海口 
西安咸阳国际机场 SIA 陕西西安 
杭州萧山国际机场 HGH 浙江杭州 
厦门高崎国际机场 XMN 福建厦门 
重庆江北国际机场 CKG 重庆 
青岛流亭机场 TAO 山东青岛 
大连周水子国际机场 DLC 辽宁大连 
南京禄口国际机场 NKG 江苏南京 
武汉天河机场 WUH 湖北武汉 
沈阳桃仙国际机场 SHE 辽宁沈阳 
乌鲁木齐地窝堡国际机场 URC 新疆乌鲁木齐 
长沙黄花国际机场 CSX 湖北长沙 
福州长乐国际机场 FOC 福建福州 
桂林两江机场 KWL 广西桂林 
哈尔滨太平国际机场 HRB 黑龙江哈尔滨 
贵阳龙洞堡机场 KWE 贵州贵阳 
郑州新郑国际机场 CGO 河南郑州 
三亚凤凰机场 SYX 海南三亚 
温州永强机场 WNZ 浙江温州 
济南遥墙机场 TNA 山东济南 
宁波栎社机场 NGB 浙江宁波 
天津滨海国际机场 TSN 天津 
太原武宿机场 TYN 山西太原 
南宁吴圩机场 NNG 广西南宁 
南昌昌北机场 KHN 江西南昌 
长春大房身机场 CGQ 吉林长春 
张家界荷花机场 DYG 湖南张家界 
合肥骆岗机场 HFE 安徽合肥 
西双版纳嘎洒机场 JHG 云南西双版纳 
泉州晋江机场 JJN 福建晋江 
兰州中川机场 LHW 甘肃兰州 
烟台莱山机场 YNT 山东烟台 
九寨黄龙机场 JZH 四川九寨沟 
丽江三义机场 LJG 云南丽江 
汕头外砂机场 SWA 广东汕头 
呼和浩特据白塔机场 HET 内蒙古呼和浩特 
拉萨贡嘎机场 LXA 西藏拉萨 
珠海三灶机场 ZUH 广东珠海 
银川河东机场 INC 宁夏银川 
延吉朝阳川机场 YNJ 吉林延吉 
武夷山机场 WUS 福建武夷山 
西宁曹家堡机场 XNN 青海西宁 
湛江机场 ZHA 广东湛江 
舟山机场 HSN 浙江舟山 
黄山屯溪机场 TXN 安徽黄山 
宜昌三峡机场 YIH 湖北宜昌 
喀什机场 KHG 新疆喀什 
包头二里半机场 BAV 内蒙古包头 
伊宁机场 YIN 新疆伊宁 
大理机场 DLU 云南大理 
北海福成机场 BHY 广西北海 
石家庄正定机场 SJW 河北石家庄 
常州奔牛机场 CZX 江苏常州 
库尔勒机场 KRL 新疆库尔勒 
黄岩路桥机场 HYN 浙江黄岩 
义乌机场 YIW 浙江义乌 
攀枝花保安营机场 PZI 四川攀枝花 
敦煌机场 DNH 甘肃敦煌 
阿勒泰机场 AAT 新疆阿勒泰 
绵阳南郊机场 MIG 四川绵阳 
牡丹江海浪机场 MDG 黑龙江牡丹江 
徐州观音机场 XUZ 江苏徐州 
宜宾莱坝机场 YBP 四川宜宾 
威海机场 WEH 山东威海 
西昌青山机场 XIC 四川西昌 
柳州白莲机场 LZH 广西柳州 
海拉尔东山机场 HLD 内蒙古海拉尔 
阿克苏机场 AKU 新疆阿克苏 
景德镇机场 JDZ 江西景德镇 
连云港白塔埠机场 LYG 江苏连云港 
南通兴东机场 NTG 江苏南通 
泸州蓝田机场 LZO 四川泸州 
和田机场 HTN 新疆和田 
榆林西沙机场 UYN 陕西榆林 
洛阳北郊机场 LYA 河南洛阳 
临沧机场 LNJ 云南临沧 
铜仁大兴机场 TEN 贵州铜仁 
常德桃花源机场 CGD 湖南常德 
保山机场 BSD 云南保山 
临沂机场 LYI 山东临沂 
佳木斯东郊机场 JMU 黑龙江佳木斯 
长治王村机场 CIH 山西长治 
梅县机场 MXZ 广东梅县 
齐齐哈尔三家子机场 NDG 黑龙江齐齐哈尔 
汉中机场 HZG 陕西汉中 
赣州黄金机场 KOW 江西赣州 
塔城机场 TCG 新疆塔城 
延安二十里堡机场 ENY 陕西延安 
潍坊机场 WEF 山东潍坊 
库车机场 KCA 新疆库车 
丹东浪头机场 DDG 辽宁丹东 
赤峰机场 CIF 内蒙古赤峰 
吉林二台子机场 JIL 吉林吉林 
南阳姜营机场 NNY 河南南阳 
盐城机场 YNZ 江苏盐城 
嘉峪关机场 JGN 甘肃嘉峪关 
思茅机场 SYM 云南思茅 
秦皇岛山海关机场 SHP 河北秦皇岛 
锡林浩特机场 XIL 内蒙古锡林浩特 
锦州小领子机场 JNZ 辽宁锦州 
乌兰浩特机场 HLH 内蒙古乌兰浩特 
通辽机场 TGO 内蒙古通辽 
东营机场 DOY 山东东营 
乌海机场 WUA 内蒙古乌海 
衢州机场 JUZ 浙江衢州 

"""

dictchart={}
def getcitychart():
    global airportnostr
    airportnostr=airportnostr.replace("\n",'')
    temp=airportnostr.split(" ")
    print(temp)
    for i in range(0,len(temp)-1,3):
        dictchart[temp[i]]=temp[i+1]
    print(dictchart)

# 链接数据库
def linkdba():
    # 建立数据库连接
    conn = pymysql.Connect(
        host='localhost',
        port=3306,
        user='root',
        passwd='tangjing666',
        db='manoftravel',
        charset='utf8'
    )

    return conn

conn=linkdba()

#创建表的方法
def createtable(sql0,conn):
    try:
        cursor = conn.cursor()
        cursor.execute(sql0)
        # 事务提交，否则数据库得不到更新
        conn.commit()
        print("表创建成功")
    except Exception:
        print("创建失败")
        conn.rollback()


#查询数据库中的航空公司信息
def serchdata(conn):
    # 查询数据库数据


    # 获取游标
    cursor = conn.cursor()

    print(cursor)

    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    sql = "SELECT *FROM aircompany"
    # cursor执行sql语句
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    print(cursor.rowcount)
    for row in rr:
        print("公司代号：%s  公司名： %s\n"%row)

#插入数据到航空公司表
def insertdata(sql0,conn,*parm):#前二位第一位为数据库语句，第二位为链接对象，第三位为插入的参数
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
        # print("插入成功")
    except Exception:
        # print("插入失败")
        conn.rollback()
    # print(cursor.rowcount)
    # 修改数据库中的内容
    # sql_update="update student SET age='1001' WHERE no='119'"
    # cursor.execute(sql_update)
    # conn.commit()
    # # # # 数据库连接和游标的关闭
    # conn.close()
    # cursor.close()

# 判断爬虫要爬的网页是否已经爬过
def judgepath(urlpath):
    sql="select * from spider where urlpath='%s'"%urlpath
    # print(sql)
    cursor=conn.cursor()
    cursor.execute(sql)
    # 如果这个网页已经爬过，返回一
    if(cursor.rowcount>0):
        return 1
    return 0

#爬取信息，返回json格式的数据
def splide_data(depCity, depTime,arrCity):
    url = 'https://sjipiao.fliggy.com/searchow/search.htm'
    data = {
        "tripType": 0,
        "depCityName": depCity,
        "arrCityName": arrCity,
        "depDate": depTime,
        "_input_charset": "utf-8"

    }
    parturl=arrCity+depTime+depCity

    data = parse.urlencode(data).encode("utf-8")

    url = url + "?" +str(data)
    # print(parturl)
    if judgepath(parturl)==0:
        # 如果这个网址爬虫没爬过，就记录下这个网址，开始爬取，相当于给了爬虫记忆功能
        sql_spider = "insert into spider values(%s)"
        insertdata(sql_spider,conn,parturl)

        # 构造一个包含请求头的请求对象
        myheaders = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Cookie": "isg=BHl5FnbNBlrY8NrccL-5wn--i-OTLkZIsn-yNpuu6qAfIpm049Z9COdQoOZxgQVw; cna=4mmnE+Hx0y4CAQ5qtip+2mT1; UM_distinctid=163f6e437a7233-0988e10cc477588-4a5268-13c680-163f6e437a928f; CNZZDATA30066717=cnzz_eid%3D102330317-1528852370-https%253A%252F%252Fwww.fliggy.com%252F%26ntime%3D1530006354; hng=CN%7Czh-CN%7CCNY%7C156; t=81a8f159bac7fb2d01136453a627513e; _tb_token_=ed10746e8a739; cookie2=1c8c54cc97c608811a089a0daeaf5ac4; uc1=cookie14=UoTfK7MwBo5m%2Bg%3D%3D&lng=zh_CN&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&existShop=false&cookie21=VT5L2FSpccLuJBreK%2BBd&tag=8&cookie15=U%2BGCWk%2F75gdr5Q%3D%3D&pas=0; uc3=nk2=rNFs4AkrKBMxxs1Y&id2=UU6gZ9mno5%2F5lg%3D%3D&vt3=F8dBzr7Bozd4gS2qORw%3D&lg2=UtASsssmOIJ0bQ%3D%3D; tracknick=%5Cu7FA1%5Cu6155%5Cu4F46%5Cu4E0D%5Cu9700%5Cu8981; ck1=""; lgc=%5Cu7FA1%5Cu6155%5Cu4F46%5Cu4E0D%5Cu9700%5Cu8981; csg=8e347a8a; skt=fc2f5a54f1650832; _umdata=E2AE90FA4E0E42DE4E236337705D78437A26A9FBCB2F4D006B8C956EC1FFCE4723AA8E471D9FA86ECD43AD3E795C914C51B65946CF1468A535777C0A2A42E20F; x5sec=7b226174783b32223a223363343239316336356363373833616166316334636363306464306263366563434c6537794e6b46454f335a326f2b4d742f53327a514561444449324d5459314e7a4d794e6a59374d773d3d227d; l=aBDt7gIZHbm3gAbmtMaTjXb_7707atBkjHgFEMakHiThNTOpwxx_AJ-o-Vwy9_qC5PFy_X-iI",
            "Host": "sjipiao.fliggy.com",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
        }

        resp = requests.get(url,headers=myheaders)
        time.sleep(3)
        print(resp)
        if (resp.status_code==200):
            print("请求成功")
            result = resp.text
            # print(result)
            result = result.replace("(", "")
            result = result.replace(");", "")
            result_json=json.loads(result)
            # 这判断一下是否存在这条航线
            if result_json.get("atwHosts")!=None:
                # print(result_json.get("atwHosts"))
                # print(result_json.get("data").get("aircodeNameMap"))
                # print(result_json.get("data").get("flight"))
                print(result_json)
                return result_json
            else:
                print("爬取得航线不存在，跳过")
                return None
    else:
        print("该网址爬过，跳过")
        return None





# 讲json里的数据分门别类存到数据库
def insertallmessage(conn,data_json):
    if data_json:
        # print(data_json.get("data").get("aircodeNameMap"))
        # print(data_json.get("data").get("airportMap"))
        # print(data_json.get("data").get("flight"))
        # 插入航空公司信息
        # sql_aircompany="insert into airCompany(acno,acname) values(%s,%s)"
        # aircompany=data_json.get("data").get("aircodeNameMap")
        # for ac in aircompany:
        #     # print(ac,aircompany[ac])
        #     insertdata(sql_aircompany,conn,ac,aircompany[ac])


        depcity=data_json.get("data").get("depCityName")
        arrcity=data_json.get("data").get("arrCityName")
        print(depcity,arrcity)
        # 插入航班信息
        sql_flight = 'insert into Flight(flightno,airlinecode,arrairport,arrterm,depairport,depterm,deptime,arrtime,flighttype,price,totalseats,remainseats,depcity,arrcity) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        flights = data_json.get("data").get("flight")
        for flight in flights:
            # print(flight)
            # print(sql_flight)
            # print(flight.get("flightNo"), flight.get("airlineCode"), flight.get("arrAirport"), flight.get("arrTerm"),
            #       flight.get("depAirport"), flight.get("depTerm"), flight.get("depTime"), flight.get("arrTime"),
            #       flight.get("flightType"), flight.get("cabin").get("basicCabinPrice"),
            #       flight.get("cabin").get("bestDiscount"), flight.get("cabin").get("bestPrice"))
            insertdata(sql_flight, conn, flight.get("flightNo"), flight.get("airlineCode"), flight.get("arrAirport"),
                       flight.get("arrTerm"), flight.get("depAirport"), flight.get("depTerm"), flight.get("depTime"),
                       flight.get("arrTime"), flight.get("flightType"), flight.get("cabin").get("basicCabinPrice"),
                       150,150,depcity,arrcity)
            # print(1)



def getcitynametono(conn,data_json):
    if data_json:
        # print(json)
        sql_aircompany="insert into Nametono(cityname,cityno) values(%s,%s)"
        ctname1=data_json.get("data").get("arrCityName")
        ctno1=data_json.get("data").get("arrCityCode")
        insertdata(sql_aircompany, conn, ctname1, ctno1)
        print(ctname1,ctno1)
        ctname2=data_json.get("data").get("depCityName")
        ctno2= data_json.get("data").get("depCityCode")
        print(ctname2, ctno2)
        insertdata(sql_aircompany,conn,ctname2,ctno2)

def countcity():


    sql = "select count(*) from Nametono "
    # cursor执行sql语句
    cursor=conn.cursor()
    cursor.execute(sql)
    rr = cursor.fetchall()  # 将所有的结果放入rr中
    print(rr[0][0])
    return rr[0][0]

city=['北京','上海','广州','深圳','成都','重庆','厦门','昆明','杭州','西安','武汉','长沙','南京','大连','郑州','青岛','天津','三亚','海口','乌鲁木齐']
if __name__ == "__main__":

    # content=splide_data("北京","2018-06-28","乌鲁木齐")
    # insertallmessage(conn,content)

    #这是获取航班信息




    # count=1
    # a=28
    # while(a!=31):
    #     k3 = "2018-06-"
    #
    #     k3 += str(a)
    #     for ct1 in city:
    #         for ct2 in city:
    #             if (ct2 != ct1):
    #
    #
    #                 print("%s->%s"%(ct1,ct2))
    #                 content=splide_data(ct1,k3,ct2)
    #                 insertallmessage(conn, content)
    #                 print("爬取完网页：",count)
    #                 print()
    #                 count+=1
    #
    #
    #     a += 1
    #     print("%s数据爬完"%k3)
    #
    # print("航班存储完毕")



    # 这里插入机场号和机场名的对照表
    getcitychart()
    sql="insert into apnotoname values(%s,%s)"
    print(sql)
    for ap in dictchart:
        print(dictchart[ap],ap)
        insertdata(sql,conn,dictchart[ap],ap)
    # 这里获取城市号和城市名对照表
    # count = 1
    # a = 28
    # while (a != 31):
    #     k3 = "2018-07-"
    #     if countcity()==20:
    #         break
    #     countcity()
    #     k3 += str(a)
    #     for ct1 in city:
    #         if countcity() == 20:
    #             break
    #         for ct2 in city:
    #             if (ct2 != ct1):
    #                 print("%s->%s" % (ct1, ct2))
    #                 content = splide_data(ct1, k3, ct2)
    #                 getcitynametono(conn,content)
    #                 print("爬取完网页：", count)
    #
    #                 print()
    #                 count += 1
    #                 break
    #
    #     a += 1
    #     print("%s数据爬完" % k3)
    #
    # print("航班存储完毕")




    # print(judgepath("www.baidu.com"))

    # 查询航班
    # conn=linkdba()
    #
    # content=splide_data("重庆","2018-06-26","上海")
    # insertallmessage(conn,content)


    # 1、从数据库中查询
    # sql="INSERT INTO login(user_name,pass_word)"
    # sql = "select * from tb_air_flight;"
    # # cursor执行sql语句
    # cursor.execute(sql)
    # rr = cursor.fetchall()  # 将所有的结果放入rr中
    # print(cursor.rowcount)
    # for row in rr:
    #     print(row)







