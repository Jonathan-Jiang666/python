import time
import os
from datetime import datetime
import logging
from zoneinfo import ZoneInfo
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from ..database.ai_emails_dp import AIEmailDataProcess
from .. import config

# module logger
logger = logging.getLogger(__name__)
class MyTastToList:

    def __init__(self, name="Default Mission", logfile="task.log"):
        self.name = name
        self.last_run_time = None

        #APScheduler configuration: use the memory to store and threadPool
        jobstores = {
            'default':MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(10) # Support multiple threads for parallel processing
        }
        job_defaults ={
            'coalesce': False, # Do not merge missed tasks
            'max_instances': 3 # The same task can run a maximum of 3 instances simultaneously  同一任务最多同时运行 3 个实例
        }
        # Use configured timezone
        try:
            tz = ZoneInfo(config.TIMEZONE)
        except Exception as e:
            tz = None
            logger.exception("Failed to load timezone from config.TIMEZONE")
        self.scheduler = BackgroundScheduler(jobstores=jobstores,executors=executors,job_defaults=job_defaults, timezone=tz)

        # instance logger
        self.logger = logger

    def job1( self ):
        """Task1: print time """
        try:
            msg = f"[{datetime.now()}] {self.name} -execute job1"
            self.logger.info(msg)
        except Exception as e:
            self.logger.exception("job1 error")

    def job2( self ):
        """Task2: mock business logic"""
        try:
            msg = f"[{datetime.now()}]{self.name} -execute job2"
            self.logger.info(msg)
        except Exception as e:
            self.logger.exception("job2 error")

    def job_get_emails( self ):
        """Task 3: Fetch Gmail emails and save to database"""
        try:
            msg = f"[{datetime.now ()}]{self.name} -execute job3"
            self.logger.info(msg)
            self.logger.info("📧 Starting scheduled Gmail data fetching job...")

            #Computer how many days since last run(fallback = 1)
            days_back =1
            #if hasattr(self,"last_run_time"):
            if self.last_run_time is not None:
                diff = datetime.now() - self.last_run_time
                days_back = max(diff.days, 1)

            # update last_run_time to current time
            self.last_run_time = datetime.now()
            self.logger.debug("job_get_emails: last_run_time=%s", str(self.last_run_time))

            credentials_path = os.path.abspath(getattr(config, 'GOOGLE_CREDENTIALS_PATH', config.resolve_data_path('credentials.json')))
            if not os.path.exists(credentials_path):
                self.logger.info(f"credentials file not found:{credentials_path}")
                return
            token_path = os.path.abspath(getattr(config, 'GOOGLE_TOKEN_PATH', config.resolve_data_path('token.pickle')))
            # now safely run your processor
            processor = AIEmailDataProcess(
                credentials_file=credentials_path ,
                token_file=token_path
            )
            try:
                processor.run(days_back=days_back)
            finally:
                try:
                    processor.session.close()
                except Exception as e:
                    self.logger.exception("Failed closing processor session")
            self.logger.info(f"✅ Gmail data fetching completed (days_back={days_back}).")

        except Exception as e:
            self.logger.error(f"❌ job_get_emails error: {e}")


    def start(self):
        """Start the scheduler and add the task"""

        if not self.scheduler.running:
            # add jobs then start once
            self.scheduler.add_job(self.job1,'interval', seconds=5,id="job1")
            self.scheduler.add_job(self.job2, 'cron', hour=19, minute=8, id="job2")
            self.scheduler.add_job(self.job_get_emails, 'cron', hour=19, minute=8, id="job3")
            self.scheduler.start()
            self.logger.info("Scheduler started with jobs: job1, job2, job3")
        else:
            self.logger.info ("Scheduler is already running — skipped start()")


    def stop( self ):
        """Stop scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("Scheduler has been stopped")