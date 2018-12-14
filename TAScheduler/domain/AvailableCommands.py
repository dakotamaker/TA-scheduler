from .Role import Role

##This class is to define the available commands to a user role
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
        self.addAvailableCommand([Role.Administrator, Role.Instructor, Role.Supervisor], "Notify", "notify")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor], "Edit User Information", "edit-user")
        self.addAvailableCommand([Role.Instructor,Role.TA], "Edit Information", "edit")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor, Role.Instructor, Role.TA], "List TAs", "list-tas")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor, Role.Instructor, Role.TA], "View User","view-user")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor, Role.Instructor], "View Course","view-course")
        self.addAvailableCommand([Role.Administrator, Role.Supervisor, Role.Instructor], "View Lab", "view-lab")

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