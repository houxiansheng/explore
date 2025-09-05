import logging
import multiprocessing
import os
from logging.handlers import TimedRotatingFileHandler
from typing import Dict

from ..share.share import global_log_queue
from ..singleton import Singleton


class TagFilter(logging.Filter):
    def __init__(self, name, tag):
        self.tag = tag
        super().__init__(name)

    def filter(self, record):
        return getattr(record, 'tag', None) == str(self.tag)

class MillisecondFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        from datetime import datetime
        ct = datetime.fromtimestamp(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
            return s[:-3]  # 保留毫秒（去掉微秒的后三位）
        else:
            return super().formatTime(record, datefmt)
class Logger(Singleton):
    _logger: Dict[str, logging.Logger] = {}
    _config = {}
    _logqueue = {}
    taskId = ""

    # 设置配置文件
    def setConfig(self, config: list):
        if isinstance(config, list):
            for item in config:
                tag = item.get("tag")
                if tag:
                    self._config[tag] = item

        self.init_logger()
        return global_log_queue

    def create_log_dir(self, filename):
        log_dir = os.path.dirname(filename)
        task_file_path = os.path.join(log_dir, self.taskId)
        file_name = os.path.basename(filename)

        # 如果目录不存在，则创建
        if task_file_path and not os.path.exists(task_file_path):
            os.makedirs(task_file_path, exist_ok=True)
        return os.path.join(task_file_path, file_name)

    def init_logger(self):
        # init queue
        queue = multiprocessing.Queue(maxsize=5000)
        for tag, item in self._config.items():
            handler = TimedRotatingFileHandler(
                filename=self.create_log_dir(item['filename']),
                when='H',
                interval=1,
                backupCount=item.get('backupCount', 48)
            )
            formatter = MillisecondFormatter(item['format'], datefmt='%Y-%m-%d %H:%M:%S.%f')
            handler.setFormatter(formatter)
            handler.addFilter(TagFilter('myfilter', tag))
            global_log_queue[tag] = {'queue': queue, 'handler': handler}

            logger = logging.getLogger(tag)
            logger.setLevel(item['level'])
            queue_handler = logging.handlers.QueueHandler(global_log_queue[tag]['queue'])
            logger.addHandler(queue_handler)
            self._logger[tag] = logger

    def get_logger(self, tag):
        return self._logger.get(tag, None)

    def getGlobalQueue(self):
        return global_log_queue

    def log(self, message: str = None, tag: str = None, level=logging.INFO):
        llog = self.get_logger(tag)
        if not llog:
            return

        # 支持字符串级别如 "INFO"
        if isinstance(level, str):
            level = logging.getLevelName(level.upper())

        llog.log(level, message, extra={'tag': tag})
