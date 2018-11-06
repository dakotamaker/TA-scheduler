from src.AbstractDataAccess import AbstractDataAccess
from src.Account import Account
from src.Course import Course
from src.Lab import Lab
from src.Role import Role
from src.ErrorMessages import ErrorMessages
import shlex


class CommandHandler:

    def __init__(self, db: AbstractDataAccess):
        self.db = db
        self.currentUser = None

    def ProcessCommand(self, cmdString: str):
        try:
            cmd = shlex.split(cmdString)  # don't split quoted substrings
        except:
            return print('Badly formatted command')

        handler = {
            'exit': self._ExitHandler,
            'login': self._LoginHandler,
            'logout': self._LogoutHandler,
            'notify': self._NotifyHandler,
            'edit': self._EditHandler,
            'create': {
                'user': self._CreateUserHandler,
                'course': self._CreateCourseHandler,
                'lab': self._CreateLabHandler
            },
            'assign': {
                'course': self._AssignCourseHandler,
                'lab': self._AssignLabHandler
            },
            'delete': {
                'user': self._DeleteUserHandler,
                'course': self._DeleteCourseHandler,
                'lab': self._DeleteLabHandler
            },
            'view': {
                'user': self._ViewUserHandler,
                'ta': self._ViewTAHandler,
                'course': self._ViewCourseHandler,
                'lab': self._ViewLabHandler
            },
            'list': {
                'users': self._ListUsersHandler,
                'tas': self._ListTAsHandler,
                'courses': self._ListCoursesHandler,
                'labs': self._ListLabsHandler
            }
        }
        while type(handler) is dict:
            handler = handler[cmd[0].lower()]
            cmd.pop(0)
        try:
            handler(cmd)
        except Exception as e:
            return print('Handler error -', e)

    def _ExitHandler(self, cmd: [str]):
        return print('Exiting...')
        exit()

    def _LoginHandler(self, cmd: [str]):
        if len(cmd) != 2:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            return print('Given email does not belong to an existing user')
        a.GetDetail()
        if a.act_password == cmd[1]:
            self.currentUser = a
            return print('Logged in as', cmd[0])
        else:
            return print('Invalid credentials')

    def _LogoutHandler(self, cmd: [str]):
        if self.currentUser is None:
            return print('No user is logged in')
        self.currentUser = None
        return print('Logged out')

    def _EditHandler(self, cmd: [str]):
        user = Account(self.db)
        if self.currentUser is None:
            return print('Must be logged in to edit an account')
        elif self.currentUser is self.currentUser.RoleIn(Role.Supervisor) or self.currentUser.RoleIn(Role.Administrator):
            if len(cmd) != 1 and len(cmd) != 3:
                return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
            user.act_email = self.currentUser.act_email if cmd[0] != 'user' else cmd[1]
            if user.Exists():
                (lambda: self._updateAccountInfo(user, cmd[0]), lambda: self._updateAccountInfo(user, cmd[2]))[cmd[0] == 'user']()
            else:
                return print('%s does not exist' % user.act_email)
        else:
            if len(cmd) != 1:
                return print('Only supervisors or admins can edit another user.')
            self._updateAccountInfo(self.currentUser, cmd)

    def _NotifyHandler(self, cmd: [str]):
        if self.currentUser is None or self.currentUser.RoleIn(Role.TA):
            return print('Must be logged in or at least an instructor to send a notification')
        elif self.currentUser.RoleIn(Role.Instructor):
            # Logic to look for TA that is in the instructor's class, to implement later
            return
        if len(cmd) != 3:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        user = Account(self.db)
        user.act_email = cmd[0]
        if user.Exists():
            return print('Notification email sent to %s!' % user)
        else:
            return print('This user does not exist')

    def _CreateUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Administrator or Supervisor')
        if len(cmd) != 6:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        acc = Account(self.db)
        acc.act_email = cmd[0]
        acc.act_fname = cmd[1]
        acc.act_lname = cmd[2]
        acc.role_id = cmd[3]
        acc.act_phone = cmd[4]
        acc.act_address = cmd[5]
        if acc.Exists():
            return print('User already exists.')
        acc.Add()
        return print('User added.')

    def _CreateCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Administrator or Supervisor')
        if len(cmd) != 1:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course(self.db)
        c.course_name = cmd[0]
        if c.Exists():
            return print('Course already exists')
        c.Add()
        return print('Course added')

    def _CreateLabHandler(self, cmd: [str]):
        return print('Create lab:', cmd)

    def _AssignCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Administrator or a Supervisor')
        if len(cmd) != 2:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.Exists():
            return print('This course does not exist.')
        c.GetDetail()
        c.instructor_email = cmd[1]

        acc = Account(self.db)
        acc.act_email = cmd[1]
        if not acc.Exists():
            return print('This user does not exist.')
        acc.GetDetail()
        if acc.role_id is not acc.RoleIn(Role.Instructor):
            return print('Assignee must be an instructor')
        c.Update()
        return print('Instructor assigned to course')

    def _AssignLabHandler(self, cmd: [str]):
        return print('Assign lab:', cmd)

    def _DeleteUserHandler(self, cmd: [str]):
        return print('Delete user:', cmd)

    def _DeleteCourseHandler(self, cmd: [str]):
        return print('Delete course:', cmd)

    def _DeleteLabHandler(self, cmd: [str]):
        return print('Delete lab:', cmd)

    def _ViewUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Administrator or a Supervisor')
        if len(cmd) != 1:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            return print('Given email does not belong to an existing user')
        a.GetDetail()
        return print(a)

    def _ViewTAHandler(self, cmd: [str]):
        return print('View TA:', cmd)

    def _ViewCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Instructor, Administrator, or a Supervisor')
        if len(cmd) != 1:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.Exists():
            return print('Course does not exist')
        c.GetDetail()
        return print(c)

    def _ViewLabHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Instructor, Administrator, or a Supervisor')
        if len(cmd) != 1:
            return print(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        l = Lab(self.db)
        if not cmd[0].isdigit():
            return print('Lab ID must be a non-negative integer')
        l.lab_id = int(cmd[0])
        if not l.Exists():
            return print('Given lab does not exist')
        l.GetDetail()
        return print(l)

    def _ListUsersHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Administrator or a Supervisor')

        Account.PrintAll(self.db)

    def _ListTAsHandler(self, cmd: [str]):
        return print('List TAs:', cmd)

    def _ListCoursesHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Instructor, Administrator, or a Supervisor')

        Course.PrintAll(self.db)

    def _ListLabsHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return print('Must be logged in as an Instructor, Administrator, or a Supervisor')
        Lab.PrintAll(self.db)

    def _updateAccountInfo(self, account: Account, value: str):
        new_value = value.split(":")
        if len(new_value) != 2:
            return print('To edit an account you need a semicolon')
        account.GetDetail()
        setattr(account, new_value[0], new_value[1])
        account.Update()
