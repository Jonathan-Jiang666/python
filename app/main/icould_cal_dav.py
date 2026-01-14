from datetime import timedelta
from icalendar import Calendar
from caldav import DAVClient
import logging
from .. import config

def fetch_icloud_calendars():
logger = logging.getLogger(__name__)


def fetch_icloud_calendars():
    user = config.ICLOUD_USER
    password = config.ICLOUD_PASSWORD
    if not user or not password:
        logger.error('iCloud credentials not configured (ICLOUD_USER/ICLOUD_PASSWORD).')
        return []

    client = DAVClient(url="https://caldav.icloud.com", username=user, password=password)
    principal = client.principal()
    calendars = principal.calendars()
    return calendars


def parse_calendar_events(calendars):
    results = []
    for calendar in calendars:
        logger.info("Calendar: %s", getattr(calendar, 'name', 'unknown'))
        try:
            events = calendar.events()
            for event in events:
                raw = event.data
                cal = Calendar.from_ical(raw)
                for component in cal.walk():
                    if component.name == 'VEVENT':
                        try:
                            summary = component.get('summary')
                            dtstart = component.get('dtstart').dt
                            dtend = component.get('dtend').dt
                            description = component.get('description')
                            location = component.get('location')
                            uid = component.get('uid')
                            alarm_time = None
                            for sub in getattr(component, 'subcomponents', []):
                                if getattr(sub, 'name', None) == 'VALARM':
                                    trig = sub.get('TRIGGER')
                                    if trig is not None:
                                        trig_dt = trig.dt
                                        if isinstance(trig_dt, timedelta):
                                            alarm_time = dtstart + trig_dt
                            results.append({
                                'summary': summary,
                                'start': dtstart,
                                'end': dtend,
                                'description': description,
                                'location': location,
                                'uid': uid,
                                'alarm_time': alarm_time,
                            })
                        except Exception as e:
                            logger.warning("Failed to parse VEVENT: %s", e)
        except Exception as e:
            logger.error("Error reading calendar %s: %s", getattr(calendar, 'name', ''), e)
    return results


if __name__ == '__main__':
    cals = fetch_icloud_calendars()
    events = parse_calendar_events(cals)
    logger.info("Parsed %d events from iCloud", len(events))






