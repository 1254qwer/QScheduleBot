import json
import os
import datetime
import time
import requests

def readSchedule(name):
    """读取课表"""
    with open("schedule/" + name,encoding="utf-8") as f:
        a = f.readlines()
        times = json.loads(a[1].replace("\n",""))
        # print(times)
        names = json.loads(a[3].replace("\n",""))
        courses = json.loads(a[4].replace("\n","").replace("*",""))
        for i in courses:
            del i["endTime"]
            del i["startTime"] 
            for j in names:
                if j["id"] == i["id"]:
                    i["courseName"] = j["courseName"]
                    i["credit"] = j["credit"]
                    break
            for j in range(len(times)):
                if i["startNode"] == times[j]["node"]:
                    # print("yes")
                    i["startTime"] = times[j]["startTime"]
                    i["endTime"] = times[j+i["step"]-1]["endTime"]
                    break
            del i["level"]
            del i["ownTime"]
            del i["tableId"]
            del i["type"]
            del i["id"]
        courses = sorted(courses, key=lambda x: (x["day"], x["startNode"], x["startWeek"]))
        # print(courses)
        # print(json.dumps(courses, ensure_ascii=False, indent=4))
        return courses

def readConfig():
    '''读取配置文件'''
    configs = json.load(open("config.json",encoding="utf-8"))
    return configs["qqun"],configs["startday"],configs["timetable"],configs["schedules"]

def num_to_char(num):
    """星期数字转中文"""
    num=str(num)
    new_str=""
    num_dict={"1":u"一","2":u"二","3":u"三","4":u"四","5":u"五","6":u"六","7":u"日"}
    listnum=list(num)
    # print(listnum)
    shu=[]
    for i in listnum:
        # print(num_dict[i])
        shu.append(num_dict[i])
    new_str="".join(shu)
    # print(new_str)
    return new_str

def sendMessage(big_info,startday,timetable,qqun):
    '''生成&发送消息'''
    # 每60s执行一次
    while(True):
        today = datetime.datetime.now()
        # 计算时间差
        delta = today - datetime.datetime.strptime(startday, "%Y-%m-%d")
        nowweek = (delta.days) // 7 + 1
        nowtime = datetime.datetime.strftime(today, "%H:%M")
        for i in timetable:
            if i == nowtime:
                if nowtime == timetable[0]:
                    flag = 0
                    text8 = "早安，早八人！\n"
                    text9 = "早安！\n"
                    text = "今天是" + datetime.datetime.strftime(today, "%Y年%m月%d日") + "，第" + str(nowweek) + "周周" + num_to_char(datetime.datetime.strftime(today, "%w")) + "\n\n"
                    for k in big_info:
                        hasClass = 0
                        atname = ""
                        classtext = ""
                        for j in k["qid"]:
                            atname += "[CQ:at,qq=" + j + "]"
                        for j in k["courses"]:
                            if (j["startWeek"] <= nowweek <= j["endWeek"]) & (j["day"] == int(datetime.datetime.strftime(today, "%w"))):
                                hasClass += 1
                                if j["startNode"] == 1:
                                    flag = 1
                                    text = text8 + text
                                classtext += j["startTime"] + "-" + j["endTime"] + " " + j["courseName"] + " " + j["room"] + " " + j["teacher"] + "\n"
                        text2 = "今日" + k["name"] + "（" + atname + "）共" + str(hasClass) + "节课，课表如下：\n"
                        text0 = "今日" + k["name"] + "（" + atname + "）无课\n"
                        if flag == 0:
                            text = text9 + text
                        if hasClass > 0:
                            text += text2 + classtext + "\n"
                        elif hasClass == 0:
                            text += text0 + "\n"
                            text += "注：由于英语和体育课的特殊性，仅上课时间相同，上课位置及教师请自行确认" # hgu特殊
                    url = "http://localhost:5700/send_group_msg"
                    content = {
                        "group_id": qqun,
                        "message": text,
                        "auto_escape": "false"
                    }
                    b = requests.post(url=url, data=content).text
        time.sleep(10)

def main():
    big_info = []
    qqun,startday,timetable,schedules = readConfig()
    for i in schedules:
        makeinfo = {
            "name": i["name"],
            "qid": i["qid"],
            "courses": readSchedule(i["file"])
        }
        big_info.append(makeinfo)
    sendMessage(big_info,startday,timetable,qqun)

if __name__ == "__main__":
    main()

# 以下为调试接口
def test():
    '''测试函数，直接修改today里的日期即可模拟该时间，消息会发送在终端里'''
    today = datetime.datetime.strptime("2022-08-26 07:30", "%Y-%m-%d %H:%M")
    big_info = []
    startday,timetable,schedules = readConfig()
    for i in schedules:
        makeinfo = {
            "name": i["name"],
            "qid": i["qid"],
            "courses": readSchedule(i["file"])
        }
        big_info.append(makeinfo)
    # 计算时间差
    delta = today - datetime.datetime.strptime(startday, "%Y-%m-%d")
    nowweek = (delta.days) // 7 + 1
    nowtime = datetime.datetime.strftime(today, "%H:%M")
    if nowtime == timetable[0]:
        flag = 0
        text8 = "早安，早八人！\n"
        text9 = "早安！\n"
        text = "今天是" + datetime.datetime.strftime(today, "%Y年%m月%d日") + "，第" + str(nowweek) + "周周" + num_to_char(datetime.datetime.strftime(today, "%w")) + "\n\n"
        for i in big_info:
            hasClass = 0
            atname = ""
            classtext = ""
            for j in i["qid"]:
                atname += "[CQ:at,qq=" + j + "]"
            for j in i["courses"]:
                if (j["startWeek"] <= nowweek <= j["endWeek"]) & (j["day"] == int(datetime.datetime.strftime(today, "%w"))):
                    hasClass += 1
                    if j["startNode"] == 1:
                        flag = 1
                        text = text8 + text
                    classtext += j["startTime"] + "-" + j["endTime"] + " " + j["courseName"] + " " + j["room"] + " " + j["teacher"] + "\n"
            text2 = "今日" + i["name"] + "（" + atname + "）共" + str(hasClass) + "节课，课表如下：\n"
            text0 = "今日" + i["name"] + "（" + atname + "）无课\n"
            if flag == 0:
                text = text9 + text
            if hasClass > 0:
                text += text2 + classtext + "\n"
            elif hasClass == 0:
                text += text0 + "\n"
        print(text)
def testmessage():
    '''测试消息是否可以正常发送'''
    url = "http://localhost:5700/send_group_msg"
    content = {
        "group_id": "549359625", # 你的群号
        "message": "测试", # 消息内容
        "auto_escape": "false" # 不用动
    }
    b = requests.post(url=url, data=content).text
    print(b)
# test()
# testmessage()