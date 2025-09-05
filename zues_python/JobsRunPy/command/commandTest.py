import src.command as command

# import services.analysis_test as analysis_test
# import services.analysis_insert as analysis_insert
# import services.analysis_debug as analysis_debug
from services.subprocess import st as SSSS
from services.subprocess import st111 as TTTTTT


class CommandTest(command.Command):
    taskId = "test"

    def SetRoute(self):
        self.routeList["test_command"] = {
            "min_pnum": 1,
            "max_pnum": 1,
            "loopnum": 10,
            "loopsleepms": 200,
            "crontab": "* * * * * *",
        }
        self.routeList["debug_command"] = {
            "min_pnum": 1,
            "max_pnum": 1,
            "loopnum": 10,
            "loopsleepms": 300,
            "crontab": "* * * * * *",
        }

    def SetSchedule(self):
        self.scheduleList["test_command"] = [
            SSSS,
        ]
        self.scheduleList["debug_command"] = [TTTTTT]
