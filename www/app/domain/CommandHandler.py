from .models.Account import Account
from .models.Course import Course
from .models.Lab import Lab
from .Role import Role
from .ErrorMessages import ErrorMessages
import shlex


class CommandHandler:

    def __init__(self):
        self.currentUser = None
        Account.objects.get_or_create(act_email='supervisor@email.com', act_fname='supervisor', act_lname='user',
                                      act_password='password', act_address='1234 Main St., Milwaukee, WI',
                                      act_phone='123-123-1234', role_id=4)

    def ProcessCommand(self, cmdString: str) -> str:
        try:
            cmd = shlex.split(cmdString)  # don't split quoted substrings
        except:
            return 'Badly formatted command'

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
                'course': {
                    'ta': self._AssignCourseTAHandler,
                    'instructor': self._AssignCourseInstructorHandler
                },
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
            try:
                handler = handler[cmd[0].lower()]
            except Exception as e:
                return 'Invalid command'
            cmd.pop(0)
        try:
            return handler(cmd)
        except Exception as e:
            return 'Handler error - %s' % e

    def _ExitHandler(self, cmd: [str]):
        print('Exiting...')
        exit()

    def _LoginHandler(self, cmd: [str]):
        if len(cmd) != 2:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        a = Account.objects.get(act_email=cmd[0])
        if not a:
            return 'Given email does not belong to an existing user'
        if a.act_password != '':
            if a.act_password == cmd[1]:
                self.currentUser = a
                return 'Logged in as %s' % cmd[0]
            else:
                return 'Invalid credentials'
        else:
            a.act_password = cmd[1]
            a.save()
            return 'Logged in as %s, your new password has been saved' % cmd[0]

    def _LogoutHandler(self, cmd: [str]):
        if not self.currentUser:
            return 'No user is logged in'
        self.currentUser = None
        return 'Logged out'

    def _EditHandler(self, cmd: [str]):
        pass

    def _NotifyHandler(self, cmd: [str]):
        if not self.currentUser or self.currentUser.RoleIn(Role.TA):
            return 'TAs cannot send notifications'
        elif self.currentUser.RoleIn(Role.Instructor):
            # Logic to look for TA that is in the instructor's class, to implement later
            return
        if len(cmd) != 3:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        user = Account.objects.get(act_email=cmd[0])
        if user:
            return 'Notification email sent to %s!' % user.act_email
        else:
            return 'This user does not exist'

    def _CreateUserHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 6:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        acc = Account.objects.filter(act_email=cmd[0])
        if acc:
            return 'User already exists'
        acc = Account()
        acc.act_email = cmd[0]
        acc.act_fname = cmd[1]
        acc.act_lname = cmd[2]
        acc.role_id = cmd[3]
        acc.act_phone = cmd[4]
        acc.act_address = cmd[5]
        acc.save()
        return 'User added'

    def _CreateCourseHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        c = Course.objects.filter(course_name=cmd[0])
        if c:
            return 'Course already exists'
        c = Course(course_name=cmd[0])
        c.save()
        return 'Course added'

    def _CreateLabHandler(self, cmd: [str]):
        return 'Create lab:' + cmd

    def _AssignCourseTAHandler(self, cmd: [str]):
        c = Course.objects.get(course_name=cmd[0])
        a = Account.objects.get(act_email=cmd[1])
        c.tas.add(a)

    def _AssignCourseInstructorHandler(self, cmd: [str]):
        pass

    def _AssignLabHandler(self, cmd: [str]):
        return 'Assign lab:' + cmd

    def _DeleteUserHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS
        a = Account.objects.get(act_email=cmd[0])
        if not a:
            return 'Given email does not belong to an existing user'
        a.delete()
        return 'Deleted user %s' % cmd[0]

    def _DeleteCourseHandler(self, cmd: [str]):
        return 'Delete course:' + cmd

    def _DeleteLabHandler(self, cmd: [str]):
        return 'Delete lab:' + cmd

    def _ViewUserHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS

    def _ViewCourseHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                                   Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS

    def _ViewLabHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                                   Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'
        if len(cmd) != 1:
            return ErrorMessages.INVALID_NUM_OF_ARGUMENTS

    def _ListUsersHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Administrator, Role.Supervisor):
            return 'Must be logged in as an Administrator or a Supervisor'

    def _ListTAsHandler(self, cmd: [str]):
        return 'List TAs:' + cmd

    def _ListCoursesHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                                   Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'

    def _ListLabsHandler(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.RoleIn(Role.Instructor, Role.Administrator,
                                                                   Role.Supervisor):
            return 'Must be logged in as an Instructor, Administrator, or a Supervisor'
