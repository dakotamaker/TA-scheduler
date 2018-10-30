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

    def ProcessCommand(self, cmdString):
        cmd = shlex.split(cmdString)  # don't split quoted substrings
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
            }
        }
        while type(handler) is dict:
            handler = handler[cmd[0].lower()]
            cmd.pop(0)
        try:
            handler(cmd)
        except Exception as e:
            print('Handler error - ', e)

    def ExitHandler(self, cmd):
        print('Exiting...')
        exit()

    def LoginHandler(self, cmd):
        a = Account(self.db)
        a.act_email = cmd[0]
        a.GetDetail()
        if a.act_password == cmd[1]:
            self.currentUser = a
            print('Logged in as', cmd[0])
        else:
            print('Invalid credentials')

    def LogoutHandler(self, cmd):
        self.currentUser = None
        print('Logged out')

    def NotifyHandler(self, cmd):
        print('Nofity:', cmd)

    def CreateUserHandler(self, cmd):
        print('Create user:', cmd)

    def CreateCourseHandler(self, cmd):
        if self.currentUser is None or Role(self.currentUser.role_id) < Role.Administrator:
            print('Must be logged in as an Administrator or Supervisor')
            return

        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.CanAdd():
            print('Course already exists')
            return
        c.Add()
        print('Course added')

    def CreateLabHandler(self, cmd):
        print('Create lab:', cmd)

    def AssignCourseHandler(self, cmd):
        print('Assign course:', cmd)

    def AssignLabHandler(self, cmd):
        print('Assign lab:', cmd)

    def DeleteUserHandler(self, cmd):
        print('Delete user:', cmd)

    def DeleteCourseHandler(self, cmd):
        print('Delete course:', cmd)

    def DeleteLabHandler(self, cmd):
        print('Delete lab:', cmd)
