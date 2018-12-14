from .Role import Role

class AvailableCommands:
    def __init__(self):
        self.commandList = []
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Create Course", "create-course")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Delete Course", "delete-course")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Create User", "create-user")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Delete User", "delete-user")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Create Lab", "create-lab")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Delete Lab", "delete-lab")
        self.addAvailableCommand([Role.Instructor, Role.Supervisor], "Assign Course TA", "assign-course-ta")
        self.addAvailableCommand(Role.Supervisor, "Assign Course Instructor", "assign-course-instructor")
        self.addAvailableCommand([Role.Instructor, Role.Supervisor], "Assign Lab", "assign-lab")



    def addAvailableCommand(self, cmd_role: Role, cmd_txt, cmd_url):
        if isinstance(cmd_role, list):
            for i in cmd_role:
                anAvailableCommand = {"cmd_role": i, "cmd_txt": cmd_txt, "cmd_url": cmd_url}
                self.commandList.append(anAvailableCommand)
        else:
            anAvailableCommand = {"cmd_role": cmd_role, "cmd_txt": cmd_txt, "cmd_url": cmd_url}
            self.commandList.append(anAvailableCommand)

    def getAvailableCommands(self, for_role: Role):
        commandList = []
        for i in self.commandList:
            if i["cmd_role"] == for_role:
                commandList.append(i)
        return commandList