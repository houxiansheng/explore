import os
class st:
    def __init__(self) -> None:
        print("我是谁初始化")
    def run(self):
        print(f"我是谁{os.getpid()}")


class st111:
    def __init__(self) -> None:
        print("st111初始化")
    def run(self):
        print(f"st111{os.getpid()}")
