from multiprocessing import Queue
from logging import FileHandler
from logging.handlers import QueueListener


# logqueue = QueueListener(
#     Queue(maxsize=1000),
#     FileHandler("/data1/apache2/htdocs/hxb-ide_zues_python/out.log"),
#     respect_handler_level=True,
# )
# QueueListener(
#     Queue(maxsize=1000),
#     FileHandler("/data1/apache2/htdocs/hxb-ide_zues_python/out.log"),
#     respect_handler_level=True,
# ).start()


class sub_logger:
    def __init__(self) -> None:
        pass

    def run(self):
        print("sub_logge123123r")
        # logqueue.start()
        pass


plugin_routes = {
    # "sub_logger": {
    #     "min_pnum": 1,
    #     "max_pnum": 1,
    #     "loopnum": 1000,
    #     "loopsleepms": 1000,
    #     "crontab": "* * * * * *",
    # },
}
plugin_schedules = {
    # "sub_logger": [
    #     sub_logger,
    # ],
}
