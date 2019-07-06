# from wxpy import *
# KEY = '2de1c72204a048679add5cb3b19c525b'
#
# bot = Bot(cache_path=True)
#
# my_friend = ensure_one(bot.search('姚小倩'))
#
# tuling = Tuling(api_key=KEY)
#
# @bot.register(my_friend)  # 使用图灵机器人自动与指定好友聊天
# def reply_my_friend(msg):
#     tuling.do_reply(msg)
# embed()

def choosedoth(str):
    if("@王二狗" in str):
        # print("捕获到了正确的句子")
        s=str.split()
        for i in s:
            print(i,end=" ")
        if(len(s)==3):
            if s[1]=="天气预报":
                print("查询%s天气信息"%s[2])
                return

            else:
                print("功能格式输入错误1")
                return
        else:
            print("功能格式输入错误2")
            return

    else:
        print("没捕获到")

if __name__ == '__main__':
    str="@王二狗        天气预报  北京"
    str1="你是    真的秀"
    s2="@王二狗 你是            傻瓜吗"
    s3="@王二狗 你是 傻瓜"
    choosedoth(str)
    choosedoth(str1)
    choosedoth(s2)
    choosedoth(s3)