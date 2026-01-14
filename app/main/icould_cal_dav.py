#解析.ics文件有三种方法，一种是 使用ICS库 一种是使用icalendar库，还有就是使用DAVclient
from datetime import timedelta
from icalendar import Calendar
from caldav import DAVClient


#Through Apple offical website to get the authorised password
client = DAVClient(

    url="https://caldav.icloud.com",
    username='77077117@qq.com',  # 主 Apple ID油箱
    password='irfj-llak-eqvn-drhk'  # 应用专用密码，可以去 account.apple.com去设置
)



#Get the  Principal object
principal = client.principal()
calendars = principal.calendars()


#Iterate all events and then package it as a method to be called in other methods
for calendar in calendars:
    print(f"📅 Calendar: {calendar.name}")
    try:
        # Get the event list
        events = calendar.events()
        # output the event information
       # print(f"📌 Found {len(events)} events.")
        # raw = events.data
        # circulate the events and use try...except method to capture exception
        count = 0
        for event in events:
            count += 1
            raw = event.data  # Original iCalendar data
            cal = Calendar.from_ical(raw)
            for component in cal.walk(): #
                if component.name == "VEVENT":
                    summary = component.get('summary')
                    #print("新方法获取的标题是", component.get('summary'))
                    dtstart = component.get('dtstart').dt
                    #print("新方法获取到的开始时间是：", dtstart)
                    dtend = component.get('dtend').dt
                    description = component.get('description')
                    #print("事件描述是：",description)
                    location = component.get('location')
                    uid = component.get('uid')
                    for sub in component.subcomponents:
                        if sub.name =="VALARM":
                           #print("valarm = ",sub.name)
                            valarm_description = sub.get('description') #The original files sub_remind informations
                           # print("新方法获取到的子提醒信息是：", valarm_description)
                            trigger_time = sub.get('TRIGGER').dt  #TRIGGER:-PT15M ,the original remind trigger time , needs to format and analysis
                           # print("新方法获取到的提醒触发时间是：", trigger_time)
                            if trigger_time is not None:
                                if isinstance(trigger_time,timedelta):
                                    alarm_time  = dtstart + trigger_time
                                    #print("事件提醒时间是",alarm_time)
        try:
            if count == 1:
                print(f"第{count}次循环，当前事件信息是：", event.data)
        #  summary = event.data.get('SUMMARY')  #get the title of event
        #  print("标题是",summary)
        #    date_start = event.gen('DTSTAR') # get the event's startime
        #    date_end = event.get('DTEND') # get the event's endtime
        #    location = event.get('LOCATION') # get the event's happend location
        ##   description = event.get('DESCRIPTION') # get the event's detail information

        # disposing the situation of the field is 'bytes'
        #   if isinstance(location,bytes):
        #       location = location.decode('UTF-8')

        #   if isinstance(description, bytes):
        #       description = description.decode('UTF-8')

        #   print('开始时间',date_start)
        #   print('结束时间',date_end)
        #   print('地点',location)
        #   print('事件描述为',description)

        # print("📄 Event details:\n", event.data)

        except Exception as e:
               print("⚠️ Error reading event:", e)
    except Exception as e:
         print("Error reading calender", e)



