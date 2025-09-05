import asyncio

from .library.plugins.log.queue_logger import LogQueue
from .library.run import crontab as crontab
from .library.run.process import ProcessManager
from .library.share import share as shareVar
from ..manager import Manager


class Master:
    def setCommand(self, Command):
        shareVar.setSchedule(Command.taskId, Command.routeList, Command.scheduleList)

    def setConfPath(self, confPath):
        shareVar.setConfigDir(confPath)

    async def exec(self, taskId, schedule=None):
        exist = shareVar.taskExsting(taskId, schedule)
        if not exist:
            print("任务信息不存在")
            return False
        # 初始化日志信息
        manger = Manager()
        manger.taskId = taskId
        manger.setConfPath(shareVar.getConfigDir())
        global_log_queue = manger.getInstance("logger").getGlobalQueue()
        shareVar.setLogQueue(global_log_queue)
        LogQueue().start_listener(global_log_queue)  # 启动日志监听
        pro = ProcessManager()
        c1 = asyncio.create_task(crontab.crontab().run(taskId, schedule))  # 定时产生任务
        c2 = asyncio.create_task(pro.join())
        c3 = asyncio.create_task(pro.run(taskId, schedule))  # 运行任务，fork子进程
        c4 = asyncio.create_task(pro.exceptJoins())
        await asyncio.gather(c1, c2, c3, c4)

    def run(self, taskId, schedule=None):
        exist = shareVar.taskExsting(taskId, schedule)
        if not exist:
            print("任务信息不存在")
            return False
        asyncio.run(self.exec(taskId, schedule))
