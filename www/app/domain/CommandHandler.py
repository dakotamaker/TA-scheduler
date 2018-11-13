from www.app.domain.models.Account import Account
from www.app.domain.models.Course import Course
from www.app.domain.models.Lab import Lab
from .Role import Role
from .ErrorMessages import ErrorMessages
import shlex


class CommandHandler:

    def __init__(self):
        self.currentUser = None

    def ProcessCommand(self, cmdString: str):
        try:
            cmd = shlex.split(cmdString)  # don't split quoted substrings
        except:
            return self._printAndReturnNonDatabaseMessages('Badly formatted command')

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
            return handler(cmd)
        except Exception as e:
            return self._printAndReturnNonDatabaseMessages('Handler error - %s' % e)

    def _ExitHandler(self, cmd: [str]):
        print('Exiting...')
        exit()

    def _LoginHandler(self, cmd: [str]):
        if len(cmd) != 2:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            return self._printAndReturnNonDatabaseMessages('Given email does not belong to an existing user')
        a.GetDetail()
        if a.act_password != '':
            if a.act_password == cmd[1]:
                self.currentUser = a
                return self._printAndReturnNonDatabaseMessages('Logged in as %s' % cmd[0])
            else:
                return self._printAndReturnNonDatabaseMessages('Invalid credentials')
        else:
            self._updateAccountInfo(a, 'act_password:%s' % cmd[1])
            self.currentUser = a
            return self._printAndReturnNonDatabaseMessages('Logged in as %s, your new password has been saved' % cmd[0])

    def _LogoutHandler(self, cmd: [str]):
        if self.currentUser is None:
            return self._printAndReturnNonDatabaseMessages('No user is logged in')
        self.currentUser = None
        return self._printAndReturnNonDatabaseMessages('Logged out')

    def _EditHandler(self, cmd: [str]):
        user = Account(self.db)
        if self.currentUser is None:
            return self._printAndReturnNonDatabaseMessages('Must be logged in to edit an account')
        elif self.currentUser is self.currentUser.RoleIn(Role.Supervisor) or self.currentUser.RoleIn(Role.Administrator):
            print(len(cmd))
            if len(cmd) != 1 and len(cmd) != 3:
                return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
            user.act_email = self.currentUser.act_email if cmd[0] != 'user' else cmd[1]
            if user.Exists():
                (lambda: self._updateAccountInfo(user, cmd[0]), lambda: self._updateAccountInfo(user, cmd[2]))[cmd[0] == 'user']()
            else:
                return self._printAndReturnNonDatabaseMessages('%s does not exist' % user.act_email)
        else:
            if len(cmd) != 1:
                return self._printAndReturnNonDatabaseMessages('Only supervisors or admins can edit another user.')
            self._updateAccountInfo(self.currentUser, cmd)

    def _NotifyHandler(self, cmd: [str]):
        if self.currentUser is None or self.currentUser.RoleIn(Role.TA):
            return self._printAndReturnNonDatabaseMessages('TAs cannot send notifications')
        elif self.currentUser.RoleIn(Role.Instructor):
            # Logic to look for TA that is in the instructor's class, to implement later
            return
        if len(cmd) != 3:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        user = Account(self.db)
        user.act_email = cmd[0]
        if user.Exists():
            return self._printAndReturnNonDatabaseMessages('Notification email sent to %s!' % user.act_email)
        else:
            return self._printAndReturnNonDatabaseMessages('This user does not exist')

    def _CreateUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Administrator or Supervisor')
        if len(cmd) != 6:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        acc = Account(self.db)
        acc.act_email = cmd[0]
        acc.act_fname = cmd[1]
        acc.act_lname = cmd[2]
        acc.role_id = cmd[3]
        acc.act_phone = cmd[4]
        acc.act_address = cmd[5]
        if acc.Exists():
            return self._printAndReturnNonDatabaseMessages('User already exists.')
        acc.Add()
        return self._printAndReturnNonDatabaseMessages('User added.')

    def _CreateCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Administrator or Supervisor')
        if len(cmd) != 1:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course(self.db)
        c.course_name = cmd[0]
        if c.Exists():
            return self._printAndReturnNonDatabaseMessages('Course already exists.')
        c.Add()
        return self._printAndReturnNonDatabaseMessages('Course added')

    def _CreateLabHandler(self, cmd: [str]):
        return self._printAndReturnNonDatabaseMessages('Create lab:' + cmd)

    def _AssignCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Administrator or a Supervisor')
        if len(cmd) != 2:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.Exists():
            return self._printAndReturnNonDatabaseMessages('This course does not exist.')
        c.GetDetail()
        c.instructor_email = cmd[1]

        acc = Account(self.db)
        acc.act_email = cmd[1]
        if not acc.Exists():
            return self._printAndReturnNonDatabaseMessages('This user does not exist.')
        acc.GetDetail()
        if not acc.RoleIn(Role.Instructor):
            return self._printAndReturnNonDatabaseMessages('Assignee must be an instructor')
        c.Update()
        return self._printAndReturnNonDatabaseMessages('Instructor assigned to course')

    def _AssignLabHandler(self, cmd: [str]):
        return self._printAndReturnNonDatabaseMessages('Assign lab:' + cmd)

    def _DeleteUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Administrator or a Supervisor')
        if len(cmd) != 1:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            return self._printAndReturnNonDatabaseMessages('Given email does not belong to an existing user')
        a.Delete()
        return self._printAndReturnNonDatabaseMessages('Removed %s' % cmd[0])

    def _DeleteCourseHandler(self, cmd: [str]):
        return self._printAndReturnNonDatabaseMessages('Delete course:' + cmd)

    def _DeleteLabHandler(self, cmd: [str]):
        return self._printAndReturnNonDatabaseMessages('Delete lab:' + cmd)

    def _ViewUserHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Administrator or a Supervisor')
        if len(cmd) != 1:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        a = Account(self.db)
        a.act_email = cmd[0]
        if not a.Exists():
            return self._printAndReturnNonDatabaseMessages('Given email does not belong to an existing user')
        a.GetDetail()
        return self._printAndReturnNonDatabaseMessages(a.__str__())

    def _ViewCourseHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Instructor, Administrator, or a Supervisor')
        if len(cmd) != 1:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        c = Course(self.db)
        c.course_name = cmd[0]
        if not c.Exists():
            return self._printAndReturnNonDatabaseMessages('Course does not exist')
        c.GetDetail()
        return self._printAndReturnNonDatabaseMessages(c.__str__())

    def _ViewLabHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Instructor, Administrator, or a Supervisor')
        if len(cmd) != 1:
            return self._printAndReturnNonDatabaseMessages(ErrorMessages.INVALID_NUM_OF_ARGUMENTS)
        l = Lab(self.db)
        if not cmd[0].isdigit():
            return self._printAndReturnNonDatabaseMessages('Lab ID must be a non-negative integer')
        l.lab_id = int(cmd[0])
        if not l.Exists():
            return self._printAndReturnNonDatabaseMessages('Given lab does not exist')
        l.GetDetail()
        return self._printAndReturnNonDatabaseMessages(l.__str__())

    def _ListUsersHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Administrator or a Supervisor')

        Account.PrintAll(self.db)

    def _ListTAsHandler(self, cmd: [str]):
        return self._printAndReturnNonDatabaseMessages('List TAs:' + cmd)

    def _ListCoursesHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Instructor, Administrator, or a Supervisor')

        return Course.PrintAll(self.db)

    def _ListLabsHandler(self, cmd: [str]):
        if self.currentUser is None or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator, Role.Supervisor):
            return self._printAndReturnNonDatabaseMessages('Must be logged in as an Instructor, Administrator, or a Supervisor')
        return Lab.PrintAll(self.db)

    def _printAndReturnNonDatabaseMessages(self, message: str):
        print(message)
        return message

    def _updateAccountInfo(self, account: Account, value: str):
        new_value = value.split(":")
        if len(new_value) != 2:
            return self._printAndReturnNonDatabaseMessages('To edit an account you need a semicolon')
        account.GetDetail()
        setattr(account, new_value[0], new_value[1])
        account.Update()
