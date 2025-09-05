from component.jobs import master

from .command import commandTest

if __name__ == "__main__":
    mm = master.Master()
    mm.setCommand(commandTest.CommandTest())
    mm.run("test")
