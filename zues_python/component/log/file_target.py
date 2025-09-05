from component.manager import Singleton
import time
import subprocess
import os
import random
import shutil
from datetime import datetime


class FileTarget(Singleton):
    def __init__(self):
        super().__init__()
        self.data = "Component1 Data"
        self.tags = []
        self.levels = ["Error", "Info", "Warning", "Trace"]
        self.enable = True
        self.delimiter = "_"
        self.postFix = "%Y%m%d"
        self.commonPrefix = ""
        self.filePath = ""  # 通常你会在这里设置一个具体的日志存储路径
        self.extension = ".log"
        self.tag2filename = (
            {}
        )  # 注意：Lua中是tag2finename，这里我假设是拼写错误并更正为tag2filename
        self.maxSize = 2  # 单位G
        self.autoCut = True
        self.randNum = 1000
        self.startCache = False

    def _check_file_size(self, fileName, name):
        if random.randint(1, self.randNum) == 1:
            result = subprocess.run(
                ["ls", "-l", fileName], capture_output=True, text=True
            )
            if result.returncode != 0:
                print(f"Error executing command: {result.stderr}")
                return False

            size_str = result.stdout.split("\n")[0].split()[4]
            size_bytes = int(size_str)

            if size_bytes >= self.maxSize * 1024 * 1024 * 1024:
                # 构建新文件名
                new_file_name = os.path.join(
                    self.filePath,
                    self.commonPrefix
                    + self.delimiter
                    + name
                    + self.delimiter
                    + datetime.now().strftime("%Y%m%d%H%M")
                    + self.extension,
                )

                # 重命名文件
                shutil.move(fileName, new_file_name)

                return True

        return False

    def _file_name(self, tag):
        # 获取或设置文件名
        name = self.tag2filename.get(tag, tag)  # 使用get来避免KeyError
        now = datetime.now()
        file_name = os.path.join(
            self.filePath,
            f"{self.commonPrefix}{self.delimiter}{name}{self.delimiter}{now.strftime(self.postFix)}{self.extension}",
        )
        # 注意：这里我们实际上没有使用format变量，因为它与file_name的构造方式相同但缺少时间部分的具体值

        # 检查文件大小（如果启用了自动切割且当前worker_id为1）
        cuted = False
        if self.autoCut and self.worker_id == 1:
            cuted = self._check_file_size(file_name, name)

        # 注意：原始Lua代码返回了format和fileName，但format在Python版本中似乎没有实际用途
        # 因此，我们只返回fileName和cuted
        return file_name, cuted

    def _format_date(timestamp):
        # 在Python中，timestamp是一个浮点数，表示从epoch（1970年1月1日）以来的秒数
        # 注意：如果timestamp是毫秒，则需要先除以1000
        # 这里我们假设timestamp已经是秒
        formatted_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")
        return formatted_date

    def _export(self, messages):
        # 使用字典来存储按标签组织的消息
        _messages = {}
        for message in messages:
            tag = message["tag"]
            text = self._format_message(message)  # 假设这个方法已经定义
            if tag in _messages:
                _messages[tag] += text + "\n"
            else:
                _messages[tag] = text + "\n"

        # 处理每个标签对应的文件写入
        for tag, msg in _messages.items():
            file_format, file_name, cuted = self._file_name(tag)  # 假设这个方法已经定义
            if self.startCache:
                # 检查是否已有打开的文件对象，或者需要打开新文件
                if (
                    file_format not in self.openfiles
                    or cuted
                    or self.openfiles[file_format]["fileName"] != file_name
                ):
                    # 如果需要关闭旧文件，则关闭
                    if (
                        file_format in self.openfiles
                        and self.openfiles[file_format]["fd"] is not None
                    ):
                        self.openfiles[file_format]["fd"].close()
                    # 打开新文件
                    try:
                        fd = open(file_name, "a+")
                        self.openfiles[file_format] = {"fd": fd, "fileName": file_name}
                    except Exception as e:
                        print(f"Error opening file {file_name}: {e}")
                        continue
                else:
                    fd = self.openfiles[file_format]["fd"]

                # 写入文件
                if fd:
                    fd.write(msg)
                    fd.flush()
        else:
            # 如果不使用缓存，直接写入文件
            with open(file_name, "a+") as fd:
                fd.write(msg)
