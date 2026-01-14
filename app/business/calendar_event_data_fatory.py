from datetime import timedelta
from icalendar import Calendar
from caldav import DAVClient
from typing import List
from ..models_oma.calendar_events_bean import CalendarEvent
from ..database.calendar_events_dp import CalenderEventsDataProcess
from .. import config
import logging

logger = logging.getLogger(__name__)


class CalendarEventDF:

    def __init__(self):
        user = config.ICLOUD_USER
        password = config.ICLOUD_PASSWORD
        if not user or not password:
            logger.error('ICLOUD credentials not configured.')
            self._calendars = []
            return

        client = DAVClient(url="https://caldav.icloud.com", username=user, password=password)
        principal = client.principal()
        self._calendars = principal.calendars()
        logger.info("Loaded %d calendars from iCloud", len(self._calendars))

    def get_calendars(self) -> List:
        return self._calendars

    def original_calendar_data_process(self, calenders: List) -> List[CalendarEvent]:
        calendar_events: List[CalendarEvent] = []
        logger.info("Processing %d calendars", len(calenders))
        for calendar in calenders:
            logger.info("Calendar: %s", getattr(calendar, 'name', 'unknown'))
            try:
                events = calendar.events()
                for event in events:
                    raw = event.data
                    cal = Calendar.from_ical(raw)
                    for component in cal.walk():
                        if component.name == "VEVENT":
                            try:
                                summary = component.get('summary')
                                dtstart = component.get('dtstart').dt
                                dtend = component.get('dtend').dt
                                description = component.get('description')
                                location = component.get('location')
                                uid = component.get('uid')
                                alarm_time = None
                                for sub in getattr(component, 'subcomponents', []):
                                    if getattr(sub, 'name', None) == "VALARM":
                                        trigger = sub.get('TRIGGER')
                                        if trigger is not None:
                                            trig_dt = trigger.dt
                                            if isinstance(trig_dt, timedelta):
                                                alarm_time = dtstart + trig_dt

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
                            except Exception as e:
                                logger.warning("Error parsing event: %s", e)
            except Exception as e:
                logger.error("Error reading calendar: %s", e)
        return calendar_events

    def iteration_CalendarArray_To_Table(self, events: List[CalendarEvent]) -> None:
        ce = CalenderEventsDataProcess()
        for calendar in events:
            ce.insert_calender_Event(calendar)

    def packing_object(self, calendarEvent: CalendarEvent) -> CalendarEvent:
        calendarBean = CalendarEvent(
            user_id=calendarEvent.user_id,
            title=calendarEvent.title,
            description=calendarEvent.description,
            location=calendarEvent.location,
            start_time=calendarEvent.start_time,
            end_time=calendarEvent.end_time,
            remindertime=calendarEvent.remindertime,
            is_all_day=calendarEvent.is_all_day,
            source=calendarEvent.source,
            created_at=calendarEvent.created_at
        )
        return calendarBean
