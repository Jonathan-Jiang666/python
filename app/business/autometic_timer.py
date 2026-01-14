import time
from .my_task_list import MyTastToList
from .. import config

# ensure logging is initialized
config.init_logging()

if __name__ == "__main__":
    #task = MyTask("多任务测试")
    task = MyTastToList("多任务测试")
    task.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        task.stop()