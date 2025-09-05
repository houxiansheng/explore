from .library.plugins.log import sub_logger
class Command:
    taskId = None  # 任务唯一标记
    desc = None  # 任务描述，适用于异步通知

    def __init__(self):
        self.routeList = sub_logger.plugin_routes
        self.scheduleList = sub_logger.plugin_schedules
        self.SetRoute()
        self.SetSchedule()

    def SetRoute(self):
        return True

    def SetSchedule(self):
        return True

    def getTaskId(self):
        return self.taskId
