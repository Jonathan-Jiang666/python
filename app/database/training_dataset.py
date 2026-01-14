from datetime import datetime, date, timedelta
from ..database.ai_emails_dp import AIEmailDataProcess
from ..database.calendar_events_dp import CalenderEventsDataProcess
from ..database.course_schedule_dp import CourseScheduleDataProcess
from ..database.weather_db import WeatherDataProcess
import pandas as pd
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)


class TrainingDatasetProcess:

    def __init__(self, email_proc, calendar_proc, course_proc, weather_proc):
        self.email_proc = email_proc
        self.calendar_proc = calendar_proc
        self.course_proc = course_proc
        self.weather_proc = weather_proc



    def assemble_dataset( self, since_ts: datetime ):
        # 1 get different dataset from different process
        emails  = self.email_proc.get_emails_by_emailtime(since_ts)
        events = self.calendar_proc.get_calender_event_by_time(since_ts)
        courses = self.course_proc.get_course_schedule_by_time(since_ts)
        weather = self.weather_proc.get_weather_data_by_time(since_ts)

        # 2 transfer to DataFrame
        email_df = pd.DataFrame([e.__dict__ for e in emails])
        event_df = pd.DataFrame([e.__dict__ for e in events])
        course_df = pd.DataFrame([e.__dict__ for e in courses])
        weather_df = pd.DataFrame([e.__dict__ for e in weather])

        # create a time scroll (30 mins)
        start_time = since_ts
        end_time = datetime.now()
        time_grid = pd.date_range(start=start_time, end=end_time, freq="30min")
        timeline_df = pd.DataFrame({"timestamp": time_grid})

        # align the data source , use merge_asof
        merged = pd.merge_asof(timeline_df, weather_df, on="timestamp", direction="backward")
        merged = pd.merge_asof(merged, email_df, on="timestamp", direction="backward")
        merged = pd.merge_asof(merged, event_df, on="timestamp", direction="backward")
        merged = pd.merge_asof(merged, course_df, on="timestamp", direction="backward")


        # feature engineering
        # defensive: some columns may be missing depending on upstream data
        is_event_na = merged.get('event_type').isna() if 'event_type' in merged else True
        is_course_na = merged.get('course_id').isna() if 'course_id' in merged else True
        merged["is_free"] = is_event_na & is_course_na

        return merged

    def get_last_processed( self ,table_name):
        with self.engine.connect() as conn:
            result = conn.execute(
                text("select last_timestamp from last_pro")
            )


if __name__ == "__main__":
    assemble = TrainingDatasetProcess(
        email_proc=AIEmailDataProcess(),
        calendar_proc=CalenderEventsDataProcess(),
        course_proc=CourseScheduleDataProcess(),
        weather_proc=WeatherDataProcess(),
    )
    dataset = assemble.assemble_dataset(datetime.now() - timedelta(hours=6))
    logger.info(dataset.head(10))




