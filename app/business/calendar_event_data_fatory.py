# 解析.ics文件有三种方法，一种是 使用ICS库 一种是使用icalendar库，还有就是使用DAVclient
from datetime import timedelta
from icalendar import Calendar
from caldav import DAVClient
from typing import List
from PersonalAIassistant.app.models_oma.calendar_events_bean import CalendarEvent
from PersonalAIassistant.app.database.calendar_events_dp import CalenderEventsDataProcess

class CalendarEventDF:

    def __init__(self):
        # 通过苹果开发官网 拿到授权研发的密码
        client = DAVClient (

            url="https://caldav.icloud.com" ,
            username='77077117@qq.com' ,  # 主 Apple ID油箱
            password='irfj-llak-eqvn-drhk'  # 应用专用密码，可以去 account.apple.com去设置
        )

        # 获取 Principal 对象
        principal = client.principal()
        self._calendars = principal.calendars()
        print("苹果原始云获取的数组数量是",len(self._calendars))

    # Packaging object and return it
    def get_calendars(self):
        return self._calendars



    def original_calendar_data_process(self, calenders: List):
        calendar_events = []  # Difine an array for store the calenderEvent
        print("第一时间获取到的数组数量是",len(calenders))
        # 遍历所有事件
        for calendar in calenders:
            print(f"📅 Calendar: {calendar.name}")
            try:
                # 获取事件列表
                events = calendar.events()
                #输出事件数量
                print(f"📌 Found {len(events)} events.")
                # raw = events.data
                # circulate the events and use try...except method to capture exception
                count = 0
                for event in events:
                    count += 1
                    raw = event.data  # 原始iCalendar数据
                    cal = Calendar.from_ical(raw)
                    count2 = 0
                    count3 = 0
                    for component in cal.walk():  #
                        count2 += 1
                        if component.name == "VEVENT":
                            count3 += 1
                            summary = component.get('summary')
                            print("新方法获取的标题是", component.get('summary'))  # this is title of database's table
                            dtstart = component.get ('dtstart').dt
                            print("新方法获取到的开始时间是：", dtstart)  # this is start time
                            dtend = component.get ('dtend').dt
                            print("新方法获取到的结束时间是：",dtend) #this is end time
                            description = component.get ('description')
                            print("事件描述是：",description) # this is description
                            location = component.get ('location')
                            print("新方法获取到的事件地点是",location) # this is location of event
                            uid = component.get ('uid')
                            for sub in component.subcomponents:
                                if sub.name == "VALARM":
                                    # print("valarm = ",sub.name)
                                    valarm_description = sub.get ('description')  # 原文件中的子提醒信息
                                    print("新方法获取到的子提醒信息是：", valarm_description)
                                    trigger_time = sub.get ('TRIGGER').dt  # TRIGGER:-PT15M ,原文件中的提醒触发时间，需要格式化解析
                                    print("新方法获取到的提醒触发时间是：", trigger_time)
                                    if trigger_time is not None:
                                        if isinstance (trigger_time , timedelta):
                                            alarm_time = dtstart + trigger_time
                                            print("事件提醒时间是",alarm_time)
                            # Encapsulation Object
                            ce = CalendarEvent(
                                title=summary,
                                description=description,
                                location=location,
                                start_time=dtstart,
                                end_time=dtend,
                                remindertime=alarm_time,
                                is_all_day=1,
                                source="Apple_iCloud"
                            )
                            calendar_events.append(ce)
                            print("当前解析的数据事件数量是：",len(calendar_events))
                            print("第三层循环的数据事件数量是：", count2)
                            print("第四层循环的数据事件数量是：", count3)
                try:
                    #if count == 1:
                        #pass
                    print(f"第{count}次循环，当前事件数量是：", len(calendar_events))

                except Exception as e:
                    print ("⚠️ Error reading event:" , e)
            except Exception as e:
                print ("Error reading calender" , e)
        return calendar_events    # Return the array



    def iteration_CalendarArray_To_Table ( self , events ):
        ce = CalenderEventsDataProcess()

        for calendar in events:
            ce.insert_calender_Event(calendar)



    def packing_object(self, calendarEvent: CalendarEvent):
        calendarBean = CalendarEvent(
            user_id= calendarEvent.user_id,
            title=calendarEvent.title,
            description = calendarEvent.description,
            location=calendarEvent.location,
            start_time=calendarEvent.start_time,
            end_time=calendarEvent.end_time,
            remindertime=calendarEvent.remindertime,
            is_all_day=calendarEvent.is_all_day,
            source=calendarEvent.source,
            created_at=calendarEvent.created_at
        )
        return calendarBean
