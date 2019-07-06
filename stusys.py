stulist=[]
# 打印函数，打印学生情况
def printstu():
    for s in stulist:
        print("学号：{0}，姓名：{1}，性别：{2}".format(s['no'],s['name'],s['sex']))
def addstu(dictx):
    flag=1
    if not stulist:
        stulist.append(dictx)
    else:

        for word in stulist:
            if word['no']==dictx.get('no'):
                print("学号重复，该学生添加失败")
                flag=0
                break
        if flag==1:
            stulist.append(dictx)
            print("添加成功")
    return flag
def deletestu(no):
    flag=0
    print("删除学生学号为：",no)
    if not stulist:
        print("学生信息表为空，无法删除信息")
        return -1
    else:
        count=0
        for s in stulist:
            # print(s.get('no'),type(s.get('no')))

            if s.get('no')==no:
                flag=1
                break
            count+=1
        if flag==0:
            print("该学生不存在，不需要删除")
            return 0
        if flag==1:
            print("学生删除成功")
            del stulist[count]
            return 1
def fixstu(no):
    flag = 0
    print("修改学生学号为：", no)
    if not stulist:
        print("学生信息表为空，无法修改信息")
        return -1
    else:
        count = 0
        for s in stulist:
            print(s.get('no'), type(s.get('no')))

            if s.get('no') == no:
                flag = 1
                break
            count += 1
        if flag == 0:
            print("该学生不存在，无法修改")
            return 0
        if flag == 1:
            s1=input("修改的学生学号为：")
            s2=input("修改的学生姓名为：")
            s3=input("修改的学生性别为：")
            stulist[count]['no']=s1
            stulist[count]['name'] = s2
            stulist[count]['sex'] = s3
            return 1


def menu():
    print("0:查看学生表")
    print("1:添加一位学生")
    print("2：删除一位学生")
    print("3:修改一位学生")
    print("3:退出本程序")
def test():
    a1={'no':"123",'name':"ace",'sex':'男'}
    a2={'no':"125",'name':"Alice",'sex':'女'}
    a3= {'no': "124", 'name': "joden", 'sex': '男'}
    addstu(a1)
    addstu(a2)
    addstu(a3)

    menu()

    # printstu()
    # deletestu('124')
    # printstu()
    op=int(input("请选择操作指令(如1):"))
    while(op!=4):

        if op==1:
            s1=input("请输入学生学号")
            s2=input("请输入学生姓名")
            s3=input("请输入学生性别（男：male；女：female）")
            dictx={}

            key='no'
            dictx[key]=s1
            key='name'
            dictx[key]=s2
            key='sex'
            dictx[key]=s3
            addstu(dictx)
        if op==2:
            num=str(input("请输入删除的学生的学号"))

            deletestu(num)
        if op==3:
            num=str(input("请输入修改的学生的学号"))

            fixstu(num)
        if op==0:
            printstu()
        op = int(input("请选择操作指令(如1):"))
    print("成功退出本程序，感谢使用")


# print(input("3+4"))
test()