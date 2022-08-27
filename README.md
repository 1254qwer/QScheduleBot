# QScheduleBot——一个基于go-cqhttp的QQ群内课表提醒机器人
## 灵感来源

[StageGuard/SuperCourseTimetableBot: 基于 mirai-console 的 超级课表上课提醒QQ机器人 插件 (github.com)](https://github.com/StageGuard/SuperCourseTimetableBot)

## 环境依赖

`Python 3.6+`
依赖库（`pip install`）：`requests`
[Mrs4s/go-cqhttp: cqhttp的golang实现，轻量、原生跨平台. (github.com)](https://github.com/Mrs4s/go-cqhttp)
一个QQ号
手机端：[WakeUp课程表](https://www.coolapk.com/apk/com.suda.yzune.wakeupschedule)（导出课表文件用）

## 食用方法

1. 参照[go-cqhttp 文档](https://docs.go-cqhttp.org/guide/quick_start.html)部署go-cqhttp
2. 使用[WakeUp课程表](https://www.coolapk.com/apk/com.suda.yzune.wakeupschedule)，正常导入（右上第二个按钮）课表，导出（右上第三个按钮）为备份文件
3. 将备份文件存入schedule目录
4. 参照下方示例填写config.json
5. Enjoy it！

## 配置文件（config.json）示例

````json
{
    //直接复制配置文件时请删除所有注释，否则程序无法运行
    "qqun": "549359625", //发消息的群号（即发到哪个群）
    "startday": "2022-08-22", // 本学期开学日，计算周数用
    "timetable": ["07:30","09:35","13:30","15:35","18:30"],  // 课前提醒时间，目前只写了第一个时间对应的程序逻辑（即早八提醒）
    //不同成员的课表
    "schedules": [
        {
            "name": "计科1班", // 班级名称
            "file": "计科1.wakeup_schedule", // 课表文件名, 在schedule目录下
            "qid": ["1101731926","1584884350"] // 群内该班级成员QQ号
        },
        {
            "name": "软工1班",
            "file": "软工1.wakeup_schedule",
            "qid": ["327089247"]
        }
    ]
}
````

## 已实现功能&TODO

- [x] 早八提醒
- [x] 多课表
- [x] 自定义提醒时间
- [x] 自动@相关人员
- [ ] 课前提醒
- [ ] 更多个性化自定义

## 致谢

[YZune/WakeupSchedule_Kotlin: Wakeup课程表Kotlin重构版 (github.com)](https://github.com/YZune/WakeupSchedule_Kotlin)

[Mrs4s/go-cqhttp: cqhttp的golang实现，轻量、原生跨平台. (github.com)](https://github.com/Mrs4s/go-cqhttp)

[StageGuard/SuperCourseTimetableBot: 基于 mirai-console 的 超级课表上课提醒QQ机器人 插件 (github.com)](https://github.com/StageGuard/SuperCourseTimetableBot)

[河地大信工科协 (hguxgkx.com)](http://hguxgkx.com/)