import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#  打印当前工作目录
logger.info("当前工作目录: %s", os.getcwd())

# 打印 Python 搜索路径
logger.info("Python sys.path:")
for p in sys.path:
    logger.info("  %s", p)

# 检查 app 目录是否存在 __init__.py
def check_init_file(path):
    init_file = os.path.join(path, "__init__.py")
    exists = os.path.isfile(init_file)
    logger.info("检查 %s/__init__.py: %s", path, '✅ 存在' if exists else '❌ 不存在')
    return exists

app_path = os.path.join(os.getcwd(), "app")
database_path = os.path.join(app_path, "database")
models_path = os.path.join(app_path, "models_oma")

logger.info("\n检查包结构:")
check_init_file(app_path)
check_init_file(database_path)
check_init_file(models_path)

# 测试导入
try:
    from app.database.db import Base
    logger.info("\n导入 Base 成功 ✅")
except ModuleNotFoundError as e:
    logger.exception("导入 Base 失败 ❌")