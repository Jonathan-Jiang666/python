import unittest
import time
import os
from datetime import datetime
import logging
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.memory import MemoryJobStore
from PersonalAIassistant.app.database.ai_emails_dp import AIEmailDataProcess
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
        self.scheduler = BackgroundScheduler(jobstores=jobstores,executors=executors,job_defaults=job_defaults)


        # Log configuration
        logging.basicConfig(filename=logfile,level=logging.INFO,format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger(__name__)

    def job1( self ):
        """Task1: print time """
        try:
            msg = f"[{datetime.now()}] {self.name} -execute job1"
            print(msg)
            self.logger.info(msg)
        except Exception as e:
            self.logger.error(f"job1 error:{e}")

    def job2( self ):
        """Task2: mock business logic"""
        try:
            msg = f"[{datetime.now()}]{self.name} -execute job2"
            print(msg)
            self.logger.info(msg)
        except Exception as e:
            self.logger.error(f"job2 error:{e}")

    def job_get_emails( self ):
        """Task 3: Fetch Gmail emails and save to database"""
        try:
            msg = f"[{datetime.now ()}]{self.name} -execute job3"
            print(msg)
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
            print("job_get_emails: last_run_time= "+str(self.last_run_time))

            credentials_path = os.path.abspath("credentials.json")
            if not os.path.exists(credentials_path):
                self.logger.info(f"credentials file not found:{credentials_path}")
                return
            token_path = os.path.abspath("token.pickle")
            # now safely run your processor
            processor = AIEmailDataProcess(
                credentials_file=credentials_path ,
                token_file=token_path
            )
            processor.run(days_back=days_back)
            processor.session.close()
            self.logger.info(f"✅ Gmail data fetching completed (days_back={days_back}).")

        except Exception as e:
            self.logger.error(f"❌ job_get_emails error: {e}")


    def start(self):
        """Start the scheduler and add the task"""

        if not self.scheduler.running:
            # Every 5 second execute one time job1
            self.scheduler.add_job(self.job1,'interval', seconds=5,id="job1")

            # Every day 12:00 execute the job2
            # In the job2 to execute the CalenderEventData process
            self.scheduler.add_job(self.job2, 'cron', hour=19, minute=8, id="job2")
            self.scheduler.start()
            self.logger.info("The schedulter task has been started")

            # Every day 24:00 execute the job3
            # In the Job3 to execute the get_email from google platform
            self.scheduler.add_job(self.job_get_emails, 'cron', hour=19, minute=8, id="job3")
            #self.scheduler.start()
            self.logger.info("The Get email task has been started")
        else:
            self.logger.info ("Scheduler is already running — skipped start()")


    def stop( self ):
        """Stop scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.logger.info("Scheduler has been stopped")