from AbstractDataAccess import AbstractDataAccess
from Account import Account
from Course import Course
from Lab import Lab
from Role import Role
import shlex


class CommandHandler:

    def __init__(self, db: AbstractDataAccess):
        self.db = db
        self.currentUser = None

    def ProcessCommand(self, cmdString: str):
        try:
            cmd = shlex.split(cmdString)  # don't split quoted substrings
        except:
            print('Badly formatted command')
            return
        handler = {
            'exit': self.ExitHandler,
            'login': self.LoginHandler,
            'logout': self.LogoutHandler,
            'notify': self.NotifyHandler,
            'create': {
                'user': self.CreateUserHandler,
                'course': self.CreateCourseHandler,
                'lab': self.CreateLabHandler
            },
            'assign': {
                'course': self.AssignCourseHandler,
                'lab': self.AssignLabHandler
            },
            'delete': {
                'user': self.DeleteUserHandler,
                'course': self.DeleteCourseHandler,
                'lab': self.DeleteLabHandler
            },
            'view': {
                'user': self.ViewUserHandler,
                'ta': self.ViewTAHandler,
                'course': self.ViewCourseHandler,
                'lab': self.ViewLabHandler
            },
            'list': {
                'users': self.ListUsersHandler,
                'tas': self.ListTAsHandler,
                'courses': self.ListCoursesHandler,
                'labs': self.ListLabsHandler
            }
        }
        while type(handler) is dict:
            handler = handler[cmd[0].lower()]
            cmd.pop(0)
        try:
            handler(cmd)
        except Exception as e:
            print('Handler error')
            print(e)

    def ExitHandler(self, cmd: [str]):
        print('Exiting...')
        exit()

    def LoginHandler(self, cmd: [str]):
        if len(cmd) != 2:
            print('Invalid number of arguments')
            return
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            print('Given email does not belong to an existing user')
            return
        a.GetDetail()
        if a.act_password == cmd[1]:
            self.currentUser = a
            print('Logged in as', cmd[0])
        else:
            print('Invalid credentials')

    def LogoutHandler(self, cmd: [str]):
        if self.currentUser is None:
            print('No user is logged in')
            return
        self.currentUser = None
        print('Logged out')

    def NotifyHandler(self, cmd: [str]):
        print('Nofity:', cmd)

    def CreateUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Administrator or Supervisor')
            return
        if len(cmd) != 6:
            print('Invalid number of arguments')
            return
        acc = Account(self.db)
        acc.act_email = cmd[0]
        acc.act_fname = cmd[1]
        acc.act_lname = cmd[2]
        acc.role_id = cmd[3]
        acc.act_phone = cmd[4]
        acc.act_address = cmd[5]
        if acc.Exists():
            print('User already exists.')
            return
        acc.Add()
        print('User added.')


    def CreateCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Administrator or Supervisor')
            return
        if len(cmd) != 1:
            print('Invalid number of arguments')
            return
        c = Course(self.db)
        c.course_name = cmd[0]
        if c.Exists():
            print('Course already exists')
            return
        c.Add()
        print('Course added')

    def CreateLabHandler(self, cmd: [str]):
        print('Create lab:', cmd)

    def AssignCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Administrator or a Supervisor')
            return
        if len(cmd) != 2:
            print('Invalid number of arguments')
        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.Exists():
            print('This course does not exist.')
            return
        c.GetDetail()
        c.instructor_email = cmd[1]

        acc = Account(self.db)
        acc.act_email = cmd[1]
        acc.GetDetail()
        if acc.role_id is None or not acc.RoleIn(Role.Instructor):
            print('Assignee must be either an instructor')
            return

        c.Update()
        print('Instructor assigned to course')

    def AssignLabHandler(self, cmd: [str]):
        print('Assign lab:', cmd)

    def DeleteUserHandler(self, cmd: [str]):
        print('Delete user:', cmd)

    def DeleteCourseHandler(self, cmd: [str]):
        print('Delete course:', cmd)

    def DeleteLabHandler(self, cmd: [str]):
        print('Delete lab:', cmd)

    def ViewUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Administrator or a Supervisor')
            return
        if len(cmd) != 1:
            print('Invalid number of arguments')
            return
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            print('Given email does not belong to an existing user')
            return
        a.GetDetail()
        print(a)

    def ViewTAHandler(self, cmd: [str]):
        print('View TA:', cmd)

    def ViewCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Instructor, Administrator, or a Supervisor')
            return
        if len(cmd) != 1:
            print('Invalid number of arguments')
            return
        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.Exists():
            print('Course does not exist')
            return
        c.GetDetail()
        print(c)

    def ViewLabHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Instructor, Administrator, or a Supervisor')
            return
        if len(cmd) != 1:
            print('Invalid number of arguments')
            return
        l = Lab(self.db)
        if not cmd[0].isdigit():
            print('Lab ID must be a non-negative integer')
            return
        l.lab_id = int(cmd[0])
        if not l.Exists():
            print('Given lab does not exist')
            return
        l.GetDetail()
        print(l)

    def ListUsersHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Administrator or a Supervisor')
            return
        Account.PrintAll(self.db)

    def ListTAsHandler(self, cmd: [str]):
        print('List TAs:', cmd)

    def ListCoursesHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Instructor, Administrator, or a Supervisor')
            return
        Course.PrintAll(self.db)

    def ListLabsHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            print('Must be logged in as an Instructor, Administrator, or a Supervisor')
            return
        Lab.PrintAll(self.db)